import logging
from dotenv import load_dotenv
load_dotenv('.env')
from os import getenv
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler
from lib import start,echo,set_reminder, start_consumer
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def on_startup(app):
    asyncio.create_task(start_consumer())
    logging.info("RabbitMQ consumer started")

def main():
    application = ApplicationBuilder().token(getenv("telegram_id")).post_init(on_startup).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_reminder))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.run_polling()



if __name__ == '__main__':
    main()