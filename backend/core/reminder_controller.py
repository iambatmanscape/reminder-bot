from datetime import datetime
from typing import List,Optional
from models import Reminder


async def save_or_update_reminder(
    reminders: List[str],
    user: str,
    time: Optional[datetime] = None,
    old_task_id: Optional[str] = None,
):
    """
    Creates a new reminder or updates an existing one.

    Args:
        reminders (List[str]): List of reminders to add.
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
        if old_task_id:
            # Update existing reminder
            task = await Reminder.find(
                Reminder.user == user,
                Reminder.task_id == old_task_id
            ).first_or_none()

            if task is None:
                raise Exception("Reminder not found.")

            task.reminder.extend(reminders)
            await task.save()
            await task.sync()
            return {"success": True, "task_id": task.task_id}

        else:
            # Create new reminder
            if not time:
                raise ValueError("Time is required to create a new reminder.")

            task_id = str(hash(time))
            remind = Reminder(reminder=reminders, time=time, task_id=task_id, user=user)
            await remind.save()
            await remind.sync()
            return {"success": True, "task_id": task_id}

    except Exception as e:
        raise Exception(f"Reminder save/update error: {e}")


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
            Reminder.user == user,
            Reminder.task_id == task_id
        )
        if task:
            await task.delete()
            return {'success':True,'task':task}
        return None
    except Exception as e:
        raise Exception(f"Delete Error: {e}")
