import asyncio
from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command
import app.keyboard as kb
from aiogram.fsm.state import State, StatesGroup
import app.State as st

router = Router()


@router.message(F.text == "1")
async def Citizenship(message: types.Message):
    await message.answer("Укажите ваше гражданство", reply_markup=kb.btn_country)

@router.message(F.text == "2")
async def Age(message: types.Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await state.set_state(st.Register.age)
    await message.answer("Введите ваш возраст", reply_markup=kb.btn_finish)

@router.message(F.text =="3")
async def Number(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    try:
        age_value = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст числом.", reply_markup=kb.btn_finish)
        return

    if age_value < 18:
        await message.answer("Извините, но мы не можем брать на работу несовершеннолетних")
    else:
        await state.set_state(st.Register.number)
        await message.answer("Введите ваш номер телефона", reply_markup=kb.btn_finish)

@router.message(F.text == "4")
async def After_work(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(st.Register.after_work)
    await message.answer("Работали ли вы раньше в самокате, если да, то какого числа была последняя смена?\nВ формате дд.мм.гг", reply_markup=kb.btn_finish)



def validate_date(input_date_str: str, date_format: str = "%d.%m.%y") -> dict:
    """
    Проверяет дату и возвращает детальную информацию.
    
    Returns:
        dict: {
            'is_valid': bool,
            'error_message': str or None,
            'days_passed': int or None,
            'is_31_days': bool or None
        }
    """
    try:
        # Преобразуем строку в объект datetime
        input_date = datetime.strptime(input_date_str, date_format)
        
        # Проверяем, что дата не в будущем
        current_date = datetime.now()
        if input_date > current_date:
            return {
                'is_valid': False,
                'error_message': "Дата не может быть в будущем!",
                'days_passed': None,
                'is_31_days': None
            }
        
        # Вычисляем разницу в днях
        time_difference = current_date - input_date
        days_passed = time_difference.days
        
        return {
            'is_valid': True,
            'error_message': None,
            'days_passed': days_passed,
            'is_31_days': days_passed >= 31
        }
        
    except ValueError:
        return {
            'is_valid': False,
            'error_message': "Неправильный формат даты! Используйте дд.мм.гг (например: 15.01.24)",
            'days_passed': None,
            'is_31_days': None
        }

@router.message(F.text == "5")
async def Medical_book(message: types.Message, state: FSMContext):
    user_date = message.text.strip()
    
    # Проверяем дату
    date_validation = validate_date(user_date)
    
    if not date_validation['is_valid']:
        await message.answer(date_validation['error_message'])
        return
    
    if not date_validation['is_31_days']:
        await message.answer(f"С указанной даты прошло только {date_validation['days_passed']} дней. Требуется не менее 31 дня.")
        return
    
    await state.update_data(after_work=message.text)
    await state.set_state(st.Register.medical_book)
    await message.answer("Есть ли у вас медицинская книжка?\nДля устройства она не требуется, но её нужно оформить в течении 14 дней после устройства на работу", reply_markup=kb.btn_finish)

@router.message(F.text == "6")  
async def Position_giving(message: types.Message, state: FSMContext):
    await state.update_data(medical_book=message.text)
    await state.set_state(st.Register.position_giving)
    await message.answer("Укажите место выдачи паспорта(также как написно в паспорте)", reply_markup=kb.btn_finish)

@router.message(F.text == "7")
async def Date_giving(message: types.Message, state: FSMContext):
    await state.update_data(position_giving=message.text)
    await state.set_state(st.Register.date_giving)
    await message.answer("Укажите дату выдачи паспорта(также как написано в паспорте) \nВ формате дд.мм.гг", reply_markup=kb.btn_finish)

@router.message(F.text == "8")
async def Date_birthday(message: types.Message, state: FSMContext):
    await state.update_data(date_giving=message.text)
    await state.set_state(st.Register.date_birthday)
    await message.answer("Укажите дату вашего рождения(также как написано в паспорте \nВ формате дд.мм.гг)", reply_markup=kb.btn_finish)

@router.message(F.text == "9")
async def Series_and_Number(message: types.Message, state: FSMContext):
    await state.update_data(date_birthday=message.text)
    await state.set_state(st.Register.series_and_number)
    await message.answer("Укажите серию и номер паспорта, также как написано в паспорте)", reply_markup=kb.btn_finish)

@router.message(F.text == "10")
async def Snils(message: types.Message, state: FSMContext):
    await state.update_data(series_and_number=message.text)
    await state.set_state(st.Register.snils)
    await message.answer("Введите номер снилса", reply_markup=kb.btn_finish)

@router.message(F.text == "11")
async def Inn(message: types.Message):
    await state.update_data(snils=message.text)
    await message.answer("Введите номер ИНН", reply_markup=kb.btn_finish)

@router.message(F.text == 'Проверить данные')
async def (message: types.Message, state: FSMContext):
    check_message = f'''Проверьте верно ли вы ввели свои данные:
    1. Гражданство: {citizenship}
    2. Возраст: {age}
    3. Номер телефона: {number}
    4. Последняя смена: {after_work}
    5. Мед. книжка: {medical_book}
    6. Место выдачи паспорта: {position_giving}
    7. Дата выдачи паспорта: {date_giving}
    8. Дата рождения: {date_birthday}
    9. Серия и номер паспорта: {series_and_number}
    10. СНИЛС: {snils}
    11. ИНН: {inn}
    Если какие-то данные не верны, то нажмите кнопку исправить данные и введите номер строки в которой хотите исправить данные
    '''

    await message.answer(check_message, reply_markup=kb.btn_correct)




