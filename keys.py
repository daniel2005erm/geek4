from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

btn1 = [ 
    InlineKeyboardButton('номер', callback_data='nomer'),
    InlineKeyboardButton('местоположение', callback_data='mesto'),
    InlineKeyboardButton('еда', callback_data='eda')
]
button = InlineKeyboardMarkup().add(*btn1)

btn2 = [
    KeyboardButton('Подтвердите номер', request_contact=True)
]
nomer = ReplyKeyboardMarkup().add(*btn2)
btn3 = [
    KeyboardButton('Подтвердите местоположение', request_location=True)
]

mesto = ReplyKeyboardMarkup().add(*btn3)