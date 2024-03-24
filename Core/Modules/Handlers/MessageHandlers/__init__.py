from aiogram import Router
from .any_message_handler import any_message_router
from .cmd_start_handler import cmd_start_router
from .cmd_about_handler import cmd_about_router

MessageRouters = Router()
MessageRouters.include_routers(cmd_start_router, cmd_about_router, any_message_router)
