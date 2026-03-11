import asyncio
import os
import random
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from aiohttp import web

# Данные из Render
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 1. ОБЯЗАТЕЛЬНО: Слушаем любые события (это открывает постоянный поток данных)
@client.on(events.NewMessage)
async def handler(event):
    pass # Мы просто слушаем, ничего не делаем

async def keep_online_ultimate():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ ОШИБКА: Сессия невалидна. Обнови SESSION!")
        return

    print("🚀 Запущен режим 'Real Device Emulation'...")
    
    while True:
        try:
            # Имитируем активность "зашел в приложение"
            async with client.action(types.InputPeerEmpty(), 'typing'):
                # Обновляем основной статус
                await client(functions.account.UpdateStatusRequest(offline=False))
                
                # Запрашиваем конфигурацию (как это делает приложение при старте)
                await client(functions.help.GetConfigRequest())
                
                # Запрашиваем состояние уведомлений
                await client(functions.account.GetNotifySettingsRequest(
                    peer=types.InputNotifyUsers()
                ))

            # Ждем рандомное время
            await asyncio.sleep(random.randint(20, 40))
            
        except Exception as e:
            print(f"Ошибка активности: {e}")
            await asyncio.sleep(20)

async def handle(request):
    return web.Response(text="Система эмуляции активна")

async def main():
    # Запуск веб-заглушки для Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080))).start()

    # Запускаем фоновый цикл и режим прослушивания
    await asyncio.gather(
        keep_online_ultimate(),
        client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())
