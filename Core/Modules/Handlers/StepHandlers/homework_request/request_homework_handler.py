from Core.Modules.Libs.HandlersLibs import *

request_homework_router = Router()


@request_homework_router.callback_query(
    lambda call: call.data == "get_homework"
)
async def cbk_request_homework(call: CallbackQuery, state: FSMContext):
    from_user: int = call.from_user.id

    if (from_user not in states):
        await TelebotFunctions.add_to_states(from_user, call.message)

    if (not states[from_user].auth_state):
        BlankPage.message_text = (
            'Ошибка! Вы не авторизованы!\n\n'
            'Перейдите на страницу авторизации, заполните данные и повторите попытку!'
        )
        await TelebotFunctions.render(call, BlankPage)
        return

    await call.answer('')
    await TelebotFunctions.render(call, GetHomeworkPage)
    await state.set_state(HomeworkRequest.selecting_wish_type)


@request_homework_router.callback_query(
    StateFilter(HomeworkRequest.selecting_wish_type),
    lambda call: 'wish' in call.data
)
async def cbk_wish_sent_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await state.update_data(wish=call.data.split('_')[2])
    await TelebotFunctions.render(call, DaySelectPage)
    await state.set_state(HomeworkRequest.selecting_day)


@request_homework_router.callback_query(
    StateFilter(HomeworkRequest.selecting_day),
    lambda call: 'day' in call.data
)
async def cbk_day_sent_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await state.update_data(day=call.data[0])
    await TelebotFunctions.render(call, AwaitPage)

    user_id = call.from_user.id

    request_params_data = await state.get_data()
    request_wish_type: str = request_params_data['wish']
    request_wish_day: str = request_params_data['day']

    request_data = {
        'auth_data': states[user_id].auth_data,
        'type': 'photo' if 'photo' in request_wish_type else 'text',
        'day': request_wish_day[0],
        'by_id': user_id
    }

    if (request_data['type'] == 'photo'):
        await call.message.bot.send_chat_action(user_id, ChatAction.UPLOAD_PHOTO)
    else:
        await call.message.bot.send_chat_action(user_id, ChatAction.TYPING)

    await state.clear()

    # await TelebotFunctions.process_request(user_id, #request_wish_type, #request_wish_day) <- На будущее
    result = await WebsiteInteraction.get_homework(request_data)

    response_exceptions = result['exceptions']
    response_text_data = result['data']['output_string']
    response_additional_links_data = result['data']['additional_links']

    if (response_exceptions):
        if ('log_in_error' in response_exceptions):
            await bot.delete_message(
                user_id,
                states[user_id].bot_last_message.message_id
            )

            await bot.send_message(
                user_id,
                'При попытке входа возникла ошибка.\n\nВозможно, вы ввели неверный логин/пароль. Проверьте правильность введенных данных и повторите попытку'
            )
        elif ('get_homework_error' in response_exceptions):
            await bot.delete_message(
                user_id,
                states[user_id].bot_last_message.message_id
            )

            await bot.send_message(
                user_id,
                'При попытке получения данных возникла ошибка.\n\nПовторите попытку.'
            )
    else:
        await bot.delete_message(user_id, states[user_id].bot_last_message.message_id)
        if (response_text_data != 'screenshot'):
            await bot.send_message(user_id, response_text_data)
        else:

            await bot.send_photo(user_id,
                                 FSInputFile(os.path.join(states[user_id].screenshots_path_absolute, 'Screenshot.png')))

            if (response_additional_links_data):

                await bot.send_message(user_id,
                                       ' | '.join(response_additional_links_data)
                                       )

            await TelebotFunctions.clear_directory(states[user_id].screenshots_path_absolute)

        if (result['data']['were_downloaded']):
            docs_path = states[user_id].docs_path_absolute
            files_list = os.listdir(docs_path)

            media = []

            if (files_list):
                for file_name in files_list:
                    file_path = os.path.join(docs_path, file_name)
                    media.append(InputMediaDocument(type='document', media=FSInputFile(file_path)))

                await bot.send_media_group(user_id, media=media)
                await TelebotFunctions.clear_directory(docs_path)

    await TelebotFunctions.render(call, StartPage, del_last=False)
