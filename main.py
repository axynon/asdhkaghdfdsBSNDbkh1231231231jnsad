import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateStatusRequest
from aiohttp import web

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def keep_online():
    await client.start()
    print("Скрипт авторизован. Начинаю удерживать онлайн...")
    
    while True:
        try:
            # 1. Отправляем явный запрос на обновление статуса
            await client(UpdateStatusRequest(offline=False))
            
            # 2. Делаем легкий запрос данных, чтобы сессия была активной
            await client.get_me()
            
            # Интервал 30 секунд гарантирует, что статус не успеет стать "был в сети"
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"Ошибка в цикле онлайна: {e}")
            await asyncio.sleep(10) # Быстрая попытка переподключения при сбое

async def handle(request):
    return web.Response(text="Сервер работает, онлайн удерживается.")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    # Запускаем фоновые задачи
    await asyncio.gather(
        web_server(),
        keep_online()
    )

if __name__ == "__main__":
    asyncio.run(main())
