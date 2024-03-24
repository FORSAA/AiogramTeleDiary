from Core.Modules.Libs.HandlersLibs import *

cmd_start_router = Router()


@cmd_start_router.message(Command('start'))
async def cmd_start(message: Message):
    await TelebotFunctions.render(message, StartPage, True)
