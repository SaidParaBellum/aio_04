from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import html
router = Router()
import requests

main_commands = [
    'Меню',
    'Язык',
    'История заказов',
    'Тех. поддержка',
    'users'
]


@router.message(CommandStart())
async def start_handler(message: Message):

    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Меню')],
        [KeyboardButton(text='Язык')],
        [KeyboardButton(text='История заказов')],
        [KeyboardButton(text='Тех. поддержка')],
        [KeyboardButton(text='users')]
    ])

    await message.answer(f'''
Hello, {html.bold(message.from_user.first_name)}
id: {message.from_user.id}
''', reply_markup=kb)


@router.message(Command('do', 'work', prefix='/'))
async def do_handler(message: Message):

    await message.answer(message.text)

# @router.message(F.text == 'Меню')
# async def menu_handler(message: Message):
#     await message.answer('Меню')

@router.message(F.text.in_(main_commands))
async def main_commands_handler(message: Message):
    if message.text == 'Меню':
        await message.answer('Меню')
    elif message.text == 'Язык':
        await message.answer('Язык')
    elif message.text == 'История заказов':
        await message.answer('История заказов')
    elif message.text == 'Тех. поддержка':
        await message.answer('Тех. поддержка')


@router.message(Command('users'))
async def message_handler(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='5')],
        [KeyboardButton(text='10')],
        [KeyboardButton(text='15')],
        [KeyboardButton(text='20')]
    ])

    await message.answer('Выберите лимит пользователей:', reply_markup=kb)


@router.message(F.text.in_(['5', '10', '15', '20']))
async def limit_handler(message: Message):
    limit = int(message.text)
    data = requests.get(f'https://reqres.in/api/users?per_page={limit}').json()
    users = data.get('data', [])
    answer = ''

    for user in users:
        answer += f'{user.get("id")}. {user.get("first_name")} {user.get("last_name")}\n'

    await message.answer(answer)


@router.message(F.text.func(lambda text: text.isdigit() ))
async def user_id_handler(message: Message):
    user_id = int(message.text)
    data = requests.get(f'https://reqres.in/api/users/{user_id}').json()

    user = data.get('data', {})
    if user:
        answer = f'{user.get("id")}. {user.get("first_name")} {user.get("last_name")}\n'
    else:
        answer = 'Нет такого пользователя'
    await message.answer(answer)