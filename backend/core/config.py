from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import getenv

class Settings:
    def __init__(self):
        self.embedding_model = None
    
    def setup(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model=getenv("embedding_model"), google_api_key=getenv('google_api_key'))
