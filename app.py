import multiprocessing as mp
import os
import shutil

from aiogram import executor

from utils import sound_to_text as s2t

from utils.logger import logger
from loader import dp
from bot_commands.bot_commands import set_default_commands


async def start(dp):
    logger.info("Bot has been started")
    await set_default_commands(dp)


if __name__ == '__main__':
    if os.path.isdir('medias'):
        shutil.rmtree('medias')
    os.makedirs('medias/input')
    os.mkdir('medias/out')

    if not os.path.isdir('archive'):
        os.mkdir('archive')

    if not os.path.isdir('data'):
        os.mkdir('data')

        with open('data/data.txt', 'w') as f:
            f.write(0)

    v2t = mp.Process(target=s2t.main)
    v2t.start()
    logger.info("Thread has been started (v2t)")

    executor.start_polling(dp, on_startup=start)
