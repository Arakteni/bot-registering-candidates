import asyncio
from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command
import app.keyboard as kb
import app.State as st
import app.handlers_info as hf
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

router = Router()

@router.message(Command("start"))
async def Choice(message: types.Message):
    await message.reply("Здравствуйте, пройдите регистрацию")
    await message.answer('До начала оформления можете ознакомиться с "Информацией о работе", а также после оформления.\n'
                         'Во время оформления(заполнения анкеты) ознакомиться с "Информацией о работе" будет нельзя',
                         reply_markup=kb.btn_choice)

@router.message(F.text == "Начать оформление")
async def Citizenship(message: types.Message, state: FSMContext):
    await state.set_state(st.Register.citizenship)
    await message.answer("Укажите ваше гражданство", reply_markup=kb.btn_country)

@router.message(st.Register.citizenship)
async def Age(message: types.Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await state.set_state(st.Register.age)
    await message.answer("Введите ваш возраст")

@router.message(st.Register.age)
async def Number(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    try:
        age_value = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст числом.")
        return

    if age_value < 18:
        await message.answer("Извините, но мы не можем брать на работу несовершеннолетних")
    else:
        await state.set_state(st.Register.number)
        await message.answer("Введите ваш номер телефона")

@router.message(st.Register.number)
async def After_work(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(st.Register.after_work)
    await message.answer("Работали ли вы раньше в самокате, если да, то какого числа была последняя смена?\nВ формате дд.мм.гг")



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

@router.message(st.Register.after_work)
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
    await message.answer("Есть ли у вас медицинская книжка?\nДля устройства она не требуется, но её нужно оформить в течении 14 дней после устройства на работу")
@router.message(st.Register.medical_book)  
async def Position_giving(message: types.Message, state: FSMContext):
    await state.update_data(medical_book=message.text)
    await state.set_state(st.Register.position_giving)
    await message.answer("Укажите место выдачи паспорта(также как написно в паспорте)")

@router.message(st.Register.position_giving)
async def Date_giving(message: types.Message, state: FSMContext):
    await state.update_data(position_giving=message.text)
    await state.set_state(st.Register.date_giving)
    await message.answer("Укажите дату выдачи паспорта(также как написано в паспорте) \nВ формате дд.мм.гг")

@router.message(st.Register.date_giving)
async def Date_birthday(message: types.Message, state: FSMContext):
    await state.update_data(date_giving=message.text)
    await state.set_state(st.Register.date_birthday)
    await message.answer("Укажите дату вашего рождения(также как написано в паспорте \nВ формате дд.мм.гг)")

@router.message(st.Register.date_birthday)
async def Series_and_Number(message: types.Message, state: FSMContext):
    await state.update_data(date_birthday=message.text)
    await state.set_state(st.Register.series_and_number)
    await message.answer("Укажите серию и номер паспорта, также как написано в паспорте)")

@router.message(st.Register.series_and_number)
async def Snils(message: types.Message, state: FSMContext):
    await state.update_data(series_and_number=message.text)
    await state.set_state(st.Register.snils)
    await message.answer("Введите номер снилса")

@router.message(st.Register.snils)
async def Photo_snils(message: types.Message, state: FSMContext):
    await state.update_data(snils=message.text)
    await state.set_state(st.Register.photo_snils)
    await message.answer("Теперь отправьте фото СНИЛС (лицевая сторона)")

@router.message(st.Register.photo_snils)
async def Inn(message: types.Message, state: FSMContext):
    # Проверяем, что сообщение содержит фото
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию СНИЛС.")
        return
    
    try:
        # Получаем самое качественное фото
        photo = message.photo[-1]
        file_id = photo.file_id
        
        # Сохраняем file_id в состоянии
        await state.update_data(photo_snils_file_id=file_id)
        
        # Переходим к следующему шагу - ИНН
        await state.set_state(st.Register.inn)
        await message.answer("Теперь введите номер ИНН (текстом)")
        
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")

@router.message(st.Register.inn)
async def Photo_inn(message: types.Message, state: FSMContext):
    inn_text = message.text.strip()
    
    # Простая валидация ИНН (12 цифр для физлица)
    if not inn_text.isdigit() or len(inn_text) != 12:
        await message.answer("ИНН должен состоять из 12 цифр. Пожалуйста, введите корректный ИНН:")
        return
    
    await state.update_data(inn=inn_text)
    await state.set_state(st.Register.photo_inn)
    await message.answer("Теперь отправьте фото ИНН")


@router.message(st.Register.photo_inn)
async def handle_inn_photo(message: types.Message, state: FSMContext):
    # Проверяем, что сообщение содержит фото
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию ИНН.")
        return
    
    try:
        # Получаем самое качественное фото
        photo = message.photo[-1]
        file_id = photo.file_id
        
        # Сохраняем file_id в состоянии
        await state.update_data(photo_inn_file_id=file_id)
        
        # Получаем ВСЕ данные из состояния
        user_data = await state.get_data()
        # Завершаем FSM
        await state.clear()
        # Формируем сообщение с проверкой данных
        check_message = f'''Проверьте верно ли вы ввели свои данные:

1. Гражданство: {user_data.get('citizenship', 'не указано')}
2. Возраст: {user_data.get('age', 'не указан')}
3. Номер телефона: {user_data.get('number', 'не указан')}
4. Последняя смена: {user_data.get('after_work', 'не указана')}
5. Мед. книжка: {user_data.get('medical_book', 'не указана')}
6. Место выдачи паспорта: {user_data.get('position_giving', 'не указано')}
7. Дата выдачи паспорта: {user_data.get('date_giving', 'не указана')}
8. Дата рождения: {user_data.get('date_birthday', 'не указана')}
9. Серия и номер паспорта: {user_data.get('series_and_number', 'не указаны')}
10. СНИЛС: {user_data.get('snils', 'не указан')}
11. ИНН: {user_data.get('inn', 'не указан')}
Если какие-то данные не верны, то нажмите кнопку исправить данные и введите номер строки в которой хотите исправить данные
'''

        await message.answer(check_message, reply_markup=kb.btn_correct)
        
        
        
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")

@router.message(F.text == 'Всё верно')
async def Finish(message: types.Message):
    await message.answer(reply_markup=kb.btn_end)




