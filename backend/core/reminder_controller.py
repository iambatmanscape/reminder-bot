from models import Reminder
from datetime import datetime


async def add_reminder(reminder:list[str],time:datetime,user:str):
    try:
        task_id = hash(time)
        remind = Reminder(reminder=reminder,time=time,task_id=task_id,user=user)
        await remind.save()
    except Exception as e:
        raise(f"Insert reminder error!: {e}")


async def update_reminder(reminder:list[str],time:datetime,user:str,to_update:str):
    try:
        pass
    except Exception as e:
        raise(f"Update Error: {e}")
        

