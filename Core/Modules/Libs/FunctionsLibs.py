from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
# from Core.Modules.Classes.Pyppeteer.WebsiteInteraction import WebsiteInteraction
from Core.Modules.Templates.UserClassTemplate import User
from Core.Modules.Templates.PageClassTemplates import Page
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from main import states, bot
import os
import aiogram.exceptions
import aiogram

