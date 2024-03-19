from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter, StateFilter, Command, CommandStart
from Core.Modules.Imports.Classes.States.AuthEditClass import AuthEdit
from Core.Modules.Imports.Classes.States.HomeworkRequest import HomeworkRequest
from Core.Modules.Imports.Classes.TelebotFunctions import *
from Core.Modules.Imports.Templates.PageClassTemplates import *
import asyncio

