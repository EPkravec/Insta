import random
import time
from time import sleep
from selenium import webdriver
from multiprocessing import Process

from configLPT import my_tags, my_coments

pars_chek = False  # переменая для контроля спарсеных данный с сайта проверки настроек браузера на ликвидность


class LogicInstagramm:
    """
    Класс созадания сессии с инстаграмм и взаимодействия в ней (фоловинг, лайк, комментарии)
    """

    def __init__(self, login, password):
        self.login: str = login
        self.password: str = password
        self.tags_defaul: list = my_tags
        self.coments_defaul: list = my_coments
        self.url_instagramm: str = 'https://www.instagram.com/'
        self.url_check: str = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        self.time_sleep_login: int = random.randint(5, 8)
        self.time_sleep: int = random.randint(20, 30)
        self.time_sleep_scroll: int = random.randint(10, 12)
        self.count_tags: int = 1
        self.count_coments: int = 1
        self.ignore_link: int = 9
        self.repeat_link: bool = False
        self.max_like_day: int = 115
        self.max_like_hour = self.max_like_day // 24
        self.min_time_wait_for_like = (60 // self.max_like_hour) * 60
        self.time_sleep_like: int = random.randint(self.min_time_wait_for_like - 20, self.min_time_wait_for_like + 20)
        self.count_scroll: int = 1  # 12 шт за один скролл в теории
        self.datatime = self.datatime()

    def datatime(self):
        """
        Ф-я отображения времени ( не работате ((( )))
        :return:
        """
        while True:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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

    def coments(self):
        """
        Ф-я определения комментариев из основного списка, зависит от настройки self.count_coments по умолчанию 1
        :return: список комментариев
        """
        random.shuffle(self.coments_defaul)
        my_coments = self.coments_defaul[:self.count_coments]
        my_coments = ''.join(my_coments)
        return my_coments

    def tags(self):
        """
        Ф-я определения тегов из основного списка, зависит от настройки self.count_tags по умолчанию 1
        :return: список тегов
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
        my_coments = self.coments()

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
                print(
                    f'{self.datatime} [{self.login}] - {self.max_like_hour} лайка в час, Ссылок для работы - {len(post_urls)}')
                poisk = False
            else:
                continue

        lik1 = 0  # счетчик лайка
        com1 = 0  # счетчик комментариев
        flow1 = 0  # счетчик подписок

        for url in post_urls:
            browser.get(url)
            sleep(self.time_sleep)
            # заходим на фото
            browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div').click()
            sleep(self.time_sleep)
            # заходим на акаутн
            browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div/span/a').click()
            sleep(self.time_sleep)

            # заходим на фото в акауте
            browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a').click()

            sleep(self.time_sleep)
            # заходим на фото в акауте
            # browser.get(post_urls_top_ac)
            # sleep(self.time_sleep)
            # # смотрим количество лайковна фото в акауте
            # count_like_button = browser.find_element_by_xpath(
            #     '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span')
            # sleep(self.time_sleep)
            # count_like = count_like_button.text
            # count_like = int(count_like.split(' ')[0])
            # print(f'{self.datatime} [{self.login}] - Количество лайков под фото - {count_like}')
            # loop_count = int(count_like / 12)
            # # смотрим список людей которые лайкнули фото в акауте
            # count_like_button.click()
            # sleep(self.time_sleep)
            # # ищем всех кто лайкнул
            # like_pipl = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
            # sleep(self.time_sleep)
            # like_pipl_urls = []
            #
            # for i in range(1, loop_count + 1):
            #     browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", like_pipl)
            #     sleep(self.time_sleep_scroll)
            #
            # all_hrefs = like_pipl.find_elements_by_tag_name('a')
            #
            # for url in all_hrefs:
            #     url = url.get_attribute('href')
            #     like_pipl_urls.append(url)
            #
            # like_pipl_urls = set(like_pipl_urls)
            # like_pipl_urls = list(like_pipl_urls)
            #
            # for pipl in like_pipl_urls:
            #     print(f'{self.datatime} [{self.login}] - Заходим к - {pipl}')
            #     # заходим на чеорвека который лайкнул
            #     browser.get(f'https://www.instagram.com/{pipl}/')
            #     sleep(self.time_sleep_scroll)
            #     # проверяем закрыт ли аккаунт
            #     close_ac = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[1]/div/h2')
            #     sleep(self.time_sleep)
            #     count_like = close_ac.text
            #     if 'Это закрытый аккаунт' == count_like:
            #         continue
            #     # подписываемся
            #     browser.find_element_by_xpath(
            #         '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button').click()
            #     flow1 += 1
            #     sleep(self.time_sleep)
            #     # ставим комент
            #     browser.find_element_by_xpath(
            #         '/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a').click()
            #     sleep(self.time_sleep)
            #     comment = browser.find_element_by_xpath(
            #         '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea').click()
            #     sleep(self.time_sleep)
            #     comment.send_keys(my_coments)
            #     sleep(self.time_sleep)
            #     browser.find_element_by_xpath(
            #         '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button[2]').click()
            #     com1 += 1
            #     sleep(self.time_sleep)
            #     # ставим лайк
            #     browser.find_element_by_xpath(
            #         '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
            #     lik1 += 1
            #     sleep(self.time_sleep)
            #     print(f'{self.datatime} [{self.login}] - Лайк по тегу [{my_hashtags}] адрес - {url}')
            #
            #     print(
            #         f'{self.datatime} [{self.login}] - Лайков за сутки [{lik1}/{self.max_like_day}]')
            #     print(
            #         f'{self.datatime} [{self.login}] - Комментариев за сутки [{com1}/{self.max_like_day}]')
            #     print(
            #         f'{self.datatime} [{self.login}] - Подписок за сутки [{flow1}/{self.max_like_day}]')
            #
            #     sleep(self.time_sleep_like)
            #
            #     # todo сделать условие проверки наличия ссылок для лайков, переходов и прочее
            #     if lik1 >= self.max_like_day and com1>= self.max_like_day and flow1>= self.max_like_day:
            #         print(f'{self.datatime} [{self.login}] - Дастигнут суточный лимит лайков комментариев и подписок')
            #         print(f'{self.datatime} [{self.login}] - Завершаю сессию')
            #         browser.close()
            #         browser.quit()
            #         break
            #     else:
            #         continue


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
    # Process(target=run, args=('Rabota_v_dekreteizdoma', '123456789q')).start()
    # sleep(5)
    Process(target=run, args=('dekret_rabota_olga', '123456789q')).start()
    # sleep(5)
    # Process(target=run, args=('rabo.tavradosti', '123456789qQ')).start()
