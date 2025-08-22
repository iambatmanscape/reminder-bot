import os
from pydantic import BaseModel
from typing import List, Union
from backend.core import qdrant_client,settings
import xml.etree.ElementTree as ET
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, WebBaseLoader



text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


async def ensure_collection(collection_name: str, vector_size: int = 384, recreate: bool = False):
    if recreate:
        await qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
    else:
        exists = await qdrant_client.collection_exists(collection_name=collection_name)
        if not exists:
            await qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

# core insert function
async def insert_documents(documents, collection_name: str, recreate: bool = False):
    await ensure_collection(collection_name, recreate=recreate)

    splits = text_splitter.split_documents(documents)
    texts = [doc.page_content for doc in splits]

    vectors = await settings.embedding_model.aembed_documents(texts)

    points = [
        PointStruct(
            id=idx,
            vector=vectors[idx],
            payload={"text": texts[idx], "metadata": splits[idx].metadata},
        )
        for idx in range(len(texts))
    ]

    await qdrant_client.upsert(collection_name=collection_name, points=points)
    return len(points)

# loaders
async def process_pdf(path: str, collection_name="default", recreate=False):
    loader = PyMuPDFLoader(path)
    docs = loader.load()
    return await insert_documents(docs, collection_name, recreate)

async def process_text(path: str, collection_name="default", recreate=False):
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    return await insert_documents(docs, collection_name, recreate)

async def process_web(url: str, collection_name="default", recreate=False):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return await insert_documents(docs, collection_name, recreate)

# auto dispatcher
ALLOWED_TEXT_EXTS = {".txt", ".md", ".log", ".csv"}
ALLOWED_PDF_EXTS = {".pdf"}
BLOCKED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3", ".wav", ".avi"}

class ProcessAutoInputs(BaseModel):
    inputs: List[Union[str, os.PathLike]] 
    collection_name:str="default"
    recreate:bool=False

async def process_auto(process_inputs: ProcessAutoInputs):
    report = {"pdf": 0, "text": 0, "url": 0, "rejected": []}
    total_points = 0

    inputs = process_inputs.inputs
    collection_name = process_inputs.collection_name
    recreate = process_inputs.recreate

    for idx, item in enumerate(inputs):
        is_first = (idx == 0)

        if isinstance(item, str) and (item.startswith("http://") or item.startswith("https://")):
            total_points += await process_web(item, collection_name, recreate=(recreate and is_first))
            report["url"] += 1

        elif isinstance(item, (str, os.PathLike)):
            ext = os.path.splitext(str(item).lower())[1]

            if ext in BLOCKED_EXTS:
                report["rejected"].append(str(item))
                continue

            if ext in ALLOWED_PDF_EXTS:
                total_points += await process_pdf(str(item), collection_name, recreate=(recreate and is_first))
                report["pdf"] += 1

            elif ext in ALLOWED_TEXT_EXTS:
                total_points += await process_text(str(item), collection_name, recreate=(recreate and is_first))
                report["text"] += 1

            else:
                report["rejected"].append(str(item))

        else:
            report["rejected"].append(str(item))

    return total_points, report

class SearchParams(BaseModel):
    query:str
    collection_name:str = "default"
    top_k:int = 5
    score_threshold:float = None



async def search_query(
    search_params:SearchParams
) -> str:
    """
    Fetch documents similar to the query from Qdrant and return results as XML.
    """

    query = search_params.query
    collection_name = search_params.collection_name
    top_k = search_params.top_k
    score_threshold = search_params.score_threshold
    
    query_vector = await settings.embedding_model.aembed_query(query)

    
    results = await qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        score_threshold=score_threshold,
    )

    
    root = ET.Element("documents")

    for hit in results:
        doc_el = ET.SubElement(root, "document")

        score_el = ET.SubElement(doc_el, "score")
        score_el.text = f"{hit.score:.4f}"

        text_el = ET.SubElement(doc_el, "text")
        text_el.text = hit.payload.get("text", "")

        metadata_el = ET.SubElement(doc_el, "metadata")
        for k, v in hit.payload.get("metadata", {}).items():
            meta_el = ET.SubElement(metadata_el, k)
            meta_el.text = str(v)

    
    return ET.tostring(root, encoding="unicode")



