import asyncio
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
import logging
import json
from .reminder_controller import save_or_update_reminder
from os import getenv
from dotenv import load_dotenv
load_dotenv('.env')


async def process_message(message: AbstractIncomingMessage):
    try:
        async with message.process():
            payload_str = message.body.decode()
            payload = json.loads(payload_str)
            user_id = payload['user_id']
            reminder = payload['reminder']
            reminder_dt = payload['reminder_dt']
            response = await save_or_update_reminder(reminders=reminder,user=user_id,time=reminder_dt)
            status = response.get('success',None)
            if status == True:
                res = response.get('task_id')
                return {
                    "task_id":res
                }
    except Exception as e:
        logging.error(f"Error occured while processing message: {e}")
        raise Exception(status_code=400, detail="Failed to add or update reminder.")

async def start_consumer():
    connection = await aio_pika.connect_robust(getenv('rabbit_url'))
    channel = await connection.channel()
    queue = await channel.declare_queue("reminders", durable=True)
    res = await queue.consume(process_message)
    logging.info(f"New task created!")
    logging.debug("Waiting for messages...")
    return connection

if __name__ == "__main__":
    asyncio.run(start_consumer())