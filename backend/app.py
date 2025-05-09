from fastapi import FastAPI
from api.routes import router as api_router
from models import init_db
import uvicorn
import asyncio
import logging
logging.basicConfig(level=logging.INFO)


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Telegram backend!"}

app.include_router(api_router, prefix="/api")

async def main():
    await init_db()
    config = uvicorn.Config("app:app", host="127.0.0.1", port=5000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())