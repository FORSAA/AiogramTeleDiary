from Core.Modules.Imports.Libs.MainLibs import *
from Core.Modules.Imports.Classes.UserClass import User
import os


states: dict[int, User] = {}
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def start():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(HandlersRouter)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Stopping..')
