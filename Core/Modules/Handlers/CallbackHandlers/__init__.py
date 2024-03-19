from aiogram import Router
from .get_menu_handler import get_menu_router
from .help_page_handler import help_page_router

CallbackRouters = Router()
CallbackRouters.include_routers(get_menu_router, help_page_router)
