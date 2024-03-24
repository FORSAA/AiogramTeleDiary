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
