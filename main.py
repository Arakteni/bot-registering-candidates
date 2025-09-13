import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from app.handlers_anketa_ru import router as anketa_router  
from app.handlers_info import router as info_router 


load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN) 
    dp = Dispatcher()
    dp.include_router(anketa_router)
    dp.include_router(info_router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
