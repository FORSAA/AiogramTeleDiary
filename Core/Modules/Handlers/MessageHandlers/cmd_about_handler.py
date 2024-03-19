from Core.Modules.Imports.Libs.HandlersLibs import *

cmd_about_router = Router()


@cmd_about_router.message(Command('start'))
async def cmd_start(message: Message):
    await TelebotFunctions.render(message, StartPage, True)
