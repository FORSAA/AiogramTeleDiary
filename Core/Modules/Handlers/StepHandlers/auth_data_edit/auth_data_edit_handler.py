from Core.Modules.Libs.HandlersLibs import *

auth_data_edit_router = Router()


@auth_data_edit_router.callback_query(StateFilter(None), lambda call: call.data == "auth_data_edit")
async def cal_auth_data_edit(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await TelebotFunctions.render(call, AuthDataEditPage)
    await state.set_state(AuthEdit.changing_login)


@auth_data_edit_router.message(
    AuthEdit.changing_login
)
async def login_sent(message: Message, state: FSMContext):
    await state.update_data(login=message.text)

    from_chat = message.chat.id
    await states[from_chat].bot_last_message.delete()

    states[from_chat].bot_last_message = await message.answer('Логин принят! Теперь введите пароль.')
    await message.delete()

    await state.set_state(AuthEdit.changing_password)


@auth_data_edit_router.message(
    AuthEdit.changing_password
)
async def password_sent(message: Message, state: FSMContext):
    await state.update_data(password=message.text)

    from_chat = message.chat.id
    await states[from_chat].bot_last_message.delete()

    user_data = await state.get_data()
    login = user_data['login']
    password = user_data['password']

    await message.delete()
    states[from_chat].bot_last_message = await message.answer(
        f'Пароль принят! Сохранены следующие данные для авторизации: "{login} : {password}"!\n\n'
        f'Выходим в главное меню..'
    )

    states[from_chat].auth_state = True
    states[from_chat].auth_data = {
        'login': login,
        'password': password
    }

    await asyncio.sleep(2)
    await TelebotFunctions.render(message, StartPage, del_user_last=False)

    await state.clear()
