import asyncio
from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command
import app.keyboard as kb

router = Router()

@router.message(F.text.in_(["Информация о работе", "Вернуться к прошлому шагу"]))
async def Information_an_work(message: types.Message):
    await message.answer("Что именно вы хотите узнать, выберите раздел", reply_markup=kb.btn_reg_1)

@router.message(F.text == "Доход")
async def Income(message: types.Message):
    await message.answer('Напишите вашу область(Например город "Химки" входит в "Московскую область")///пока что тупиковый вопрос', reply_markup=kb.btn_return)

@router.message(F.text == "График работы")
async def Schedule(message: types.Message):
    await message.answer("График работы полностью свободный, в какие часы работать будете выбирать вы сами, с приложением вас познакомят после прохождения стажировки",reply_markup=kb.btn_return)

@router.message(F.text == "Какой тип оформления")
async def Type_design(message: types.Message):
    await message.answer("Гпх или смз", reply_markup=kb.btn_return)


