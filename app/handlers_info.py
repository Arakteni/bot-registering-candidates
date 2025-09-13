import asyncio
from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import app.keyboard as kb
import app.State as st
import pandas as pd

df = pd.read_csv('Ставки.csv')
df.set_index('Город', inplace=True)

router = Router()


@router.message(F.text.in_(["Информация о работе", "Вернуться к прошлому шагу"]))
async def Information_an_work(message: types.Message):
    await message.answer("Что именно вы хотите узнать, выберите раздел", reply_markup=kb.btn_reg_1)

@router.message(F.text == "Доход")
async def Country(message: types.Message, state: FSMContext):
    await state.set_state(st.Register.country)
    await message.answer('Напишите ваш город проживания\nУказываться должен город областного значения\nНапример город "Химки" входит в состав города Москва, значит нужно указать Москву', reply_markup=kb.btn_return)

@router.message(st.Register.country)
async def Vacancy(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(st.Register.vacancy)
    await message.answer("Укажите вашу вакансию", reply_markup=kb.btn_vacancy)

@router.message(st.Register.vacancy)
async def Type_vacancy(message: types.Message, state: FSMContext):
    await state.update_data(vacancy=message.text)
    await state.set_state(st.Register.type_vacancy)
    data = await state.get_data()
    country = data.get('country')
    vacancy = data.get('vacancy')
    if message.text == 'Сборщик-партнёр':
        rate = df.loc[country, vacancy]
        await message.answer(f'''У сборщиков-партнёров комбинированная оплата\n
Ставка-{rate} рублей в час + 1 рубль за каждую единицу товара
В час можно собирать от 100 единиц
Таким образом доход от {rate + 100} рублей в час''', reply_markup=kb.btn_main)
    else:
        await message.answer('Укажите тип вашей вакансии(пеший, вело, авто итд)', reply_markup=kb.btn_type_vacancy)

@router.message(st.Register.type_vacancy)
async def Return_profit(message: types.Message, state: FSMContext):
    await state.update_data(type_vacancy=message.text)
    data = await state.get_data()
    country = data.get('country')
    type_vacancy = data.get('type_vacancy')

    rate = df.loc[country, type_vacancy]
    rate2 = df.loc[country, type_vacancy+"-ближний"]
    rate3 = df.loc[country, type_vacancy+"-дальний"]
    await message.answer(f'''У курьеров-партнёров комбинированная оплата\n
Ставка в час-{rate} рублей
Ближний заказ(15 минут)-{rate2} рублей
Дальний заказ(30 минут)-{rate3} рублей
Таким образом доход за час от {rate + (rate2 * 3) + (rate3 * 2)} рублей''', reply_markup=kb.btn_main)
    await state.clear()

@router.message(F.text == "График работы")
async def Schedule(message: types.Message):
    await message.answer("График работы полностью свободный, в какие часы работать будете выбирать вы сами, с приложением вас познакомят после прохождения стажировки",reply_markup=kb.btn_return)

@router.message(F.text == "Какой тип оформления")
async def Type_design(message: types.Message):
    await message.answer('''ГПХ или СМЗ\n
ГПХ(Гражданско-Правовой Характер) — это вид договора, по которому одна сторона (исполнитель) обязуется выполнить конкретную работу или оказать услугу, а вторая сторона (заказчик) обязуется принять результат и оплатить его. Такой договор регулируется Гражданским кодексом и отличается от трудового договора тем, что не подразумевает официального трудоустройства и социальных гарантий в полном объеме, хотя по ГПХ работнику теперь полагаются выплаты больничных и пособий по уходу за ребенком.\n
СМЗ(Самозанятый) - это человек, который платит специальный налог на профессиональный доход (НПД). При этом не нужно дополнительно отчислять подоходный налог или налог на прибыль.
Неофициального или официального трудоустройства у нас нет\n
При банкротстве по ГПХ и СМЗ ваши доходы будут видны''', reply_markup=kb.btn_return)
                        
