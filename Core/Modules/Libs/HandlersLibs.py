from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter, StateFilter, Command, CommandStart
from Core.Modules.Classes.States.AuthEditClass import AuthEdit
from Core.Modules.Classes.States.HomeworkRequest import HomeworkRequest
from Core.Modules.Classes.TelebotFunctions import *
from Core.Modules.Templates.PageClassTemplates import *
from main import states
import asyncio




