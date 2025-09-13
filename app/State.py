from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Register(StatesGroup):
    citizenship = State()#гражданство
    age = State()#Возраст
    number = State()#Номер телефон
    after_work = State()#Раболи ли раньше в самокате
    medical_book = State()#Есть ли мед.книжка
    position_giving = State()#Место выдачи
    date_giving = State()#Дата выдачи
    date_birthday = State()#Дата рождения
    series_and_number = State()#Серия и номер
    photo_pasporta = State()#Первая страница паспорта
    position_registration = State()#Адрес регистрации
    photo_registration = State()#фото регистрации
    snils = State()#СНИЛС
    inn = State()#ИНН
    photo_snils = State()#фото снилс
    photo_inn = State()#фото инн
    photo_pact = State()#фото договора
    type_registration = State()#гпх или смз
    examination = State()
    proverka = State()
    correct_field = State()      
    correct_value = State()
    country = State()
    vacancy = State()
    type_vacancy = State()

