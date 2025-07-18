from core import settings
from langchain.vectorstores import Qdrant
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams



qdrant_client = AsyncQdrantClient(
    host="localhost",
    port=6333,
)


def create_and_return_vector_store(
    qdrant_client,
    collection_name: str = 'default',
    embedding_model=None,
    vector_size: int = 384,
    recreate: bool = False
):
    """
    Create (or return) a Qdrant vector store.
    If 'recreate' is True, collection will be dropped and re-created.
    If 'recreate' is False, collection will only be created if it does not exist.
    """
    if recreate:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )
    else:
        if not qdrant_client.collection_exists(collection_name=collection_name):
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embedding_model,
    )
    return vector_store







