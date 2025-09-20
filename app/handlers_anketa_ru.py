import asyncio
from aiogram import types, Router, F, Bot
from aiogram.filters import Command
import app.keyboard as kb
import app.State as st
from aiogram.fsm.context import FSMContext
from datetime import datetime
import re
from dotenv import load_dotenv
import os
router = Router()

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID_Andrey")

FIELD_MAPPING = {
    '1': ('citizenship', "Укажите ваше гражданство", kb.btn_country),
    '2': ('age', "Введите ваш возраст", None),
    '3': ('number', "Введите ваш номер телефона", None),
    '4': ('after_work', "Введите дату последней смены (дд.мм.гг)", None),
    '5': ('medical_book', "Есть ли у вас медицинская книжка?", None),
    '6': ('position_giving', "Укажите место выдачи паспорта", None),
    '7': ('date_giving', "Укажите дату выдачи паспорта (дд.мм.гг)", None),
    '8': ('date_birthday', "Укажите дату рождения (дд.мм.гг)", None),
    '9': ('series_and_number', "Укажите серию и номер паспорта", None),
    '10': ('snils', "Введите номер СНИЛС", None),
    '11': ('inn', "Введите номер ИНН", None),
}

@router.message(Command("start"))
async def Choice(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == ADMIN_ID:
        await message.answer("Новых данных пока что нет")
    else:
        await message.reply("Здравствуйте, пройдите регистрацию")
        await message.answer('До начала оформления можете ознакомиться с "Информацией о работе", а также после оформления.\n'
                         'Во время оформления(заполнения анкеты) ознакомиться с "Информацией о работе" будет нельзя',
                         reply_markup=kb.btn_choice)
        

@router.message(F.text.in_(["Начать оформление", "Вернуться к оформлению"]))
async def Citizenship(message: types.Message, state: FSMContext):
    await state.set_state(st.Register.citizenship)
    await message.answer("Укажите ваше гражданство", reply_markup=kb.btn_country)

@router.message(st.Register.citizenship)
async def Age(message: types.Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    if message.text == 'Другое':
        await message.answer('Пока что я умею оформлять только граждан РФ')
    else:
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
    await message.answer('''Работали ли вы раньше в самокате, если да, то какого числа была последняя смена?\nВ формате дд.мм.гг\nЕсли вы не работали, то укажите "Не было смен"''', reply_markup=kb.btn_not_work)



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
        input_date = datetime.strptime(input_date_str, date_format)
        
        current_date = datetime.now()
        if input_date > current_date:
            return {
                'is_valid': False,
                'error_message': "Дата не может быть в будущем!",
                'days_passed': None,
                'is_31_days': None
            }
        
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
    if message.text == 'Не было смен':
        await state.update_data(after_work=message.text)
        await state.set_state(st.Register.medical_book)
        await message.answer("Есть ли у вас медицинская книжка?\nДля устройства она не требуется, но её нужно оформить в течении 14 дней после устройства на работу")

    else:
        date_validation = validate_date(user_date)
        
        if not date_validation['is_valid']:
            await message.answer(date_validation['error_message'])
            return
        
        if not date_validation['is_31_days']:
            await message.answer(f"С указанной даты прошло только {date_validation['days_passed']} дней. Требуется не менее 31 дня.")
            return
        else:
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
    await message.answer("Укажите дату вашего рождения(также как написано в паспорте) \nВ формате дд.мм.гг")

@router.message(st.Register.date_birthday)
async def Series_and_Number(message: types.Message, state: FSMContext):
    await state.update_data(date_birthday=message.text)
    await state.set_state(st.Register.series_and_number)
    await message.answer("Укажите серию и номер паспорта, (также как написано в паспорте)")

@router.message(st.Register.series_and_number)
async def Photo_pasporta(message: types.Message, state: FSMContext):
    await state.update_data(series_and_number=message.text)
    await state.set_state(st.Register.photo_pasporta)
    await message.answer("Теперь отправьте фото 1 страницы паспорта")

@router.message(st.Register.photo_pasporta)
async def Position_regestration(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию 1 страницы паспорта .")
        return
    
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        
        await state.update_data(photo_pasporta_file_id=file_id)
        
        
        await state.set_state(st.Register.position_registration)
        await message.answer("Введите адрес регистрации также как написано в паспорте")
        
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")

@router.message(st.Register.position_registration)
async def Photo_registration(message: types.Message, state: FSMContext):
    await state.update_data(position_registration=message.text)
    await state.set_state(st.Register.photo_registration)
    await message.answer("Теперь отправьте фото паспорта с адресом регистрации(пропиской)")

@router.message(st.Register.photo_registration)
async def Snils(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте паспорта с адресом регистрации(пропиской) .")
        return
    
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        
        await state.update_data(photo_registration_file_id=file_id)
        
        
        await state.set_state(st.Register.snils)
        await message.answer("Введите номер СНИЛС")
        
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")


@router.message(st.Register.snils)
async def Photo_snils(message: types.Message, state: FSMContext):
    await state.update_data(snils=message.text)
    await state.set_state(st.Register.photo_snils)
    await message.answer("Теперь отправьте фото СНИЛС (лицевая сторона)")

@router.message(st.Register.photo_snils)
async def Inn(message: types.Message, state: FSMContext):
    
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию СНИЛС.")
        return
    
    try:

        photo = message.photo[-1]
        file_id = photo.file_id
        

        await state.update_data(photo_snils_file_id=file_id)
        
        await state.set_state(st.Register.inn)
        await message.answer("Теперь введите номер ИНН (текстом)")
        
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")

@router.message(st.Register.inn)
async def Photo_inn(message: types.Message, state: FSMContext):
    inn_text = message.text.strip()
    
    if not inn_text.isdigit() or len(inn_text) != 12:
        await message.answer("ИНН должен состоять из 12 цифр. Пожалуйста, введите корректный ИНН:")
        return
    
    await state.update_data(inn=inn_text)
    await state.set_state(st.Register.photo_inn)
    await message.answer("Теперь отправьте фото ИНН")

@router.message(st.Register.photo_inn)
async def handle_inn_photo(message: types.Message, state: FSMContext):

    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию ИНН.")
        return
    
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        

        await state.update_data(photo_inn_file_id=file_id)
        await state.set_state(st.Register.type_registration)
        await message.answer("Вы хотите оформиться по гпх или смз?\nПри гпх налоги платит компания\nПри смз налоги платите вы\nНа доход это не влияет", reply_markup=kb.btn_gph_smz)
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")


@router.message(st.Register.type_registration)        
async def Type_registration(message: types.Message, state: FSMContext):
    await state.update_data(type_registration=message.text)
    await state.set_state(st.Register.photo_pact)
    if message.text == "ГПХ":
        await message.answer('''Если вы устраиваетесь как Физ.Лицо, то переходите по реферальной ссылке и проходите регистрацию - https://work.jump.finance/registrations/e4d8d3df-fdba-45d7-a2f6-60b24525f453
Пройдите регистрацию, скачайте приложение "Jump.работа" и пришлите скриншот подписанного в этом договора.Затем я создам  учетную запись по Вашим  данным  для входа в рабочее приложение Узнай Про.''')
    elif message.text == "СМЗ":
        await message.answer('''Если вы устраиваетесь , как Самозанятый, то переходите по реферальной ссылке и завершайте регистрацию - https://work.jump.finance/registrations/9e8fd9f1-2471-4193-88b9-6bb294f951b0
Пройдите регистрацию, скачайте приложение "Jump.работа" и пришлите скриншот подписанного договора.Затем я создам  учетную запись по Вашим  данным  для входа в рабочее приложение Узнай Про.''')
        
@router.message(st.Register.photo_pact)
async def End_registration(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фотографию подписанного договора.")
        return
    
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        

        await state.update_data(photo_pact_file_id=file_id)
        await state.set_state(st.Register.examination)

        user_data = await state.get_data()

        await message.answer("Все нужные документы прикреплены. Проверьте свои данные перед отправкой", reply_markup=kb.btn_finish)
        
    except Exception as e:
        await message.answer("Ошибка при обработке фото. Попробуйте отправить фото еще раз.")

    
@router.message(st.Register.examination) 
async def Proverka(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
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

Если какие-то данные не верны, нажмите "Исправить данные"
Если все верно, нажмите "Всё верно"
'''
    await state.set_state(None)
    await message.answer(check_message, reply_markup=kb.btn_correct)

@router.message(F.text == 'Исправить данные')
async def correct_data(message: types.Message, state: FSMContext):
    await message.answer("Введите номер поля, которое хотите исправить (1-11):\n\n"
                      "1. Гражданство\n2. Возраст\n3. Номер телефона\n4. Последняя смена\n"
                      "5. Мед. книжка\n6. Место выдачи паспорта\n7. Дата выдачи паспорта\n"
                      "8. Дата рождения\n9. Серия и номер паспорта\n10. СНИЛС\n11. ИНН")
    await state.set_state(st.Register.correct_field)

@router.message(st.Register.correct_field)
async def handle_field_selection(message: types.Message, state: FSMContext):
    field_number = message.text.strip()
    
    if field_number not in FIELD_MAPPING:
        await message.answer("Пожалуйста, введите число от 1 до 12:")
        return
    
    field_name, prompt_text, keyboard = FIELD_MAPPING[field_number]
    await state.update_data(correcting_field=field_name)
    
    if keyboard:
        await message.answer(prompt_text, reply_markup=keyboard)
    else:
        await message.answer(prompt_text)
    
    await state.set_state(st.Register.correct_value)

@router.message(st.Register.correct_value)
async def handle_correct_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    field_name = user_data.get('correcting_field')
    new_value = message.text
    
    if field_name == 'age':
        try:
            age_value = int(new_value)
            if age_value < 18:
                await message.answer("Возраст должен быть не менее 18 лет. Введите корректный возраст:")
                return
        except ValueError:
            await message.answer("Пожалуйста, введите корректный возраст числом:")
            return
    
    elif field_name in ['after_work', 'date_giving', 'date_birthday']:
        validation = validate_date(new_value)
        if not validation['is_valid']:
            await message.answer(validation['error_message'])
            return
        
        if field_name == 'after_work' and not validation['is_31_days']:
            await message.answer(f"С указанной даты прошло только {validation['days_passed']} дней. Требуется не менее 31 дня.")
            return
    
    elif field_name == 'inn':
        if not new_value.isdigit() or len(new_value) != 12:
            await message.answer("ИНН должен состоять из 12 цифр. Пожалуйста, введите корректный ИНН:")
            return
    
    await state.update_data({field_name: new_value})
    await state.update_data(correcting_field=None)
    
    await message.answer("✅ Данные успешно обновлены!")
    
    await Proverka(message, state)
    await state.set_state(None)

@router.message(F.text == 'Всё верно')
async def Send_to_admin(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()

    check_message = f'''
Новая анкета от пользователя @{message.from_user.username}:
1. Гражданство: {user_data.get('citizenship', '❌ НЕ УКАЗАНО')}
2. Возраст: {user_data.get('age', '❌ НЕ УКАЗАН')}
3. Номер телефона: {user_data.get('number', '❌ НЕ УКАЗАН')}
4. Последняя смена: {user_data.get('after_work', '❌ НЕ УКАЗАНА')}
5. Мед. книжка: {user_data.get('medical_book', '❌ НЕ УКАЗАНА')}
6. Место выдачи паспорта: {user_data.get('position_giving', '❌ НЕ УКАЗАНО')}
7. Дата выдачи паспорта: {user_data.get('date_giving', '❌ НЕ УКАЗАНА')}
8. Дата рождения: {user_data.get('date_birthday', '❌ НЕ УКАЗАНА')}
9. Серия и номер паспорта: {user_data.get('series_and_number', '❌ НЕ УКАЗАНЫ')}
10. СНИЛС: {user_data.get('snils', '❌ НЕ УКАЗАН')}
11. ИНН: {user_data.get('inn', '❌ НЕ УКАЗАН')}
12. Тип договора: {user_data.get('type_registration', '❌ НЕ УКАЗАН')}
'''

    try:
        await bot.send_message(ADMIN_ID, check_message)
        print("✅ Текстовое сообщение отправлено админу")

        photo_map = {
            "Фото паспорта (1 стр.)": user_data.get('photo_pasporta_file_id'),
            "Фото регистрации": user_data.get('photo_registration_file_id'), 
            "Фото СНИЛС": user_data.get('photo_snils_file_id'),
            "Фото ИНН": user_data.get('photo_inn_file_id'),
            "Фото договора": user_data.get('photo_pact_file_id')
        }

        for name, photo_id in photo_map.items():
            if photo_id:
                try:
                    await bot.send_photo(ADMIN_ID, photo=photo_id)
                    print(f"✅ Отправлено: {name}")
                except Exception as e:
                    print(f"❌ Ошибка отправки {name}: {e}")
            else:
                print(f"⚠️ Пропущено: {name} — file_id отсутствует!")

        await message.answer("✅ Ваша анкета успешно отправлена на проверку!", reply_markup = kb.btn_main)

    except Exception as e:
        error_msg = f"❌ Ошибка при отправке анкеты: {e}"
        await message.answer(error_msg)
        print(error_msg)

    finally:
        await state.clear()