import logging
from dotenv import load_dotenv
load_dotenv('.env')
from os import getenv
from telegram.ext import filters, ApplicationBuilder
from lib import start,echo

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(getenv('telegram_id')).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()