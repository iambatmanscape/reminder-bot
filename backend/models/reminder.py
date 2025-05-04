from typing import Annotated,List
from beanie import Document,Indexed
from pydantic import Field
from datetime import datetime


class Reminder(Document):
    reminder:List[str] = Field(default_factory=list)
    time:datetime
    task_id:Annotated[str,Indexed(unique=True)]
    user:str

    class Settings:
        name='reminders'
    
