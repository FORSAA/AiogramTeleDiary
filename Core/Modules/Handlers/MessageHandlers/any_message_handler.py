from Core.Modules.Libs.HandlersLibs import *

any_message_router = Router()


@any_message_router.message(F)
async def any_message(message: Message):
    await message.delete()
