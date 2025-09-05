import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from app.handlers_anketa import router as anketa_router  
from app.handlers_info import router as info_router 



async def main():
    bot = Bot(token='YOUR_TOKEN') 
    dp = Dispatcher()
    dp.include_router(anketa_router)
    dp.include_router(info_router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
