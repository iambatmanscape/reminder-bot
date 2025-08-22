from datetime import datetime
from typing import List,Optional
from backend.models import Reminder
from backend.core import scheduler
from backend.utils.tele_producer import send_reminder
from uuid import uuid4
from dateutil import parser
import logging
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import getenv


async def save_or_update_reminder(
    reminders: str,
    user: str,
    time: Optional[datetime] = None,
    old_task_id: Optional[str] = None,
):
    """
    Creates a new reminder or updates an existing one.

    Args:
        reminders (str): Reminders to add.
        user (str): User ID.
        time (Optional[datetime]): Time for the new reminder. Required if creating.
        old_task_id (Optional[str]): Task ID of an existing reminder to update.

    Returns:
        dict: {
            "success": True,
            "task_id": str
        }
    """
    try:
        
        task = await Reminder.find(
            {"user": user, "task_id": old_task_id}
        ).first_or_none()

        if task:
            task.reminder.extend(reminders)
            await task.save()
            await task.sync()
            return {"success": True, "task_id": task.task_id}

        # Create new reminder
        if not time:
            raise ValueError("Time is required to create a new reminder.")

        id = str(uuid4())
        task_id = ''.join(id.split('-'))
        remind = Reminder(reminder=reminders, time=time, task_id=task_id, user=user)
        scheduler.add_job(send_reminder, args=[user, reminders], trigger="date", run_date=time, id=task_id, jobstore=getenv('jobstore'))
        await remind.save()
        await remind.sync()
        return {"success": True, "task_id": task_id}

    except Exception as e:
        logging.error(f"Error: {e}")
        raise Exception(f"Reminder save/update error: {e}")


# Get all reminders from a user
async def get_reminders(user: str):
    """
    Retrieve all reminders for a given user.

    Args:
        user (str): The unique identifier of the user whose reminders are to be retrieved.

    Returns:
        List[Reminder]: A list of Reminder objects associated with the user.

    Raises:
        Exception: If there is an error during database retrieval.
    """
    try:
        tasks = await Reminder.find(
            Reminder.user == user
        ).to_list()
        
        return tasks
    
    except Exception as e:
        logging.error(f"Error while getting reminders: {e}")
        raise Exception(f"Reminder listing error: {e}")


async def get_reminder_by_datetime(user: str, time: datetime):
    """
    Retrieve reminders for a given user scheduled at a specific datetime.

    Args:
        user (str): The unique identifier of the user.
        time (datetime): The exact datetime to filter reminders by.

    Returns:
        List[Reminder]: A list of Reminder objects matching the given datetime for the user.

    Raises:
        Exception: If there is an error during database retrieval.
    """
    try:
        tasks = await Reminder.find(
            Reminder.user == user,
            Reminder.time == time
        ).to_list()

        return tasks
    
    except Exception as e:
        logging.error(f"Error while getting reminder: {e}")
        raise Exception(f"Reminder error: {e}")


# Delete a reminder
async def clear_reminder(user: str, task_id: str):
    """
    Deletes a reminder based on user and time.

    Args:
        user (str): User ID.
        task_time (id): ID of the reminder.

    Returns:
        Optional[Reminder]: The deleted reminder object or None.
    """
    try:
        task = await Reminder.find_one(
            {"user": user, "task_id": task_id}
        )
        if task:
            await task.delete()
            return {'success':True,'task':task}
        return None
    except Exception as e:
        raise Exception(f"Delete Error: {e}")
