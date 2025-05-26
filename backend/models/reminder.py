from typing import Annotated,List
from beanie import Document,Indexed
from pydantic import Field,BaseModel
from datetime import datetime

class ReminderUpdateSchema(BaseModel):
    success:bool
    task_id:str

class TimeModel(BaseModel):
    time:datetime

class ReminderSchema(BaseModel):
    reminder:str
    time:datetime
    task_id:Annotated[str,Indexed(unique=True)]
    user:str

class Reminder(Document):
    reminder:str
    time:datetime
    task_id:Annotated[str,Indexed(unique=True)]
    user:str

    class Settings:
        name='reminders'
    
