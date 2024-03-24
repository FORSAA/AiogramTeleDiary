from Core.Modules.Libs.HandlersLibs import *

cmd_about_router = Router()


@cmd_about_router.message(Command('about'))
async def cmd_start(message: Message):
    await TelebotFunctions.render(message, AboutPage, True)
