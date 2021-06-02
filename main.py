import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from configLPT import my_tags
from multiprocessing import Process


# options.headless = True/False # безголовый режим не видим браузера ВАЩЕ !!!!!!!!!!!!!!
class LogicInstagramm:
    """
    Класс созадания сессии с инстаграмм и взаимодействия в нем (фоловинг, лайк, комментарии)
    """

    def __init__(self, login, password):
        self.login: str = login
        self.password: str = password
        self.tags: list = my_tags
        self.headless: bool = True
        self.browser = False
        self.url_instagramm: str = 'https://www.instagram.com/'
        self.url_check: str = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.time_speep: int = random.randint(15, 30)

    def chek(self):
        """
        Проверка опций chromedriver-а на валиндность и схожесть с человеком
        """
        options = webdriver.ChromeOptions()

        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.77 Safari/537.36')

        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')

        if self.headless:
            options.headless = True

        browser = webdriver.Chrome(options=options)
        browser.set_window_rect(width=630, height=930)
        browser.get(self.url_check)

    def options(self):
        """
        Ф-я настроек для браузера
        """
        options = webdriver.ChromeOptions()

        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.77 Safari/537.36')

        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')

        if self.headless:
            pass
        else:
            options.headless = False

        browser = webdriver.Chrome(options=options)
        browser.set_window_rect(width=630, height=930)
        return browser

    def pars_url_chek(self):
        """
        Ф-я парсинга сайта intoli.com ипроверка на ликвидность chromedriver-а
        :return: True - если прошел проверку на ликвидность chromedriver-а
        :return: False - если  не прошел проверку  на ликвидность chromedriver-а
        """
        try:
            print('ты человек')
            return True
        except:
            print('ты бот')
            return False

    def go_instagramm(self):
        """
        Ф-я подключения к инстаграмм поехали
        """
        random.shuffle(self.tags)
        my_hashtags = self.tags[:1]
        my_hashtags = ''.join(my_hashtags)

        if self.pars_url_chek:

            browser = self.options()
            browser.get(self.url_instagramm)
            sleep(self.time_speep)

            user_input = browser.find_element_by_css_selector('input[name="username"]')
            sleep(self.time_speep)
            user_input.send_keys(self.login)
            sleep(self.time_speep)

            password_input = browser.find_element_by_css_selector('input[name="password"]')
            sleep(self.time_speep)
            password_input.send_keys(self.password)
            sleep(self.time_speep)

            login = browser.find_element_by_css_selector('button[type="submit"]')
            sleep(self.time_speep)
            login.click()
            sleep(self.time_speep)

            login_button = browser.find_element_by_css_selector('span[role="link"]')
            sleep(self.time_speep)
            login_button.click()
            sleep(self.time_speep)

            profil_button = browser.find_element_by_css_selector('a[class="-qQT3"]')
            sleep(self.time_speep)
            profil_button.click()
            sleep(self.time_speep)

            serc_input = browser.find_element_by_css_selector('input[placeholder="Поиск"]')
            sleep(self.time_speep)
            serc_input.send_keys(my_hashtags)
            sleep(self.time_speep)
            serc_input.send_keys(Keys.ENTER)
            sleep(self.time_speep)
            serc_input.send_keys(Keys.ENTER)
            sleep(self.time_speep)









            browser.get(f"https://www.instagram.com/explore/tags/{my_hashtags}/")

# if __name__ == '__main__':
#     a = Process(target=job)
#     a.start()
#     b = Process(target=job)
#     b.start()
#     c = Process(target=job)
#     c.start()
