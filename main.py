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

async def keep_online():
    # Используем connect вместо start, чтобы не было запроса телефона в пустоту
    await client.connect()
    
    # Проверяем, авторизованы ли мы по строке SESSION
    if not await client.is_user_authorized():
        print("❌ ОШИБКА: SESSION не подходит или пуста!")
        print("Скрипт не может спросить телефон на сервере.")
        print("Пожалуйста, получи новую SESSION через get_session.py и вставь её в настройки Render.")
        return

    print("✅ Авторизация успешна! Держим онлайн...")
    while True:
        try:
            # Тот самый "хардкорный" метод с диалогами
            await client(functions.account.UpdateStatusRequest(offline=False))
            await client(functions.messages.GetDialogsRequest(
                offset_date=None, offset_id=0, 
                offset_peer=types.InputPeerEmpty(), limit=1, hash=0
            ))
            await asyncio.sleep(random.randint(15, 25))
        except Exception as e:
            print(f"Ошибка: {e}")
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

