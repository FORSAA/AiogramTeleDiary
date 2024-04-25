import os

from Core.Modules.Libs.FunctionsLibs import *
SEPARATOR = ':'


class TelebotFunctions:
    @staticmethod
    async def render(data: Message | CallbackQuery, page: Page, del_last=True, del_user_last=True) -> None:
        user_id: int = data.from_user.id

        local_bot_last_message: None | Message = None
        local_user_last_message: None | Message = None

        if (user_id not in states):
            await TelebotFunctions.add_to_states(user_id)

            if (isinstance(data, CallbackQuery)):
                local_bot_last_message: Message = data.message
        else:
            local_bot_last_message: Message = states[user_id].bot_last_message

        if (isinstance(data, Message)):
            if (not data.from_user.is_bot):
                local_user_last_message: Message = data

        if (del_last and local_bot_last_message):
            try:
                await local_bot_last_message.delete()
            except BaseException:
                pass

        if (del_user_last and local_user_last_message):
            await local_user_last_message.delete()

        if (isinstance(data, CallbackQuery)):
            data = data.message

        states[user_id].bot_last_message = await data.answer(page.message_text, parse_mode='HTML',
                                                             reply_markup=await TelebotFunctions.markup_generator(page))

    @staticmethod
    async def check_directory_existence(path: str) -> bool:
        if (os.path.exists(path)):
            return True
        else:
            return False

    @staticmethod
    async def create_directory(path: str) -> None:
        os.makedirs(path)

    @staticmethod
    async def clear_directory(path: str):
        files = os.listdir(path)

        for file in files:
            file_path = os.path.join(path, file)

            if (os.path.isfile(file_path)):
                os.remove(file_path)

    @staticmethod
    async def add_to_states(user_id: int, bot_last_message: Message = None) -> User:
        user_paths = (
            "\\".join([os.getcwd(), "Core", "Temp_Files", "Docs", f"User_{user_id}"]),
            "\\".join([os.getcwd(), "Core", "Temp_Files", "Screenshots", f"User_{user_id}"]),
            "\\".join(["Temp_Files", "Docs", f"User_{user_id}"]),
            "\\".join(["Temp_Files", "Screenshots", f"User_{user_id}"])
        )

        if not (await TelebotFunctions.check_directory_existence(user_paths[0])):
            await TelebotFunctions.create_directory(user_paths[0])

        if not (await TelebotFunctions.check_directory_existence(user_paths[1])):
            await TelebotFunctions.create_directory(user_paths[1])

        defaults = {
            'auth_state': 0,
            'menu_state': 'start',
            'bot_last_message': bot_last_message,
            'auth_data': None,
            'wish_type': None,
            'wish_day': None,
            'docs_path_absolute': user_paths[0],
            'docs_path_relative': user_paths[2],
            'screenshots_path_absolute': user_paths[1],
            'screenshots_path_relative': user_paths[3]
        }
        states[user_id] = User(defaults)
        return states[user_id]

    @staticmethod
    async def markup_generator(page: Page, row_width: int = 2) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for button in page.markup_data:
            builder.add(button)
        builder.adjust(row_width)
        return builder.as_markup()

    @staticmethod
    async def process_request(user_id: int) -> dict[str, str]:
        auth_data = states[user_id].auth_data
        # await WebsiteInteraction.test()
        return {}
