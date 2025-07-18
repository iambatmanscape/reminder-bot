from fastapi import FastAPI
from api.routes import router as api_router
from models import init_db
from .utils import start_consumer
from contextlib import asynccontextmanager
import uvicorn
import asyncio
import logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifecycle(app:FastAPI):
    connection = await start_consumer()
    yield
    await connection.close()
    logging.info(f"Shutting down!")

app = FastAPI(lifespan=lifecycle)

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