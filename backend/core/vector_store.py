# vector_store.py
from qdrant_client.async_qdrant_client import AsyncQdrantClient



qdrant_client = AsyncQdrantClient(
    host="localhost",
    grpc_port=6334,
    prefer_grpc=True
    
)







