from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaDocument, InputMediaPhoto, FSInputFile, InputMedia
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter, StateFilter, Command, CommandStart
from Core.Modules.Classes.States.AuthEditClass import AuthEdit
from Core.Modules.Classes.States.HomeworkRequest import HomeworkRequest
from Core.Modules.Classes.BotProcessFunctions import *
from Core.Modules.Templates.PageClassTemplates import *
from Core.Modules.Classes.Pyppeteer.WebsiteInteraction import WebsiteInteraction
from main import states
from aiogram.enums import ChatAction
from aiogram.utils.media_group import MediaGroupBuilder
import asyncio




