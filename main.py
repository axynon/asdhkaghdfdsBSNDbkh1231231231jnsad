import asyncio
import os
import random
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
from aiohttp import web

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def keep_online_hardcore():
    await client.connect()
    if not await client.is_user_authorized():
        print("Сессия невалидна!")
        return

    print("Режим 'Бетонный онлайн' запущен...")
    
    while True:
        try:
            # 1. Основной сигнал онлайна
            await client(functions.account.UpdateStatusRequest(offline=False))
            
            # 2. Имитация открытия списка чатов (очень важно!)
            # Запрашиваем только 1 последний диалог, чтобы не нагружать сеть
            await client(functions.messages.GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=types.InputPeerEmpty(),
                limit=1,
                hash=0
            ))

            # 3. Случайная пауза, чтобы не выглядеть как робот
            wait_time = random.randint(15, 25)
            await asyncio.sleep(wait_time)
            
        except Exception as e:
            print(f"Ошибка активности: {e}")
            await asyncio.sleep(30)

async def handle(request):
    return web.Response(text="Online script is running...")

async def main():
    # Запуск веб-сервера для Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(runner, '0.0.0.0', port).start()

    # Запускаем цикл активности
    await keep_online_hardcore()

if __name__ == "__main__":
    asyncio.run(main())
