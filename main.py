import asyncio
import os
import random
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
from aiohttp import web

# Берем данные из переменных Render
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def periodic_online():
    print("🤖 Запуск цикличного режима...")
    while True:
        try:
            # Проверяем подключение
            if not client.is_connected():
                await client.connect()
            
            if not await client.is_user_authorized():
                print("❌ Ошибка: Сессия SESSION не подходит!")
                return

            # ФАЗА: ОНЛАЙН (зашли на 2-3 минуты)
            online_time = random.randint(120, 180)
            print(f"📱 Зашли в сеть на {online_time} сек.")
            
            start_mark = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_mark < online_time:
                await client(functions.account.UpdateStatusRequest(offline=False))
                # Имитируем легкую активность
                await client.get_me() 
                await asyncio.sleep(30)

            # ФАЗА: ОФФЛАЙН (ушли на 10-15 минут)
            await client(functions.account.UpdateStatusRequest(offline=True))
            # Отключаемся, чтобы не висеть мертвым грузом
            await client.disconnect()
            
            wait_time = random.randint(600, 900)
            print(f"💤 Ушли в оффлайн на {wait_time // 60} мин.")
            await asyncio.sleep(wait_time)

        except Exception as e:
            print(f"⚠️ Ошибка: {e}. Перезапуск через минуту...")
            await asyncio.sleep(60)

async def handle(request):
    return web.Response(text="Скрипт периодического онлайна активен.")

async def main():
    # 1. Запускаем веб-сервер для Render (чтобы не было ошибок порта)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Веб-сервер готов на порту {port}")

    # 2. Запускаем основной цикл
    await periodic_online()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        
