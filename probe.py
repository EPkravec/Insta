

import random
import time
from time import sleep
from selenium import webdriver
from multiprocessing import Process


from configLPT import my_tags

pars_chek = False  # переменая для контроля спарсеных данный с сайта проверки настроек браузера на ликвидность



class LogicInstagramm:
    """
    Класс созадания сессии с инстаграмм и взаимодействия в ней (фоловинг, лайк, комментарии)
    """

    def __init__(self, login, password):
        self.login: str = login
        self.password: str = password
        self.tags_defaul: list = my_tags
        self.url_instagramm: str = 'https://www.instagram.com/'
        self.url_check: str = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.time_sleep_login: int = random.randint(5, 8)
        self.time_sleep: int = random.randint(20, 30)
        self.time_sleep_scroll: int = random.randint(10, 12)
        self.count_tags: int = 1
        self.ignore_link: int = 9
        self.repeat_link: bool = False
        self.max_like_day: int = 115
        self.max_like_hour = self.max_like_day // 24
        self.min_time_wait_for_like = (60 // self.max_like_hour) * 60
        self.time_sleep_like: int = random.randint(self.min_time_wait_for_like - 20, self.min_time_wait_for_like + 20)
        self.count_scroll: int = 1  # 12 шт за один скролл в теории
        self.datatime: str = self.check_time()

    def time1(self):
        a = time.localtime()
        data = time.strftime("%Y-%m-%d %H:%M:%S", a)
        return data

    def check_time(self):
        while True:
            self.time1()
            return self.time1()

    def options_argument(self):
        """
        Ф-я определения настроек для chromedriver-а в котором будем работать
        :return: webdriver.ChromeOptions() с нашими настройками
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
        Ф-я парсинга результатов проверки настроек для chromedriver-а

        П.С. Пока не реализованно в связи с тем что при запуске ф-и в режие --headless,
        webdriver-result возвращает False

        :return: True - если прошел проверку на ликвидность chromedriver-а
        :return: False - если  не прошел проверку на ликвидность chromedriver-а
        """
        global pars_chek
        _browser = webdriver.Chrome(r".\chromedriver.exe", options=self.options_argument())
        _browser.set_window_rect(width=630, height=960)
        _browser.get(self.url_check)
        a = _browser.find_element_by_id("user-agent-result").value_of_css_property('background-color')
        b = _browser.find_element_by_id("webdriver-result").value_of_css_property('background-color')
        c = _browser.find_element_by_id("chrome-result").value_of_css_property('background-color')
        d = _browser.find_element_by_id("permissions-result").value_of_css_property('background-color')
        e = _browser.find_element_by_id("plugins-length-result").value_of_css_property('background-color')
        g = _browser.find_element_by_id("languages-result").value_of_css_property('background-color')

        if a == b == c == d == e == g == 'rgba(200, 216, 109, 1)':
            print(f'{self.datatime} [{self.login}] - user_agent_result - OK')
            print(f'{self.datatime} [{self.login}] - webdriver_result - OK')
            print(f'{self.datatime} [{self.login}] - chrome_result - OK')
            print(f'{self.datatime} [{self.login}] - permissions_result -OK')
            print(f'{self.datatime} [{self.login}] - plugins_length_result - OK')
            print(f'{self.datatime} [{self.login}] - languages_result - OK')
            _browser.close()
            _browser.quit()
            sleep(5)
            pars_chek = True
            return pars_chek
        else:
            print(
                f'{self.datatime} [{self.login}] - Инстаграмм будет видеть вас как бота, нужно проверить options_argument')
            print(f'{self.datatime} [{self.login}] - Бот запускать не буду ;)')
            _browser.close()
            _browser.quit()

        pars_chek = False
        return pars_chek

    def tags(self):
        """
        Ф-я определения тегов из основного списка, зависит от настройки self.count_tags по умолчанию 1
        :return:
        """
        random.shuffle(self.tags_defaul)
        my_hashtags = self.tags_defaul[:self.count_tags]
        my_hashtags = ''.join(my_hashtags)
        return my_hashtags

    def insta(self):
        """
        Ф-я созадания сессии подключения в инстаграмм, осуществление входа под учетными данными.
        На основе тегов ф-ии tags, получает список ссылок*:
            критерии для списка:
                - поспускаются первых Х (топ) ссылок на фото параметр self.ignore_link | по умолчанию 9
                - повторение юрл параметр self.repeat_link не допускается  | по умолчанию False

            критерии для лайков:

                - максимальное количество лайков в день параметр self.max_like_day | по умолчанию  120
                - максимальное количество лайков в час параметр self.max_like_hour | по умолчанию  1max_like_day // 24
                - время сна до следующего лайка не превышая лимит ---> зависимо от лайков <--- не трагать
                    параметр self.min_time_wait_for_like
                    параметр self.time_sleep_like


          * - юрл фотографии с заданными тегами, другие ссылки не учитываются
        """
        global sesion_clos, post_urls
        browser = webdriver.Chrome(options=self.options_argument())
        browser.set_window_rect(width=630, height=930)

        browser.get(self.url_instagramm)
        sleep(self.time_sleep_login)
        user_input = browser.find_element_by_css_selector('input[name="username"]')
        user_input.send_keys(self.login)
        password_input = browser.find_element_by_css_selector('input[name="password"]')
        password_input.send_keys(self.password)
        login = browser.find_element_by_css_selector('button[type="submit"]')
        login.click()
        sleep(self.time_sleep_login)

        my_hashtags = self.tags()

        print(f'{self.datatime} [{self.login}] - Ищем фоточки по тегу {my_hashtags}')
        browser.get(f'https://www.instagram.com/explore/tags/{my_hashtags}/')
        sleep(self.time_sleep_scroll)

        poisk = True
        while poisk:
            browser.execute_script("window.scrollBy(0,2000)")
            new_height = browser.execute_script("return document.body.scrollHeight")
            sleep(self.time_sleep_scroll)

            hrefs = browser.find_elements_by_tag_name('a')
            post_urls = []
            for item in hrefs:
                href = item.get_attribute('href')
                if '/p/' in href:
                    post_urls.append(href)

            if len(post_urls) > 50:  # todo  времнное значение, больше 54 ссылок не могу спарсить
                count_scroll = self.count_scroll
                self.count_scroll = count_scroll
                print(
                    f'{self.datatime} [{self.login}] - {self.max_like_hour} лайка в час, Ссылок для работы - {len(post_urls)}')
                del post_urls[0:self.ignore_link]
                poisk = False
            else:
                continue

        i = 0  # часовой счетчик лайка
        j = 0  # суточный счетчик лайка
        k = 0  # общий счетчик лайка

        for url in post_urls:
            browser.get(url)
            sleep(self.time_sleep)
            browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
            i += 1
            j += 1
            k += 1
            print(
                f'{self.datatime} [{self.login}] - лайк за час [{i}/{self.max_like_hour}] за сутки [{k}/{self.max_like_day}]')
            print(f'{self.datatime} [{self.login}] - Лайк по тегу [{my_hashtags}] адрес - {url}')
            sleep(self.time_sleep_like)
            if i >= self.max_like_hour:
                print(f'{self.datatime} [{self.login}] - Дастигнут часовой лимит лайков [{i}/{self.max_like_hour}]')
                i = 0
                sleep(self.time_sleep_like * 2)
                continue
            elif i >= self.max_like_day:
                print(f'{self.datatime} [{self.login}] - Дастигнут суточный лимит лайков [{k}/{self.max_like_day}]')
                j = 0
                sleep(self.time_sleep_like)
                print(f'{self.datatime} [{self.login}] - Пора отдохнуть или придумать новые настройки')
                browser.close()
                browser.quit()
                break
            else:
                continue


def run(login, password):
    """
    Ф-я для запуска мультипроцесоов
    :param login: логин от интаграмм
    :param password: пароль от интаграмм
    """

    instagramm = LogicInstagramm(login, password)

    print(f'==================================================================================================')
    print(f'                                  Привет {login}')
    print(f'==================================================================================================')
    print(f'====================================== Запустились ===============================================')
    print(f'================================ Я работать иди отдыхай ==========================================')
    print(f'====================================== Мои натройки ==============================================')
    print(f'{instagramm.datatime} [{login}] - Количество лайков за сутки - {instagramm.max_like_day} лайка(ов)')
    print(f'{instagramm.datatime} [{login}] - Количество лайков в час - {instagramm.max_like_hour} лайка(ов)')
    print(
        f'{instagramm.datatime} [{login}] - Количество игнорируемых фото при поиске по тегу - {instagramm.ignore_link} фоток')
    instagramm.insta()


if __name__ == "__main__":
    Process(target=run, args=('Rabota_v_dekreteizdoma', '123456789q')).start()
    sleep(5)
    Process(target=run, args=('dekret_rabota_olga', '123456789q')).start()
    sleep(5)
    Process(target=run, args=('rabo.tavradosti', '123456789qQ')).start()
