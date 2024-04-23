from Core.Modules.Libs.WebsiteIntercationLibs import *


test_auth_data = {
        'login': 'ЗахаровЕ9',
        'password': '5084433'
    }

test_request_data = {
    'auth_data': test_auth_data,
    'type': 'text'
}


async def days_until_next_weekday(target_weekday: int) -> int:
    weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    current_day_index = datetime.now().weekday()

    difference = target_weekday - current_day_index

    return difference

    # 0 - Monday, 1 - Tuesday,...

async def get_homework(request_data: dict) -> dict[str, str]:
    auth_data = request_data['auth_data']
    req_type = request_data['type']

    exceptions: str = ''
    #  for example: log_in_error / get_homework_error etc.

    response = {
        'data': {
            'text_data': '',
            'additional_files': [],
        },
        'exceptions': ''
    }

    browser = await launch({'headless': False, 'start-maximized': True})
    page = await browser.newPage()

    await page.setViewport({'width': 2535, 'height': 1126})
    await page.goto('https://e-school.obr.lenreg.ru/authorize/')

    if (await log_in(auth_data, page)):
        await asyncio.sleep(5)

        #  get_exercieses()

        await asyncio.sleep(5)

        await log_out(page)
    else:
        response['exceptions'] += ' log_in_error'
        return response

    await asyncio.sleep(5)
    await page.screenshot({'path': 'example.png'})
    await browser.close()

    return response


async def log_in(auth_data: dict[str, str], page) -> bool:
    login = auth_data.get('login', '-')
    password = auth_data.get('password', '-')

    await page.waitForSelector('span.selection')
    await page.click('span.selection')

    await page.type('input.select2-search__field', 'МОБУ "СОШ "ЦО "Кудрово"')
    await asyncio.sleep(0.6)

    schools = await page.querySelectorAll('li.select2-results__option')
    await schools[1].click()

    await page.type('[name="loginname"]', login)
    await page.type('[name="password"]', password)

    await page.click('div.primary-button')

    await asyncio.sleep(1.5)
    if (page.url != 'https://e-school.obr.lenreg.ru/app/school/main/'):
        return False

    await asyncio.sleep(1)

    try:
        await page.waitForSelector('button[type="button"]', timeout=4000)
        print('Confirmed security button')
        await page.click('button[type="button"]')
    except pyppeteer.errors.TimeoutError as Error:
        print(Error)

    return True

async def get_exercises(date:str):
    pass

async def log_out(page) -> bool:
    await page.click("li.no_separator")
    await page.waitForSelector('button.btn')
    await page.click('button.btn')

    return True


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_homework(test_request_data))
    print(result)

    response_exceptions = result['exceptions']
    response_text_data = result['data']['text_data']
    response_additional_files_data = result['data']['additional_files']

    if (response_exceptions):
        if (response_exceptions == 'log_in_error'):
            print('There is log_in_error.')
        elif (response_exceptions == 'get_homework_error'):
            print('There is get_homework_error.')
    else:
        print('No exceptions!')
        if (response_text_data != 'screenshot'):
            print(response_text_data)
        else:
            print('Screenshot!')


