from langchain.text_splitter import RecursiveCharacterTextSplitter
from .vector_store import create_and_return_vector_store
from langchain.document_loaders import PyMuPDFLoader, WebBaseLoader, TextLoader
from dotenv import load_dotenv
load_dotenv('.env')
from os import getenv


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)





