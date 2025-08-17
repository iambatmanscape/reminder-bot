from fastapi import FastAPI
from api.routes import router as api_router
from models import init_db
from contextlib import asynccontextmanager
from core import scheduler
import uvicorn
import asyncio
import logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ init DB first
    await init_db()
    scheduler.start()
    logging.info("Application started!")
    yield
    logging.info("Application stopped!")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to Telegram backend!"}

app.include_router(api_router, prefix="/api")

def main():
    config = uvicorn.Config("app:app", host="127.0.0.1", port=5000, reload=True)
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()