from aiogram.types import Message


class User:
    def __init__(self, states_dict: dict = {}):
        self.auth_state = states_dict.get('auth_state', False)
        self.menu_state = states_dict.get('menu_state', 'start')
        self.bot_last_message: Message = states_dict.get('bot_last_message', None)
        self.auth_data = states_dict.get('auth_data', None)
        self.wish_type = states_dict.get('wish_type', None)
        self.wish_day = states_dict.get('wish_day', None)
        self.docs_path_absolute = states_dict.get('docs_path_absolute', None)
        self.docs_path_relative = states_dict.get('docs_path_relative', None)
        self.screenshots_path_absolute = states_dict.get('screenshots_path_absolute', None)
        self.screenshots_path_relative = states_dict.get('screenshots_path_relative', None)

    def __repr__(self):
        states_dict = {
            'auth_state': self.auth_state,
            'menu_state': self.menu_state,
            'bot_last_message': self.bot_last_message,
            'auth_data': self.auth_data,
            'wish_type': self.wish_type,
            'wish_day': self.wish_day,
        }
        return f"User({states_dict})"
