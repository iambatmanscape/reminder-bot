from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import getenv

class Settings:
    def __init__(self):
        # self.embedding_model = HuggingFaceEmbeddings(model_name=getenv('embedding_model','sentence-transformers/all-MiniLM-L6-v2'))
        self.embedding_model = None
