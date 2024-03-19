from aiogram import Router
from .CallbackHandlers import CallbackRouters
from .MessageHandlers import MessageRouters
from .StepHandlers import StepHandlersRouter

HandlersRouter = Router()
HandlersRouter.include_routers(CallbackRouters, StepHandlersRouter, MessageRouters)
