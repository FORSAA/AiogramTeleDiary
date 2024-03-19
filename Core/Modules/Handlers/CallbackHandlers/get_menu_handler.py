from Core.Modules.Imports.Libs.HandlersLibs import *

get_menu_router = Router()


@get_menu_router.callback_query(lambda call: call.data == 'menu')
async def get_menu(call: CallbackQuery):
    await call.answer('')
    await TelebotFunctions.render(call, StartPage)
