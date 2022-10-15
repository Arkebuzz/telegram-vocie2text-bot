"""
Задаёт параметры ответа бота
"""

import asyncio
import os
import shutil

from aiogram import types
from aiogram.dispatcher.filters import state
from aiogram.types import Message

from bot_commands.keyboards import start_menu
from bot_commands.states import Voice2Text
from loader import dp
from utils.logger import logger


async def set_default_commands(dp):
    """
    Задаёт список команд доступных пользователю
    """
    await dp.bot.set_my_commands([
        types.BotCommand('/menu', 'Открыть меню бота')
    ])


@dp.message_handler(text=['/menu', '/start'], state=state.any_state)
async def menu_action(message: Message):
    """
    Вывод меню
    """
    logger.info(f'{message.from_user.id} call for menu')
    await message.answer(
        text='Я могу преобразовать голос в текст.\n'
             'Просто отправь мне голосовое сообщение!',
        reply_markup=start_menu
    )

    await Voice2Text.wait_voice.set()


@dp.message_handler(content_types=['voice'], state=[Voice2Text.wait_voice, None])
async def voice_message(message: Message):
    """
    Получение голосовых сообщений
    """
    await Voice2Text.wait_recognition.set()
    await message.reply(text='Отлично! Сообщение получено!\n'
                             'Подождите, пока я преобразую его в текст.\n'
                             'Это может занять некоторое время.')

    logger.info(f'{message.from_user.id} voice received')

    voice = await message.voice.get_file()
    await dp.bot.download_file(file_path=voice.file_path, destination=f'medias/input/{message.from_user.id}.temp')
    shutil.move(f'medias/input/{message.from_user.id}.temp', f'medias/input/{message.from_user.id}.ogg')

    await send_text_out(message.from_user.id)


@dp.message_handler(text=None, content_types=types.ContentTypes.ANY, state=Voice2Text.wait_recognition)
async def voice_message(message: Message):
    """
    Если отправлено несколько голосовых сообщений за раз, то бот ругается
    """
    await message.reply(text='Подождите, я уже преобразую ваше голосовое сообщение!\n')

    logger.info(f'{message.from_user.id} new message')


async def send_text_out(id):
    """
    Отправляет расшифрованное голосовое сообщение в виде текста
    """
    while not os.path.isfile(f'medias/out/{id}.txt'):
        await asyncio.sleep(5)

    with open(f'medias/out/{id}.txt', encoding='utf-8') as f:
        text = f.readlines()

        if len(text) == 2 and text[1] == 'READY':
            await dp.bot.send_message(id, text[0])
        else:
            await send_text_out(id)
            return

    os.remove(f'medias/out/{id}.txt')

    with open(f'data/data.txt', 'r', encoding='utf-8') as f:
        requests = int(f.read()) + 1

    with open(f'data/data.txt', 'w', encoding='utf-8') as f:
        f.write(str(requests))

    logger.info(f'{id} text sent')

    await Voice2Text.wait_voice.set()
