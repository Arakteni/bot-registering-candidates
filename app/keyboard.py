from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Информация о работе')]],resize_keyboard = True)

btn_reg_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Доход'), KeyboardButton(text = 'График работы')],
                                          [KeyboardButton(text = 'Какой тип оформления')],
                                          [KeyboardButton(text = 'Вернуться к оформлению')],],resize_keyboard = True)

btn_country = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'РФ'), KeyboardButton(text = 'Другое')]],
                                  resize_keyboard = True)

btn_age = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да'),KeyboardButton(text='Нет')],
                                        [KeyboardButton(text = 'Информация о работе')]],resize_keyboard = True)

btn_return = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Вернуться к оформлению')],
                                           [KeyboardButton(text = 'Вернуться к прошлому шагу')]], resize_keyboard = True)

btn_choice = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Информация о работе'), KeyboardButton(text = 'Начать оформление')]], resize_keyboard = True)


btn_correct = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Исправить данные'), 
                                               KeyboardButton(text = 'Всё верно')]],resize_keyboard = True)

btn_finish = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Проверить данные')]],resize_keyboard = True)

btn_end = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Завершить оформление')]],resize_keyboard = True)

btn_finish_country = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'РФ'), KeyboardButton(text = 'Другое')],
                                                                  [KeyboardButton(text = 'Проверить данные')]],resize_keyboard = True)

btn_gph_smz = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'ГПХ'), KeyboardButton(text = 'СМЗ')]],
                                  resize_keyboard = True)

btn_vacancy = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Курьер-партнёр'), KeyboardButton(text = 'Сборщик-партнёр')]],resize_keyboard = True)

btn_type_vacancy = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Вело'), KeyboardButton(text = 'Авто')],
                                                 [KeyboardButton(text = 'Мото'), KeyboardButton(text = 'Пеший')],
                                                 [KeyboardButton(text = 'Электровело')]],resize_keyboard = True)
