from aiogram import Router
from .auth_data_edit import auth_data_edit_router
from .homework_request import request_homework_router

StepHandlersRouter = Router()
StepHandlersRouter.include_routers(auth_data_edit_router, request_homework_router)

