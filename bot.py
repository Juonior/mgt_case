import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
import os
import datetime, time
from aiogram.types import reply_keyboard, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import Window
from aiogram.types import ParseMode
from aiogram.utils import executor
import json
import random

dir = os.path.abspath(os.curdir)

owner_id = int

bot = Bot(token = '5788336893:AAHvi3ZlrG0sLGEhiXeLgzwYF1mkpA2jixM')
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
logging.basicConfig(level = logging.INFO)

class User():
    is_true = False
    is_login = False
    id = 0
    mail = ''
    busss = {
        'A750': ['Ст. Солнечная', 'Почта', 'Попутная ул.', 'Боровский пр.', 'Боровское ш., 20', 'Метро "Боровское шоссе"', '9-я Чоботовская ал.', 'Новопеределкинская ул.', 'Метро "Новопеределкино"', 'Метро "Новопеределкино"', 'Боровское ш., 56', 'Рассказовка-1', 'Метро "Рассказовка"', 'Пыхтино', 'Внуковское ш.', 'Изваринская ул.', 'Внуковский з-д', 'Постниково', 'Внуково-3', 'АЗС', 'Садовые участки', 'Привольная ул.', 'Дачный пос.', 'Марушкино', 'Советская ул.', 'Советская ул., 41', 'Д. Толстопальцево', 'Ст. Толстопальцево']
        }
    info = dict


class Form(StatesGroup):

    name = State() 
    bday = State()
    passport = State()
    passport_data = State()
    passport_place = State()
    email = State()
    password = State()
    phone_number = State()

class Courrier(StatesGroup):

    bus = State()
    stop_from = State()
    stop_to = State()

class Sender(StatesGroup):

    recipient_id = State()
    from_stop = State()
    to_stop = State()
    sender_id = State()

def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('/cancel'))

'''def tracknumber():
    track = str(random.randint(1, 999)) + hex(int(User.id))[2:] + oct(int(User.id))[2:] + hex(int(User.id)//random.randint(1,100))[2:] + str(random.randint(1, 999))

    return track'''

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message, state: FSMContext):
    #User.id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Войти", "Зарегистрироваться"]
    keyboard.add(*buttons)
    await message.answer("Приветствую тебя!\nВыбери действие на клавиатуре", reply_markup=keyboard)

@dp.message_handler(commands=["cancel"], state = '*')
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Действие отменено')
    await state.finish()
    # await cmd_start(message, state=None)

@dp.message_handler(Text(equals='Зарегистрироваться', ignore_case=True), state = None)
async def registration(message: types.Message, state: FSMContext) -> None:
    await Form.name.set()
    await message.answer('Отправь своё ФИО', reply_markup = get_cancel())

    await Form.name.set()

