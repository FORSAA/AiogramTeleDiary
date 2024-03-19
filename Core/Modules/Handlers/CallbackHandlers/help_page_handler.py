from Core.Modules.Imports.Libs.HandlersLibs import *

help_page_router = Router()


@help_page_router.callback_query(lambda call: call.data == 'help_page')
async def help_page(call: CallbackQuery):
    await call.answer('')
    await TelebotFunctions.render(call, HelpPage)
