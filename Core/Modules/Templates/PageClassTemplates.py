from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.types import InlineKeyboardButton


class Page:
    def __init__(self, name: str, message_text: str, markup_data: list[InlineKeyboardButton] = []):
        self.name = name
        self.message_text = message_text
        self.markup_data = markup_data

        """
        # Markup_data example:
            markup_data = [
                InlineKeyboardButton(text='Привет!', callback_data='hello')
            ]
        """


StartPage = Page(
    name='start',
    message_text='Добро пожаловать в главное меню телеграмм бота!\n\n'
                 'Используйте кнопки ниже для навигации.',
    markup_data=[
        InlineKeyboardButton(text='Смена Логина/Пароля', callback_data='auth_data_edit'),
        InlineKeyboardButton(text='Как пользоваться?', callback_data='help_page'),
        InlineKeyboardButton(text='Получить Д/З', callback_data='get_homework')
    ]
)

AuthDataEditPage = Page(
    name='auth_data_edit',
    message_text=f'Тут вы можете поменять ваш логин и пароль для автоматической работы бота.\n\n'
                 f'Вы должны ввести ваш логин и пароль <u>двумя</u> <u>отдельными</u> сообщениями (Первым логин, вторым пароль). Бот ожидает ввода.\n\n'
                 f'P.S: <b><i>Отправляя свои данные авторизации вы делаете это добровольно и соглашаетесь с их обработкой.</i></b>"',
    markup_data=[
        InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu')
    ]
)

HelpPage = Page(
    name='help_page',
    message_text='Как пользоваться ботом? Очень легко!\n\n'
                 'Для начала использования бота достаточно ввести логин и пароль от сайта ГИССОЛО на странице "Смена логина/пароля". (Кнопка "Смена Логина/Пароля").\n\n'
                 'После выполнения этого шага вы можете перейти в <i>"Получить Д/З"</i>, выбрать формат и день недели. Ваш запрос будет обработан.',
    markup_data=[
        InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu')
    ]
)

GetHomeworkPage = Page(
    name='get_homework',
    message_text='Выберите в каком формате бот должен прислать вам домашнее задание:',
    markup_data=[
        InlineKeyboardButton(text='Фотография', callback_data='homework_wish_photo'),
        InlineKeyboardButton(text='Текст', callback_data='homework_wish_text'),
        InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu')
    ]
)

DaySelectPage = Page(
    name='day_select_page',
    message_text='Выберите день недели домашнее задание для которого вас интересует:',
    markup_data=[
        InlineKeyboardButton(text='Понедельник', callback_data='0_day'),
        InlineKeyboardButton(text='Четверг', callback_data='3_day'),
        InlineKeyboardButton(text='Вторник', callback_data='1_day'),
        InlineKeyboardButton(text='Пятница', callback_data='4_day'),
        InlineKeyboardButton(text='Среда', callback_data='2_day'),
        InlineKeyboardButton(text='Суббота', callback_data='5_day'),
        InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu'),
    ]
)

AboutPage = Page(
    name='about_page',
    message_text='Годовой проект создан учеником класса 9.4 школы МОБУ "СОШ "ЦО "Кудрово", Захаровым Егором.\n\n'
                 '<b>Telegram</b>: https://t.me/Unsaint_d\n'
                 '<b>Discord</b>: unsaint_d\n'
                 '<b>VK</b>: https://vk.com/ilnkar',
    markup_data=[
        InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu')
    ]

)

AwaitPage = Page(
    name='help_page',
    message_text='Запрос отправлен! Ожидайте ответ бота.',
    markup_data=[
    ]
)

BlankPage = Page(
    name='BlankPage',
    message_text='',
    markup_data=[
        InlineKeyboardButton(text='« Вернуться в главное меню', callback_data='menu')
    ]
)