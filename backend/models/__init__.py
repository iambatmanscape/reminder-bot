from .reminder import Reminder,ReminderUpdateSchema,ReminderSchema
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv('.env')
from os import getenv
import logging

async def init_db():
    logging.info(getenv('MDB_URI_STRING'))
    client = AsyncIOMotorClient(
        getenv('MDB_URI_STRING')
    )

    db_name = client['reminders']
    await init_beanie(database=db_name, document_models=[Reminder])

__all__ = [Reminder,ReminderUpdateSchema,ReminderSchema,init_db]