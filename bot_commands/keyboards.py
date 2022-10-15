"""
Создаёт наборы кнопок, прикрепляемые к сообщению.
"""
from aiogram.dispatcher.filters import state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp
from utils.logger import logger

start_menu = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [InlineKeyboardButton(text="Статистика", callback_data="statistics")],
                                      [InlineKeyboardButton(text="Как работает алгоритм?", callback_data="howwork")],
                                      [InlineKeyboardButton(text="Кто работал над проектом?", callback_data="about")]
                                  ])


@dp.callback_query_handler(state=state.any_state, text='statistics')
async def statistics_action(call: CallbackQuery):
    """
    Вывод статистики
    """
    logger.info(f'{call.from_user.id} call for statistics')

    with open(f'data/data.txt', 'r', encoding='utf-8') as f:
        requests = int(f.readline())

    await dp.bot.send_message(call.from_user.id, f'За время работы было преобразовано {requests} сообщений.')


@dp.callback_query_handler(state=state.any_state, text='howwork')
async def statistics_action(call: CallbackQuery):
    """
    Вывод информации о боте
    """
    logger.info(f'{call.from_user.id} call for how work')

    await dp.bot.send_message(call.from_user.id,
                              'Бот сделан на Python 3 при помощи библиотеки aiogram\n'
                              'Распознавание речи работает на базе Google Speech Recognition.')


@dp.callback_query_handler(state=state.any_state, text='about')
async def statistics_action(call: CallbackQuery):
    """
    Вывод информации о разработчике
    """
    logger.info(f'{call.from_user.id} call for about')

    await dp.bot.send_message(call.from_user.id, 'Над проектом работал @Arkebuzz\n')
