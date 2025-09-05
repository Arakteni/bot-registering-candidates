from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Информация о работе')]],resize_keyboard = True)

btn_reg_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Доход'), KeyboardButton(text = 'График работы')],
                                          [KeyboardButton(text = 'Какой тип оформления')],
                                          [KeyboardButton(text = 'Вернуться к оформлению')],],resize_keyboard = True)

btn_country = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'РФ'), KeyboardButton(text = 'Другое')],
                                            ],resize_keyboard = True)

btn_age = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да'),KeyboardButton(text='Нет')],
                                        [KeyboardButton(text = 'Информация о работе')]],resize_keyboard = True)

btn_return = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Вернуться к оформлению')],
                                           [KeyboardButton(text = 'Вернуться к прошлому шагу')]], resize_keyboard = True)

btn_choice = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Информация о работе'), KeyboardButton(text = 'Начать оформление')]], resize_keyboard = True)


btn_correct = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Исправить данные'), Keyboardbutton(text = 'Всё верно')]])

btn_finish = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Проверить данные')]])

btn_end = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Завершить оформление')]])
