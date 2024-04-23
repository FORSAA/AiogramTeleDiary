from Core.Modules.Libs.MainLibs import *
from Core.Modules.Classes.UserClass import User
import os

FILES_DIR = '\\'.join([os.getcwd(), 'Core', 'Temp_Files'])

states: dict[int, User] = {}
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

# browser_options = webdriver.ChromeOptions()

# browser_options.add_argument("--headless=new")
# prefs = {
#     "download.default_directory": '\\'.join([os.getcwd(), 'Core', 'Temp_Files']),
#     'profile.default_content_setting_values.automatic_downloads': 1,
# }
# browser_options.add_experimental_option("prefs", prefs)
#
# browser = webdriver.Chrome(options=browser_options)
# browser.set_window_size(2515, 1250)


async def start():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(HandlersRouter)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Stopping..')