@dp.message_handler(state=Form.name)
async def user_name(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['name'] = answer

    await message.answer('Отправь свою дату рождений(dd.mm.yyyy)', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.bday)
async def user_bday(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['bday'] = answer

    await message.answer('Отправь Серию и Номер паспорт(xxxx yyyyyy)', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.passport)
async def user_passport(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['passport'] = answer

    await message.answer('Отправь дату выдачи паспорта(dd.mm.yyyy)', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.passport_data)
async def user_passport(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['passport_data'] = answer

    await message.answer('Отправь место выдачи паспорта', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.passport_place)
async def user_passport(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['passport_place'] = answer

    await message.answer('Отправь почту', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.email)
async def user_email(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)
    
    async with state.proxy() as data:
        data['email'] = answer

    User.mail = data['email']
    await message.answer('Отправь пароль', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.password)
async def user_password(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['password'] = answer

    await message.answer('Отправь номер телефона', reply_markup = get_cancel())

    await Form.next()

@dp.message_handler(state=Form.phone_number)
async def user_phone(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['phone'] = answer

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Главное меню"]
    keyboard.add(*buttons)

    User.is_login = True

    await message.answer('Вы успешно зарегистрировались!', reply_markup = keyboard)

    async with state.proxy() as data:

        data_pass = data['passport']+';'+data['passport_place']+';'+data['passport_data']

        fio = data['name'].split(' ')
        print(fio)
        name = fio[0]
        surname = fio[1]
        patronymic = fio[2]

        datas = {
            "email": data['email'],
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
            'phone_number': data['phone'],
            'password': data['password'],
            'passport_data': data_pass
            }

        print(datas)

        r = requests.post('http://192.168.2.60:5000/users', json=datas)

        print(r)

    await state.finish()

@dp.message_handler(lambda message: message.text == "Войти" and User.is_login == False)
async def login(message: types.Message):
    await message.answer('Введите логин и пароль(логин|почта|телефон пароль)', reply_markup = get_cancel())

@dp.message_handler(lambda message: message.text and User.is_login == False)
async def login_verification(message: types.Message):
    user_data = message.text.split(' ')
    login = user_data[0]
    password = user_data[1]

    if '@' in str(login):
        r = requests.get(f'http://192.168.2.60:5000/auth/email/{login}/{password}')

    else:
        r = requests.get(f'http://192.168.2.60:5000/auth/phone_number/{login}/{password}')

    if r.status_code == 200:

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Отправить посылку", "Получить посылку", "Стать курьером", "Биржа заказов"]
        keyboard.add(*buttons)
        User.is_login = True
        User.mail = login
        await message.answer('Вы успешно вошли!\nВыберите дальнейшее действие', reply_markup=keyboard)

    else:

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["/start"]
        keyboard.add(*buttons)
        User.is_login = False
        await message.answer('Пользователь не найден', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Стать курьером" and User.is_login == True, state = None)
async def be_courrier(message: types.Message, state: FSMContext):
    await message.answer('Укажите номер автобуса, на котором вы передвигаетесь')

    await Courrier.bus.set()

@dp.message_handler(state=Courrier.bus)
async def courrier_bus(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['bus'] = answer

    r = requests.get(f'http://192.168.2.60:5000/get_route/{data["bus"]}')
    k = r.json()['stations']
    s = ''
    for i in range(len(k)):
        s+=str(i+1)+'. '+k[i]+'\n'
    await message.answer(f'Отправь начальную остановку!\n{s}', reply_markup = get_cancel())

    await Courrier.next()

@dp.message_handler(state=Courrier.stop_from)
async def courrier_first(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['stop_from'] = str(int(answer)-1)
    r = requests.get(f'http://192.168.2.60:5000/get_route/{data["bus"]}')
    k = r.json()['stations']
    s = ''
    for i in range(len(k)):
        s+=str(i+1)+'. '+k[i]+'\n'
    await message.answer(f'Отправь конечную остановку!\n{s}', reply_markup = get_cancel())

    await Courrier.next()  


@dp.message_handler(state=Courrier.stop_to)
async def courrier_last(message: types.Message, state: FSMContext):
    answer = message.text

    # await state.update_data(name = answer)

    async with state.proxy() as data:
        data['stop_to'] = answer

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Главное меню"]
    keyboard.add(*buttons)

    r = requests.get(f'http://192.168.2.60:5000/get_route/{data["bus"]}')
    k = r.json()['stations']
    log = User.mail
    if '@' in log:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_email/{log}')
    else:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_phone_number/{log}') 
    us_id = r.json()["id"]
    User.id = us_id
    print(us_id)
    await message.answer('Вы успешно стали курьером, доступные заказы вы можете посмотреть на бирже заказов', reply_markup=keyboard)

    async with state.proxy() as data:
        
        in1 = int(data['stop_from'])
        in2 = int(data['stop_to'])
        if in2-in1 > 0:
            chck = 1
        else:
            chck = -1
        # print('AAAAAAAAAAAAAA',from_, to_)
        '''in1 = k.index('from_')
        in2 = k.index('to_')'''
        dt = {
           "routes": {data["bus"]: k[in1:in2:chck]}
            }
        print(us_id, dt, type(dt), type(k), type(k[0]), type(data['bus']))
        r = requests.post(f'http://192.168.2.60:5000/update_routes_by_user_id/{us_id}', json=dt)
        print(r)

    await state.finish()

@dp.message_handler(lambda message: message.text == "Отправить посылку" and User.is_login == True, state = None)
async def user_email(message: types.Message, state: FSMContext):

    await message.answer('Отправьте email или номер получателя')
    await Sender.recipient_id.set() 

    log = User.mail
    if '@' in log:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_email/{log}')
    else:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_phone_number/{log}') 

    if r.status_code == 200:
        ans = r.json()["id"]
        async with state.proxy() as data:
            data['sender_id'] = ans 
    else:
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Главное меню"]
        keyboard.add(*buttons)

        await message.answer('Произошла непредвиденная ошибка, повторите попытку', reply_markup=keyboard)

    #await Sender.next()     

@dp.message_handler(state=Sender.recipient_id)
async def user_name(message: types.Message, state: FSMContext):
    answer = message.text

    if '@' in answer:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_email/{answer}')
    else:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_phone_number/{answer}') 
    if r.status_code == 200:
        ans = r.json()["id"]

        async with state.proxy() as data:
            data['recipient_id'] = ans
        r = requests.get(f'http://192.168.2.60:5000/get_route/32')
        k = r.json()['stations']
        s = ''
        for i in range(len(k)):
            s+=str(i+1)+'. '+k[i]+'\n'
        await message.answer(f'Выберите остановку отправки\n{s}')

        await Sender.next()
    
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Главное меню"]
        keyboard.add(*buttons)
        await message.answer('Получатель не зарегистрирован', reply_markup=keyboard)
        state.finish()

@dp.message_handler(state=Sender.from_stop)
async def user_name(message: types.Message, state: FSMContext):
    answer = str(int(message.text)-1)

    async with state.proxy() as data:
        data['from_stop'] = answer

    r = requests.get(f'http://192.168.2.60:5000/get_route/32')
    k = r.json()['stations']
    s = ''
    for i in range(len(k)):
        s+=str(i+1)+'. '+k[i]+'\n'
    await message.answer(f'Выберите остановку получателя\n{s}')
    await Sender.next()

@dp.message_handler(state=Sender.to_stop)
async def user_name(message: types.Message, state: FSMContext):
    answer = message.text

    r = requests.get(f'http://192.168.2.60:5000/get_route/32')
    k = r.json()['stations']

    async with state.proxy() as data:
        data['to_stop'] = answer

        datas = {
            "sender_id": data['sender_id'],
            "recipient_id": data['recipient_id'],
            "destination_station": k[int(data['to_stop'])-1],
            "departure_station": k[int(data['from_stop'])]
        }

        print(datas)

    r = requests.post('http://192.168.2.60:5000/orders', json=datas)

    await message.answer('Объявление создано')
    await state.finish()

@dp.message_handler(lambda message: message.text == "Биржа заказов" and User.is_login == True and User.is_true == False)
async def market(message: types.Message):
    global ans
    log = User.mail
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Главное меню"]
    keyboard.add(*buttons)
    if '@' in log:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_email/{log}')
    else:
        r = requests.get(f'http://192.168.2.60:5000/get_user_by_phone_number/{log}') 

    data = r.json()
    User.info = data

    r = requests.post('http://192.168.2.60:5000/get_correct_orders', json = data)
    ans = r.json()
    s = ''
    if len(ans) > 0:
        for i in range(len(ans)):   
            s+=str(i+1)+'. Заказ №'+str(ans[i]['id'])+'\nОткуда: '+ans[i]['departure_station']+'\nКуда: '+ ans[i]['destination_station']+'\n'
        await message.answer(f'Выберите один из доступных заказов\n{s}', reply_markup=keyboard)
        User.is_true = True
    else:
        await message.answer('Доступных заказов нет', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text and User.is_login == True and User.is_true == True)
async def market2(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Главное меню"]
    keyboard.add(*buttons)
    global ans
    answer = message.text
    print(User.info)
    data = {
        "user": User.info, 
        "order": ans[int(answer)-1]
        }
    print(data)
    r = requests.post('http://192.168.2.60:5000/take_order/', json = data)
    await message.answer('Вы успешно взяли заказ!', reply_markup=keyboard)
    return

@dp.message_handler(lambda message: message.text == "Главное меню" and User.is_login == True)
async def registration(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отправить посылку", "Получить посылку", "Стать курьером", "Биржа заказов"]
    keyboard.add(*buttons)

    await message.answer('Добро пожаловать в главное меню', reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)