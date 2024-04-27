import asyncio

from Core.Modules.Libs.MainLibs import *
from Core.Modules.Templates.UserClassTemplate import User
import os

FILES_DIR = '\\'.join([os.getcwd(), 'Core', 'Temp_Files'])

states: dict[int, User] = {}
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def start():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(HandlersRouter)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        print('Stopping..')
