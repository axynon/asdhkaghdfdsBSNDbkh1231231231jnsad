import os
import asyncio
from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.functions.updates import GetStateRequest

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session = os.environ.get("SESSION")

client = TelegramClient(session, api_id, api_hash)

async def keep_online():
    while True:
        try:
            if not client.is_connected():
                print("Connecting to Telegram...")
                await client.connect()

            print("Online...")
            await client(GetStateRequest())

        except RPCError as e:
            print("Telegram RPC error:", e)

        except Exception as e:
            print("Connection error:", e)

        await asyncio.sleep(60)

async def main():
    await client.start()
    print("Client started")
    await keep_online()

while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print("Restarting script due to:", e)
        asyncio.sleep(5)
