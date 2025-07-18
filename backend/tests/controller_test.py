from models import init_db
from utils import save_or_update_reminder,clear_reminder
import asyncio
from datetime import datetime, timedelta
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def test_reminder_crud():

    await init_db()

    user = "916306755989"
    time = datetime.now() + timedelta(minutes=5)
    reminders = ["Drink water", "Stand up"]

    logging.info("Adding reminder...")
    saved = await save_or_update_reminder(reminders,user,time)
    logging.info("Saved:", saved)
    if saved:
        task_id = saved.get('task_id', None)

    if task_id:        
        logging.info("Updating reminder...")
        updated = await save_or_update_reminder(old_task_id=task_id, reminders=["Stretch", "Check posture"], user=user)
        logging.info("Updated:", updated)
        if updated:
            updated_task_id = updated.get('task_id',None)

    if updated_task_id:
        logging.info("Deleting reminder...")
        deleted = await clear_reminder(user, updated_task_id)
        logging.info("Deleted:", deleted)
        if deleted:
            deleted_task = deleted.get('task',)


asyncio.run(test_reminder_crud())
