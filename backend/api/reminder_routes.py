from backend.utils import save_or_update_reminder,clear_reminder,get_reminder_by_datetime,get_reminders
from backend.models import ReminderSchema,TimeModel
from fastapi import APIRouter,Body,Path,HTTPException
from datetime import datetime
from typing import Dict,List,Annotated
import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post('/{user}/reminders/add',status_code=201)
async def add_or_update_reminder(reminders:str=Body(...),user:str=Path(...),time:datetime=Body(...),task_id:str=Body(...,default_factory=str))->Dict[str,str]:
    try:
        response = await save_or_update_reminder(reminders,user,time,old_task_id=task_id)
        status = response.get('success',None)
        if status == True:
            res = response.get('task_id')
            return {
                "task_id":res
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to add or update reminder.")
        
    except Exception as e:
        logging.error(f"Exception while adding reminder!: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get('/{user}/reminders',response_model=List[ReminderSchema],status_code=200)
async def all_reminders(user:str=Path(...))->List[ReminderSchema]:
    try:
        tasks = await get_reminders(user)
        return tasks

    except Exception as e:
        logging.error(f"Exception while getting reminders!: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.post('/{user}/reminders/by-time',response_model=List[ReminderSchema],status_code=200)
async def get_current_reminders(user:str=Path(...),time:TimeModel=Body(...))->List[ReminderSchema]:
    try:
        tasks = await get_reminder_by_datetime(user,time.time)
        return tasks
    
    except Exception as e:
        logging.error(f"Exception while getting reminder!: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete('/{user}/reminders/{task_id}',response_model=ReminderSchema,status_code=200)
async def delete_reminder(user:str=Path(...),task_id:str=Path(...))->ReminderSchema:
    try:
        res = await clear_reminder(user=user,task_id=task_id)
        status = res.get('success',None)
        if status == True:
            task = res.get('task')
            return task

    except Exception as e:
        logging.error(f"Error while deleting task! {e}")
        return {}