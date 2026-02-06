# Главный файл бота PlusTim
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
import database
import handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Запуск бота"""
    # Инициализация бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    
    # Инициализация диспетчера
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(handlers.router)
    
    # Инициализация базы данных
    logger.info("📦 Инициализация базы данных...")
    db = await database.init_database()
    await database.close_database(db)
    logger.info("✅ База данных готова!")
    
    # Инициализация планировщика (опционально)
    scheduler = AsyncIOScheduler()
    
    # Пример задачи: ежедневное уведомление (раскомментировать при необходимости)
    # async def daily_reminder():
    #     await bot.send_message(CHAT_ID, "🌅 Доброе утро! Готов к новому уроку?")
    # 
    # scheduler.add_job(daily_reminder, 'cron', hour=9, minute=0)
    # scheduler.start()
    
    # Запускpolling
    logger.info("🚀 Запуск бота PlusTim...")
    logger.info("👋 Отправь /start чтобы начать!")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("🔒 Бот остановлен")


if __name__ == "__main__":
    # Проверка токена
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("""
⚠️  ВНИМАНИЕ! Не забудь указать BOT_TOKEN!

1. Создай файл .env в папке plus_tim
2. Добавь строку: BOT_TOKEN=твой_токен_бота_от_@BotFather
3. Или измени значение в config.py

Как получить токен:
1. Напиши @BotFather в Telegram
2. Отправь /newbot
3. Следуй инструкциям
4. Скопируй токен и вставь сюда
        """)
    else:
        asyncio.run(main())