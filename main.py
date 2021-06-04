import os
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from configLPT import my_tags
from multiprocessing import Process

pars_chek = False

class LogicInstagramm:
    """
    Класс созадания сессии с инстаграмм и взаимодействия в нем (фоловинг, лайк, комментарии)
    """
    def __init__(self, login, password):
        self.login: str = login
        self.password: str = password
        self.tags_defaul: list = my_tags
        self.url_instagramm: str = 'https://www.instagram.com/'
        self.url_check: str = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.time_sleep: int = random.randint(15, 30)
        self.time_sleep_scroll: int = random.randint(2, 5)  # /12 надо подуматькак сделать
        self.count_scroll: int = 5
        self.count_tags: int = 5
        self.ignore_link: int = 9
        self.browser = webdriver.Chrome(r".\chromedriver.exe", options=self.options_argument())
        self.browser.set_window_rect(width=630, height=930)


    def close_browser(self):
        self.browser.close()
        self.browser.quit()
        os.system('TASKKILL /f /IM chromedriver.exe')

    def options_argument(self):
        """
        Ф-я настроеки для браузера
        """
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.77 Safari/537.36')
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        return options

    def pars_url_chek(self):
        """
        Ф-я парсинга сайта intoli.com ипроверка на ликвидность chromedriver-а
        :return: True - если прошел проверку на ликвидность chromedriver-а
        :return: False - если  не прошел проверку на ликвидность chromedriver-а
        """
        global pars_chek
        _browser = self.browser
        _browser.get(self.url_check)
        a = _browser.find_element_by_id("user-agent-result").value_of_css_property('background-color')
        b = _browser.find_element_by_id("webdriver-result").value_of_css_property('background-color')
        c = _browser.find_element_by_id("chrome-result").value_of_css_property('background-color')
        d = _browser.find_element_by_id("permissions-result").value_of_css_property('background-color')
        e = _browser.find_element_by_id("plugins-length-result").value_of_css_property('background-color')
        g = _browser.find_element_by_id("languages-result").value_of_css_property('background-color')

        if a == b == c == d == e == g == 'rgba(200, 216, 109, 1)':
            print('user_agent_result - OK')
            print('webdriver_result - OK')
            print('chrome_result - OK')
            print('permissions_result -OK')
            print('plugins_length_result - OK')
            print('languages_result - OK')
            _browser.close()
            _browser.quit()
            sleep(5)
            pars_chek = True
            return pars_chek
        else:
            print('Инстаграм будет видеть вас как бота, нужно проверить все настройки')
            _browser.close()
            _browser.quit()
            self.close_browser()

        pars_chek = False
        return pars_chek

    def login_insta(self):
        """
        Ф-я подключения к инстаграм после проверки опций браузера
        """

        if pars_chek:
            browser = self.browser
            browser.get(self.url_instagramm)
            sleep(3)
            user_input = browser.find_element_by_css_selector('input[name="username"]')
            # sleep(self.time_speep)
            user_input.send_keys(self.login)
            # sleep(self.time_speep)

            password_input = browser.find_element_by_css_selector('input[name="password"]')
            # sleep(self.time_speep)
            password_input.send_keys(self.password)
            # sleep(self.time_speep)

            login = browser.find_element_by_css_selector('button[type="submit"]')
            # sleep(self.time_speep)
            login.click()
            # sleep(self.time_speep)
            sleep(5)

        else:
            print('Вход в инстаграм не совершен')



    # def tags(self):
    #     """
    #     Ф-я пределения тегов, возвращает count_tags тег по умолчанию 1
    #     """
    #     random.shuffle(self.tags_defaul)
    #     # my_hashtags = self.tags_defaul[:self.count_tags]
    #     my_hashtags = self.tags_defaul[:1]
    #     my_hashtags = ''.join(my_hashtags)
    #     return my_hashtags

    # def list_link_to_tags_for_(self):
    #     """
    #     Ф-я получения списка ссылок на фото по тегам
    #
    #     """
    #     # post_urls = []
    #     my_hashtags = self.tags()
    #     browser = self.browser
    #     # for my_hashtag in my_hashtags:
    #     browser.get(f'https://www.instagram.com/explore/tags/{my_hashtags}/')
    #     for scroll in range(1, self.count_scroll):
    #         browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    #
    #     hrefs = browser.find_elements_by_tag_name('a')
    #     post_urls = [item.get_attribute('href') for item in hrefs if '/p' in item.get_attribute('href')]
    #     del post_urls[0:self.ignore_link]
    #     post_urls = set(post_urls)
    #     post_urls = list(post_urls)
    #
    #     return post_urls

    # def like_by_tags(self):
    #     browser = self.conect_insta()
    #
    #     pass
    #
    # def go_instagramm(self):
    #     """
    #     Ф-я подключения к инстаграмм поехали
    #     """
    #     random.shuffle(self.tags)
    #     my_hashtags = self.tags[:1]
    #     my_hashtags = ''.join(my_hashtags)
    #
    #     if self.pars_url_chek:
    #         browser = self.options_insta()
    #         browser.get(self.url_instagramm)
    #         sleep(5)
    #         # sleep(self.time_speep)
    #
    #         browser.get(f'https://www.instagram.com/explore/tags/{my_hashtags}/')
    #         # sleep(self.time_speep)
    #         sleep(5)
    #         # todo тут настройку потом сделать СКРОЛОВ ЗАВИСЯЩУЮ ОТ ОТ КОЛИЧЕСТВА ЛАЙКОВ которые хотим поставить или других действий
    #         for scroll in range(1, self.count_scroll):
    #             browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    #             sleep(5)
    #
    #         hrefs = browser.find_elements_by_tag_name('a')
    #         post_urls = [item.get_attribute('href') for item in hrefs if '/p' in item.get_attribute('href')]
    #
    #         # todo тут настройку потом сделать по колличеству лайков и вывести лайки в одельную функцию
    #         for url in post_urls:
    #             browser.get(url)
    #             sleep(5)
    #             # sleep(self.time_sleep)
    #             like_button = browser.find_element_by_xpath(
    #                 '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
    #             # sleep(2)
    #             like_button.click()


if __name__ == '__main__':
    a = LogicInstagramm('dekret_rabota_olga', '123456789q')
    a.pars_url_chek()
    a.login_insta()

    # a.list_link_to_tags_for_()

# a.go_instagramm()
#     a = Process(target=job)
#     a.start()
#     b = Process(target=job)
#     b.start()
#     c = Process(target=job)
#     c.start()
