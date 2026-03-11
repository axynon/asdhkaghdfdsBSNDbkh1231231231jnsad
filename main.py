import asyncio
import os
import random
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
from aiohttp import web

# Данные из Render
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def periodic_online_logic():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ ОШИБКА: SESSION невалидна. Проверь переменные в Render!")
        return

    print("✅ Скрипт авторизован. Переходим в режим периодического онлайна.")
    
    while True:
        try:
            # --- ФАЗА 1: ОФФЛАЙН ---
            # Спим от 10 до 20 минут (в секундах)
            sleep_time = random.randint(600, 1200) 
            print(f"💤 Уходим в оффлайн на {sleep_time // 60} минут...")
            await asyncio.sleep(sleep_time)

            # --- ФАЗА 2: ОНЛАЙН ---
            # Будем "в сети" от 2 до 4 минут
            online_duration = random.randint(120, 240)
            print(f"📱 Заходим в сеть на {online_duration} секунд...")
            
            end_time = asyncio.get_event_loop().time() + online_duration
            while asyncio.get_event_loop().time() < end_time:
                # Обновляем статус
                await client(functions.account.UpdateStatusRequest(offline=False))
                # Имитируем просмотр диалогов
                await client(functions.messages.GetDialogsRequest(
                    offset_date=None, offset_id=0, 
                    offset_peer=types.InputPeerEmpty(), limit=1, hash=0
                ))
                # Держим статус каждые 30 секунд внутри активной фазы
                await asyncio.sleep(30)
                
            print("🚶 Выходим из приложения...")
            # Явно говорим серверу, что мы оффлайн (по желанию)
            await client(functions.account.UpdateStatusRequest(offline=True))

        except Exception as e:
            print(f"⚠️ Ошибка в цикле: {e}")
            await asyncio.sleep(60)

async def handle(request):
    return web.Response(text="Бот имитирует периодический онлайн.")

async def main():
    # Запуск веб-сервера (обязательно для Render)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080))).start()

    # Запускаем логику
    await periodic_online_logic()

if __name__ == "__main__":
    asyncio.run(main())
