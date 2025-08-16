# tele_consumer.py
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
        payload_str = message.body.decode()
        payload = json.loads(payload_str)

        user_id = payload["user_id"]
        reminder = payload["reminder"]
        reminder_dt = payload["reminder_dt"]

        response = await save_or_update_reminder(
            reminders=reminder, user=user_id, time=reminder_dt
        )

        status = response.get("success")
        if status:
            await message.ack()
            logging.info(f"Reminder saved: {response.get('task_id')}")
        else:
            await message.reject(requeue=False)
            logging.warning("Reminder rejected - no success flag")

    except Exception as e:
        logging.error(f"Error while processing message: {e}")
        await message.reject(requeue=False)

async def start_consumer():
    connection = await aio_pika.connect_robust(getenv("rabbit_url"))
    channel = await connection.channel()
    queue = await channel.declare_queue("reminders", durable=True)

    await queue.consume(process_message)
    logging.info("Waiting for RabbitMQ messages...")

    return connection