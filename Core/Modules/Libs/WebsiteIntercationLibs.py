import pyppeteer.errors
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle
from datetime import datetime, timedelta
from main import states
from pyppeteer import launch
from time import sleep
import asyncio
# from Core.Modules.Classes.BotProcessFunctions import *
import locale, asyncio, os, re, pyppeteer.errors

locale.setlocale(locale.LC_TIME, 'ru_RU')
