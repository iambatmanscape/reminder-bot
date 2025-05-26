import asyncio
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
import logging
from .reminder_controller import save_or_update_reminder
from os import getenv
from dotenv import load_dotenv
load_dotenv('.env')


async def process_message(message: AbstractIncomingMessage):
    async with message.process():
        payload = message.body.decode()
        logging.info(f"Received reminder: {payload}")
        user_id = payload['user_id']
        reminder = payload['reminder']
        reminder_dt = payload['reminder_dt']
        saved = await save_or_update_reminder(reminders=[reminder])

async def start_consumer():
    connection = await aio_pika.connect_robust(getenv('rabbit_url'))
    channel = await connection.channel()
    queue = await channel.declare_queue("reminders", durable=True)
    await queue.consume(process_message)
    logging.debug("Waiting for messages...")
    return connection

if __name__ == "__main__":
    asyncio.run(start_consumer())