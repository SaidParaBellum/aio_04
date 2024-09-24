import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, \
    ReplyKeyboardMarkup

from app.notes.models import Note
from app.states import NoteState

router=Router()

logger=logging.getLogger('handlers')






# @router.message(Command('notes'))
# async def get_notes(message:Message):
#     notes=await Note.get_all()
#     print(notes)
#     for i in notes:
#         await message.answer(f'{i.id} {i.title} {i.content}')


@router.message(Command('edit'))
async def update_note(message: Message):
    note=await Note.update(2,title='Edited')
    print(note.title)
    await message.answer(f"Заметка изменена на {note.title}")


@router.message(F.text.startswith('delete'))
async def delete_note(message: Message):
    note_id=int(message.text.split(' ')[1])
    await Note.delete(Note.id==note_id)
    await message.answer('Заметка удалена')

@router.message(Command('filter'))
async def filter_note(message:Message):
    notes=await Note.filter(Note.title=='First')
    notes=await Note.pagginate(limit=10,page=1,filters=Note.content)
    await message.answer(f"Кол-во заметок- {len(notes)}")

@router.message(CommandStart())
async def zam_handler(message:Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Вывести заметку')],
        [KeyboardButton(text='Создать заметку')],

    ])
    await message.answer("Выберите один из вариантов",reply_markup=kb)

@router.message(F.text == 'Вывести заметку')
async def show_handler(message:Message):
    data = await Note.get_all()
    text = ''
    for i in data:
        text +=f'''Номер заметки: {i.id}
Название заметки: {i.title}
Описание заметки: {i.content}

'''
    await message.answer(f'{text}')

@router.message(F.text == 'Создать заметку')
async def create_note(message: Message, state: FSMContext):
    await message.answer('Введите название')
    await state.set_state(NoteState.title)


@router.message(NoteState.title)
async def handle_title(message: Message, state: FSMContext):

    await state.update_data(title=message.text)
    await message.answer('Введите Описание')
    await state.set_state(NoteState.description)


@router.message(NoteState.description)
async def handle_data(message: Message, state: FSMContext):

    data = await state.get_data()
    title = data['title']

    description = message.text
    note = await Note.create(title=title, content=description)
    await message.answer('Заметка создана')

    await state.clear()


# @router.message(Command('заметка'))
# async def get_note(message:Message):
#     notes=await Note.get_all()
#     note: Note=notes[0]
#     print(note.user.name)
#     print(notes)

