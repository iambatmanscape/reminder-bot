from fastapi import FastAPI
from api import router as api_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Boilerplate"}

app.include_router(api_router, prefix="/api")


