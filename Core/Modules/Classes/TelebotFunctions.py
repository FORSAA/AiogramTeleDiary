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
            await local_bot_last_message.delete()

        if (del_user_last and local_user_last_message):
            await local_user_last_message.delete()

        if (isinstance(data, CallbackQuery)):
            data = data.message

        states[user_id].bot_last_message = await data.answer(page.message_text, parse_mode='HTML',
                                                             reply_markup=await TelebotFunctions.markup_generator(page))

    @staticmethod
    async def add_to_states(user_id: int, bot_last_message: Message = None) -> User:
        defaults = {
            'auth_state': 0,
            'menu_state': 'start',
            'bot_last_message': bot_last_message,
            'auth_data': None,
            'wish_type': None,
            'wish_day': None,
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
        return {}
