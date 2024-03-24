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
    await state.update_data(wish=call.data.split('_')[1])
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
    request_wish_type = request_params_data['wish']
    request_wish_day = request_params_data['day']

    await state.clear()

    # await TelebotFunctions.process_request(user_id, #request_wish_type, #request_wish_day) <- На будущее

    await TelebotFunctions.render(call, StartPage)
