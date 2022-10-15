"""
Задаёт машину состояний
"""
from aiogram.dispatcher.filters.state import StatesGroup, State


class Voice2Text(StatesGroup):
    wait_voice = State()
    wait_recognition = State()
