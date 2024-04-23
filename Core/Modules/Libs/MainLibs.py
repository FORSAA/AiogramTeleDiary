from aiogram import Bot, Dispatcher, Router

from Core.Modules.Handlers import HandlersRouter
import logging, asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options