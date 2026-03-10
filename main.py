import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateStatusRequest
from aiohttp import web

# Получаем данные из переменных окружения
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

# Создаем клиента (но пока не запускаем цикл)
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def keep_online():
    await client.start()
    print("Вечный онлайн успешно запущен!")
    while True:
        try:
            # Статус "Online"
            await client(UpdateStatusRequest(offline=False))
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Ошибка в ТГ: {e}")
            await asyncio.sleep(60)

async def handle(request):
    return web.Response(text="Бот активен и держит онлайн!")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

async def main():
    # Запускаем всё внутри одного асинхронного контекста
    await asyncio.gather(
        web_server(),
        keep_online()
    )

if __name__ == "__main__":
    # Правильный запуск для новых версий Python
    asyncio.run(main())
