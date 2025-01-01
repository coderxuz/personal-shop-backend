import asyncio

from .app import dp, bot
from backend.common import logger

from .app.handlers import start
from bot.app.handlers import lang



async def main():
    logger.info("bot running")
    dp.include_router(start.router)
    dp.include_router(lang.router)
    await dp.start_polling(bot) #type:ignore

if __name__ =="__main__":
    asyncio.run(main())