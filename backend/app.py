from fastapi import FastAPI
from backend.api.reminder_routes import router as reminder_router
from backend.api.knowledgebase_routes import router as knowledgebase_router
from backend.models import init_db
from contextlib import asynccontextmanager
from backend.core import scheduler, settings
import uvicorn
import asyncio
import logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    settings.setup()
    scheduler.start()
    logging.info("Application started!")
    yield
    logging.info("Application stopped!")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to Telegram backend!"}

app.include_router(reminder_router, prefix="/api")
app.include_router(knowledgebase_router, prefix="/api")

def main():
    config = uvicorn.Config("backend.app:app", host="127.0.0.1", port=5000, reload=True)
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()