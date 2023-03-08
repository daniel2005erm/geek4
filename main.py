from aiogram import Bot,Dispatcher,types,executor
from dotenv import load_dotenv
from spisok import Dp
from keys import button, nomer, mesto
import os, time , logging

db = Dp()
connect = db.connect
db.connect_db()

load_dotenv('.env')

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Здраствуйте {message.from_user.full_name}")
    await message.answer(f"я ваш официант вот мои команды",reply_markup=button)
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM customers WHERE user_id = {message.from_user.id};')
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"INSERT INTO customers VALUES ('{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.id}', 'None');")
    connect.commit()

@dp.callback_query_handler(lambda call : call)
async def inline(call):
    if call.data == 'nomer':
        await daypozvonity(call.message)
    elif call.data == 'mesto':
        await pikitochenye(call.message)
    elif call.data == 'eda':
        await vkusnozaybal(call.message)

@dp.message_handler(commands='number')
async def daypozvonity(message:types.Message):
    await message.answer('Подтвердите отправку своего номера.', reply_markup=nomer)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def pozvonitesty(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"UPDATE customers SET phone_number = '{message.contact['phone_number']}' WHERE user_id = {message.from_user.id};")
    connect.commit()
    await message.answer("Ваш номер успешно добавлен.")

@dp.message_handler(commands='location')
async def pikitochenye(message:types.Message):
    await message.answer("Подтвердите отправку местоположения.", reply_markup=mesto)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def skagigdetygivyshy(message:types.Message):
    await message.answer("Ваш адрес записан.")
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO address VALUES ('{message.from_user.id}', '{message.location.longitude}', '{message.location.latitude}');")
    connect.commit()

@dp.message_handler(commands='eda')
async def vkusnozaybal(message:types.Message):
    await message.reply(f"так {message.from_user.first_name} зайбал выбери то что у нас осталось и мозги не еби зайбал у нас есть")
    with open('1.jpg', 'rb')as p1:
        await message.answer_photo(p1, caption="1. ебаный осел")
    with open('2.jpg', 'rb')as p2:
        await message.answer_photo(p2,caption="2. ахуенная капибара")
    with open('3.jpg', 'rb')as p3:
        await message.answer_photo(p3, caption="3. бобр далбан")
    with open('4.jpg', 'rb')as p4:
        await message.answer_photo(p4, caption="4. ахуенный я пиздатый сексуальный анальный великолепный бля идеал просто")

@dp.message_handler(text=[1,2,3,4])
async def kazah(message:types.Message):
    cursor = connect.cursor()
    if message.text == '1':
        cursor.execute(f"INSERT INTO orders VALUES('осел', 'None', '{time.ctime()}');")
        await message.answer("бедный ослик")
    elif message.text == '2':
        cursor.execute(f"INSERT INTO orders VALUES('капибара', 'None', '{time.ctime()}');")
        await message.answer("нет капибара нет-нет")
    elif message.text == '3':
        cursor.execute(f"INSERT INTO orders VALUES('бобр', 'None', '{time.ctime()}');")
        await message.answer("че бобра убивать что опять")
    elif message.text == '4':
        cursor.execute(f"INSERT INTO orders VALUES('Асхат', 'None', '{time.ctime()}');")
        await message.answer("бля он один такой если его есть то только в постели")
    
    connect.commit()
    await message.reply("ожидай еду живадер")

@dp.message_handler()
async def pidr(message:types.Message):
    await message.reply("Ты еблан у меня нет таких команд вот мои команды", reply_markup=button)
    print("hello")
executor.start_polling(dp)