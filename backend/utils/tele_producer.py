from dotenv import load_dotenv
import aio_pika
from pika.exceptions import ChannelError
import json
from typing import Dict, Any
from os import getenv


async def send_reminder(user_id: str, description: str) -> Dict[str, Any]:
    """
    Sends a reminder to the telegram API

    Parameters:
        user_id (str): The unique identifier for the user.
        description (str): The reminder text.

    Returns:
        dict: JSON response from the backend API.

    Raises:
        aiohttp.ClientError: For HTTP-related errors during the request.
    """
    try:
        if not description:
            return {
                "message": "Description missing"
            }
        
        payload = {
            "user_id":user_id,
            "reminder":description
        }

        message = json.dumps(payload).encode()
        connection = await aio_pika.connect_robust(getenv('rabbit_url'))

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue('reminders',durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message),
                routing_key=queue.name
            )

            return {
                "message": "Saved to queue"
            }

    except ChannelError as ce:
        raise ChannelError(f"Connection request failed: {ce}") from ce
            

if __name__ == "__main__":
    import asyncio
    async def main():
        res = await send_reminder('1245','Jogging')
        print(res)
    asyncio.run(main())