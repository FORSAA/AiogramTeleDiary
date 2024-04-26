import asyncio, traceback

from Core.Modules.Libs.WebsiteIntercationLibs import *

BROWSER_ARGS: dict = {
    'headless': True,
    'args': ['--disable-infobars', '--disable-features=DownloadBubble', '--start-fullscreen']
}

test_auth_data = {
        'login': 'ЗахаровЕ9',
        'password': '5084433'
    }

test_request_data = {
    'auth_data': test_auth_data,
    'type': 'text',
    'day': 3,
    'by_id': 958
}


class WebsiteInteraction:

    @staticmethod
    async def get_element_text(selector, row) -> str:
        element = await row.querySelector(selector)
        if element:
            return (await (await element.getProperty('textContent')).jsonValue()).strip().replace('\n', '').replace('\t', '')
        else:
            return ''

    @staticmethod
    async def get_date(offset: int = 0) -> str:
        months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
                  "декабря"]
        today: datetime = datetime.today()+timedelta(days=offset)

        day_num: str = today.strftime("%d")

        month: str = months[int(today.strftime("%m"))-1]

        weekday: str = today.strftime("%A")
        weekday: str = weekday[0].upper()+weekday[1:]

        year: str = today.strftime("%Y")

        return f'{weekday}, {day_num} {month} {year} г.'

    @staticmethod
    async def days_until_next_weekday(target_weekday: int) -> int:
        # weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

        current_day_index = datetime.now().weekday()

        difference = target_weekday - current_day_index

        return difference

        # 0 - Monday, 1 - Tuesday,...

    @staticmethod
    async def get_homework(request_data: dict) -> dict[str, str]:
        browser = await launch(BROWSER_ARGS)

        auth_data = request_data['auth_data']
        req_type = request_data['type']
        req_day = int(request_data['day'])
        req_by_id = request_data['by_id']

        print(f'Request | By: {req_by_id} | Type: {req_type} | Day: {req_day}')

        response = {
            'data': {
                'output_string': '',
                'additional_links': [],
                'were_downloaded': False
            },
            'exceptions': ''
        }

        page: Page = await browser.newPage()

        await page.setViewport({'width': 2560, 'height': 2560})
        await page.goto('https://e-school.obr.lenreg.ru/authorize/')

        if (await WebsiteInteraction.log_in(auth_data, page)):
            print(f'Logined in | By: {req_by_id}')
            bot_local_message = await bot.send_message(req_by_id, 'Подготовка полученных данных...')
            try:
                exercises_data = await WebsiteInteraction.get_exercises(req_day, req_by_id, req_type, page)
                response['data'] = exercises_data
                await bot.delete_message(req_by_id, bot_local_message.message_id)

            except BaseException as Error:
                print(f'Process_error | By: {req_by_id} | Error: {Error}')
                traceback.print_exc()
                await bot.delete_message(req_by_id, bot_local_message.message_id)
                response['exceptions'] += 'get_homework_error'
                await WebsiteInteraction.log_out(page)
                await browser.close()
                return response

            print(f'Loging out | By: {req_by_id}')
            await WebsiteInteraction.log_out(page)

        else:
            print(f'Log in error | By: {req_by_id}')
            response['exceptions'] += ' log_in_error'
            await browser.close()
            return response

        await browser.close()

        return response

    @staticmethod
    async def log_in(auth_data: dict[str, str], page: Page) -> bool:
        login = auth_data['login']
        password = auth_data['password']

        await page.waitForSelector('span.selection')
        await page.click('span.selection')
        await page.type('input.select2-search__field', 'МОБУ "СОШ "ЦО "Кудрово"')

        await asyncio.sleep(0.68)
        schools = await page.querySelectorAll('li.select2-results__option')
        await schools[1].click()

        await page.type('[name="loginname"]', login)
        await page.type('[name="password"]', password)

        await page.click('div.primary-button')

        try:
            await page.waitForNavigation({'url': 'https://e-school.obr.lenreg.ru/app/school/main/', 'timeout': 2500})
        except pyppeteer.errors.TimeoutError as Error:
            return False

        try:
            await page.waitForSelector('button[type="button"]', timeout=2000)
            await page.click('button[type="button"]')
        except pyppeteer.errors.TimeoutError as Error:
            pass

        return True

    @staticmethod
    async def get_exercises(weekday_num: int, user_id: int, request_type: str, page: Page) -> dict:
        screenshot_path = "\\".join(
            [os.getcwd(), "Core", "Temp_Files", "Screenshots", f"User_{user_id}", "Screenshot.png"])
        docs_path = "\\".join(
            [os.getcwd(), "Core", "Temp_Files", "Docs", f"User_{user_id}"])

        offset: int = await WebsiteInteraction.days_until_next_weekday(weekday_num)
        date: str = await WebsiteInteraction.get_date(offset)

        print(f'Date: {date} | By: {user_id}')

        url_pattern: re.Pattern = re.compile(r'https?://\S+')
        were_downloaded: bool = False
        output_string: str = ''
        links: list = []

        if (page.url.endswith('/main/')):
            await asyncio.sleep(0.18)
            await page.click('div.journal > div.readmore.center.ng-binding')

        if (page.url.endswith('studentdiary/')):
            print(f'Got page, getting data | By: {user_id}')

        await page.waitForXPath(f'//span[contains(text(), "{date}")]/../../..')
        table = (await page.xpath(f'//span[contains(text(), "{date}")]/../../..'))[0]
        paperclips = await table.xpath('.//assign-attachments')
        rows = await table.xpath('./tr[@class="ng-scope"]')
        expand_buttons = await table.xpath('.//label[@title="показать/свернуть все содержимое таблицы"][@style = "display: block;"]')


        for expand_button in expand_buttons:
            try:
                await expand_button.click()
            except pyppeteer.errors.ElementHandleError as Error:
                pass

        await page._client.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': docs_path})

        table_text: str = await (await table.getProperty('textContent')).jsonValue()
        match = re.findall(url_pattern, table_text)
        if (match):
            links += match

        if (request_type == 'text'):
            joinable_list = []
            for row in rows:
                lesson_num: str = await WebsiteInteraction.get_element_text('td.num_subject', row)
                lesson_name: str = await WebsiteInteraction.get_element_text('* > a.subject', row)
                lesson_task: str = await WebsiteInteraction.get_element_text('* > div.three_dots', row)
                lesson_time_room: str = await WebsiteInteraction.get_element_text('* > div.time', row)

                text = f"{lesson_num} | {lesson_name.center(34)} | {lesson_time_room.center(23)} | {lesson_task}"

                joinable_list.append(text)

            output_string = f'\n\n{"="*34}\n\n'.join(joinable_list)
            print(f'Got text data | By: {user_id}')
        else:
            await asyncio.sleep(0.1)
            await table.screenshot({'path': screenshot_path})
            output_string = 'screenshot'
            print(f'Got screenshot | By: {user_id}')

        print(f'Check paperclips | By: {user_id}')
        for paperclip in paperclips:
            try:
                await paperclip.click()
                await page.waitForSelector('div.visible')
                files_table = await page.querySelector('div.visible')
                files = await files_table.xpath('.//a')
                for file in files:
                    await file.click()
                    were_downloaded = True
                    await asyncio.sleep(0.08)
                await paperclip.click()
                await asyncio.sleep(0.18)
            except pyppeteer.errors.ElementHandleError as Error:
                pass

        return {
            'output_string': output_string,
            'additional_links': links[::2],
            'were_downloaded': were_downloaded
        }

    @staticmethod
    async def log_out(page: Page) -> bool:
        await page.waitForSelector("li.no_separator")
        await page.click("li.no_separator")
        await page.waitForSelector('button.btn-primary')
        await asyncio.sleep(0.4)
        await page.click('button.btn-primary', {'clickCount': 4})
        await page.waitForNavigation({'url': 'https://e-school.obr.lenreg.ru/logout'}),

        return True


if __name__ == "__main__":
    result = asyncio.get_event_loop().run_until_complete(WebsiteInteraction.get_homework(test_request_data))
    print(result)

    response_exceptions = result['exceptions']
    response_text_data = result['data']['output_string']
    response_additional_links_data = result['data']['additional_links']

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

        if (response_additional_links_data):
            print(response_additional_links_data)