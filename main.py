import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.updates import GetStateRequest

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def keep_online():
    while True:
        try:
            if not client.is_connected():
                print("Connecting...")
                await client.connect()

            await client(GetStateRequest())
            print("Still online")

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(60)

async def main():
    await client.start()
    print("Client started")
    await keep_online()

asyncio.run(main())
