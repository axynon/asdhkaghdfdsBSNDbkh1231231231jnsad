import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateStatusRequest
from aiohttp import web

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

if not API_ID or not API_HASH or not SESSION:
    print("❌ ОШИБКА: Не заполнены API_ID, API_HASH или SESSION!")
    sys.exit(1)

client = TelegramClient(StringSession(SESSION), int(API_ID), API_HASH)

async def ping_online():
    """Фоновая задача, которая регулярно бьет в API"""
    while True:
        try:
            if client.is_connected():
                # Отправляем статус "в сети"
                await client(UpdateStatusRequest(offline=False))
        except Exception as e:
            print(f"Ошибка пинга: {e}")
        # Пингуем каждые 15 секунд для надежности
        await asyncio.sleep(15)

async def handle(request):
    return web.Response(text="Сервер работает, онлайн удерживается.")

async def main():
    # 1. Запускаем веб-сервер для Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print("🌐 Веб-сервер запущен!")

    # 2. Подключаемся к Telegram
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ ОШИБКА: Сессия недействительна!")
        return

    # 3. Запускаем параллельную задачу пинга (она будет работать в фоне)
    asyncio.create_task(ping_online())

    # 4. САМОЕ ВАЖНОЕ: Говорим библиотеке активно "слушать" сервер.
    # Это действие держит сокет открытым, и Telegram видит, что приложение "запущено".
    print("✅ Успешная авторизация! Режим вечного онлайна активирован.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Запуск для современных версий Python
    asyncio.run(main())
