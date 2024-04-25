import asyncio

from Core.Modules.Libs.WebsiteIntercationLibs import *

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
        browser = await launch({'headless': False, 'args': ['--disable-infobars', '--disable-features=DownloadBubble']})

        auth_data = request_data['auth_data']
        req_type = request_data['type']
        req_day = int(request_data['day'])
        req_by_id = request_data['by_id']

        response = {
            'data': {
                'output_string': '',
                'additional_links': [],
                'were_downloaded': False
            },
            'exceptions': ''
        }

        page: Page = await browser.newPage()

        await page.setViewport({'width': 2535, 'height': 1126})
        await page.goto('https://e-school.obr.lenreg.ru/authorize/')

        if (await WebsiteInteraction.log_in(auth_data, page)):
            if (page.url.endswith('/main/')):
                await asyncio.sleep(0.9)
                await page.click('div.journal > div.readmore.center.ng-binding')

            try:
                exercises_data = await WebsiteInteraction.get_exercises(req_day, req_by_id, req_type, page)
                response['data'] = exercises_data

            except pyppeteer.errors as Error:
                response['exceptions'] += 'request_process_error'
                await WebsiteInteraction.log_out(page)
                return response

            await WebsiteInteraction.log_out(page)

        else:
            response['exceptions'] += ' log_in_error'
            return response

        await browser.close()

        return response

    @staticmethod
    async def log_in(auth_data: dict[str, str], page: Page) -> bool:
        login = auth_data.get('login', '-')
        password = auth_data.get('password', '-')

        await page.waitForSelector('span.selection')
        await page.click('span.selection')

        await page.type('input.select2-search__field', 'МОБУ "СОШ "ЦО "Кудрово"')

        await asyncio.sleep(0.7)
        schools = await page.querySelectorAll('li.select2-results__option')
        await schools[1].click()

        await page.type('[name="loginname"]', login)
        await page.type('[name="password"]', password)

        await page.click('div.primary-button')

        try:
            await page.waitForNavigation({'url': 'https://e-school.obr.lenreg.ru/app/school/main/', 'timeout': 2000})
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
        offset: int = await WebsiteInteraction.days_until_next_weekday(weekday_num)
        date: str = await WebsiteInteraction.get_date(offset)
        url_pattern: re.Pattern = re.compile(r'https?://\S+')
        were_downloaded: bool = False
        output_string: str = ''
        links: list = []

        await page.waitForXPath(f'//span[contains(text(), "{date}")]')
        date_element = (await page.xpath(f'//span[contains(text(), "{date}")]'))[0]
        table = (await date_element.xpath(f'./../../..'))[0]
        rows = await table.xpath('./tr[@class="ng-scope"]')

        buttons = await table.xpath('.//label[@title="показать/свернуть все содержимое таблицы"]')
        for button in buttons:
            try:
                await button.click()
            except pyppeteer.errors.ElementHandleError as Error:
                pass

        paperclips = await table.xpath('.//assign-attachments')

        docs_path = "\\".join([os.getcwd(), "Core", "Temp_Files", "Docs", f"User_{user_id}"])

        await page._client.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': docs_path})

        url_check_text: str = await (await table.getProperty('textContent')).jsonValue()
        match = re.findall(url_pattern, url_check_text)
        if (match):
            links += match

        for paperclip in paperclips:
            try:
                await asyncio.sleep(0.1)
                await paperclip.click()
                await page.waitForSelector('div.visible')
                files_table: ElementHandle = await page.querySelector('div.visible')
                files = await files_table.xpath('.//a')
                for file in files:
                    await file.click({'delay': 200})
                    were_downloaded = True
                await paperclip.click()
            except pyppeteer.errors.ElementHandleError as Error:
                await date_element.click()

        joinable_list = []
        if (request_type == 'text'):
            for row in rows:
                lesson_num: str = await WebsiteInteraction.get_element_text('td.num_subject', row)
                lesson_name: str = await WebsiteInteraction.get_element_text('* > a.subject', row)
                lesson_task: str = await WebsiteInteraction.get_element_text('* > div.three_dots', row)
                lesson_time_room: str = await WebsiteInteraction.get_element_text('* > div.time', row)

                text = f"{lesson_num} | {lesson_name.center(34)} | {lesson_time_room.center(23)} | {lesson_task}"

                joinable_list.append(text)

            output_string = f'\n\n{"="*50}\n\n'.join(joinable_list)
        else:
            screenshot_path = "\\".join([os.getcwd(), "Core", "Temp_Files", "Screenshots", f"User_{user_id}", "Screenshot.png"])
            await table.screenshot({'path': screenshot_path})
            output_string = 'screenshot'

        return {
            'output_string': output_string,
            'additional_links': links[::2],
            'were_downloaded': were_downloaded
        }

    @staticmethod
    async def log_out(page: Page) -> bool:
        await page.click("li.no_separator")
        await page.waitForSelector('button.btn-primary')
        await asyncio.sleep(0.4)
        await page.click('button.btn-primary', {'clickCount': 4})
        await page.waitForNavigation({'url': 'https://e-school.obr.lenreg.ru/logout'})

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
