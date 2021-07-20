import os
import random
import datetime
from time import sleep
from datetime import datetime
from selenium import webdriver
from multiprocessing import Process

from configLPT import my_tags, my_coments

lik1 = 0


def datatime_m():
    """
    Ф-я отображения времени
    """
    while 1:
        CurrentTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        break
    return CurrentTime


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

        self.time_sleep: int = random.randint(25, 30)
        self.time_sleep_login: int = random.randint(5, 8)
        self.time_sleep_scroll: int = random.randint(10, 12)

        self.count_tags: int = 1
        self.count_coments: int = 1

        self.max_action: int = 115
        self.max_action_hour: int = self.max_action // 24
        self.min_time_wait_for_action: int = (60 // self.max_action_hour) * 60
        self.sleeping: int = random.randint(self.min_time_wait_for_action - 20, self.min_time_wait_for_action + 20)

        self.count_scrolling: int = 10

        self.browser = None

    def options_argument(self):
        """
        Ф-я определения настроек для chromedriver-а в котором будем работать
        """
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.77 Safari/537.36')
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        return options

    def run_browser(self):
        """
        Ф-я запуска браузера
        """
        self.browser = webdriver.Chrome(options=self.options_argument())
        self.browser.set_window_rect(width=750, height=1050)

        print(f'{datatime_m()} [{self.login}] - Привет приступим к работе')
        print(f'{datatime_m()} [{self.login}] - Пауза между основными операциями ~ {self.time_sleep} сек')
        print(f'{datatime_m()} [{self.login}] - Пауза между скролами ~ {self.time_sleep_scroll} сек')
        print(f'{datatime_m()} [{self.login}] - Пауза между действиями ~ {self.sleeping:} сек')
        print(f'{datatime_m()} [{self.login}] - Количество действий в сутки {self.max_action}')
        print(f'{datatime_m()} [{self.login}] - Количество действий в час {self.max_action_hour}')
        print(f'{datatime_m()} [{self.login}] - Количество используемых тегов {self.count_tags}')
        print(f'{datatime_m()} [{self.login}] - Количество используемых коментариев {self.count_coments}')

    def close_browser(self):
        """
        Ф-я закрытия браузера
        """
        self.browser.close()
        self.browser.quit()

    def xpath_exists(self, url):
        """
        Ф-я проверяет по xpath существует ли элемент на странице
        """
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except:
            exist = False
        return exist

    def coments(self):
        """
        Ф-я определения комментариев из основного списка, зависит от настройки self.count_coments по умолчанию 1
        """
        random.shuffle(self.coments_defaul)
        my_coments = self.coments_defaul[:self.count_coments]
        my_coments = ''.join(my_coments)
        return my_coments

    def tags(self):
        """
        Ф-я определения тегов из основного списка, зависит от настройки self.count_tags по умолчанию 1
        """
        random.shuffle(self.tags_defaul)
        my_hashtags = self.tags_defaul[:self.count_tags]
        my_hashtags = ''.join(my_hashtags)
        return my_hashtags

    def login_go(self):
        """
        Ф-я входа в инстаграмм учетной записью.
        """
        browser = self.browser
        browser.get(self.url_instagramm)
        sleep(self.time_sleep_login)

        user_input = browser.find_element_by_css_selector('input[name="username"]')
        user_input.send_keys(self.login)

        password_input = browser.find_element_by_css_selector('input[name="password"]')
        password_input.send_keys(self.password)

        login = browser.find_element_by_css_selector('button[type="submit"]')
        login.click()
        sleep(self.time_sleep_login)

    def like_photo_by_hashtag(self):
        """
        Ф-я ставит лайки по hashtag
        """
        my_hashtags = self.tags()

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{my_hashtags}/')
        sleep(self.time_sleep)

        for i in range(1, self.count_scrolling):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(self.time_sleep_scroll)

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                sleep(self.time_sleep_scroll)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                sleep(self.sleeping)
            except:
                self.close_browser()

    def put_exactly_like(self, userpost):
        """
        Ф-я ставит лайк на пост по прямой ссылке
        """
        global lik1
        browser = self.browser
        browser.get(userpost)
        sleep(self.time_sleep)
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f'{datatime_m()} [{self.login}] - Такого поста не существует {userpost}')
            self.close_browser()
        else:
            sleep(self.time_sleep)
            lik1 += 1
            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            sleep(self.time_sleep)
            print(f'{datatime_m()} [{self.login}] -  [{lik1}/{self.max_action}]')
            print(f'{datatime_m()} [{self.login}] - Лайк поста - {userpost}')
            self.close_browser()

    def get_all_posts_urls(self, userpage):
        """
        Ф-я собирает ссылки на все посты пользователя
        """
        browser = self.browser
        browser.get(userpage)
        sleep(self.time_sleep)
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f'{datatime_m()} [{self.login}] - Такого пользователя не существует, провете юрл')
            self.close_browser()
        else:
            sleep(self.time_sleep)
            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_urls.append(href)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(self.time_sleep_scroll)
            file_name = userpage.split("/")[-2]
            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)
            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    def put_many_likes(self, userpage):
        """
        Ф-я ставит лайки по ссылке на аккаунт пользователя
        """
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        sleep(self.time_sleep)
        browser.get(userpage)
        sleep(self.time_sleep)
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()
            for post_url in urls_list[0:6]:
                try:
                    browser.get(post_url)
                    sleep(self.time_sleep)
                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    sleep(self.time_sleep)
                    print(f'{datatime_m()} [{self.login}] -  [{lik1}/{self.max_action}]')
                    print(f'{datatime_m()} [{self.login}] - Лайк поста - {post_url}')
                except:
                    self.close_browser()

        self.close_browser()

    def get_all_followers(self, userpage):
        """
        Ф-я подписки на всех подписчиков переданного аккаунта
        """
        browser = self.browser
        browser.get(userpage)
        sleep(self.time_sleep)
        file_name = userpage.split("/")[-2]
        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print(f"{datatime_m()} [{self.login}] - Папка {file_name} уже существует!")
        else:
            print(f"{datatime_m()} [{self.login}] - Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f'{datatime_m()} [{self.login}] - Такого пользователя не существует, провете юрл')
            self.close_browser()
        else:
            sleep(self.time_sleep)
            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.get_attribute('title')
            # если количество подписчиков больше 999, убираем из числа запятые
            if ',' in followers_count:
                followers_count = int(''.join(followers_count.split(',')))
            else:
                followers_count = int(followers_count)
            print(f"{datatime_m()} [{self.login}] - Количество подписчиков: {followers_count}")
            sleep(self.time_sleep)
            loops_count = int(followers_count / 12)
            followers_button.click()
            sleep(self.time_sleep)
            followers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    sleep(self.time_sleep_scroll)
                all_urls_div = followers_ul.find_elements_by_tag_name("li")
                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)
                # сохраняем всех подписчиков пользователя в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")
                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()
                    for user in users_urls[0:10]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'{datatime_m()} [{self.login}] - Мы уже подписаны на {user}')
                                        continue
                            except:
                                print(f'{datatime_m()} [{self.login}] - Файл со ссылками ещё не создан!')
                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]
                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):
                                print(f"{datatime_m()} [{self.login}] - Это наш профиль, уже подписан")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(
                                    f"{datatime_m()} [{self.login}] - Уже подписаны, на {page_owner} пропускаем итерацию")
                            else:
                                sleep(self.time_sleep)
                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(
                                            f'{datatime_m()} [{self.login}] - Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except:
                                        print(
                                            f'{datatime_m()} [{self.login}] - Запросили подписку на пользователя - не удалось')
                                else:
                                    try:
                                        if self.xpath_exists(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(
                                                f'{datatime_m()} [{self.login}] - Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button").click()
                                            print(
                                                f'{datatime_m()} [{self.login}] - Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except:
                                        print(
                                            f'{datatime_m()} [{self.login}] - Запросили подписку на пользователя - не удалось')
                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)
                                sleep(self.time_sleep)
                        except:
                            self.close_browser()
            except:
                self.close_browser()
        self.close_browser()


def run(login, password):
    """
    Ф-я для запуска мультипроцесоов
    :param login: логин от интаграмм
    :param password: пароль от интаграмм
    """

    instagramm = LogicInstagramm(login, password)
    print(
        '░░░░░░░░░░░░▄▄░░░░░░░░░░░░░░\n'
        '░░░░░░░░░░░█░░█░░░░░░░░░░░░░\n'
        '░░░░░░░░░░░█░░█░░░░░░░░░░░░░\n'
        '░░░░░░░░░░█░░░█░░░░░░░░░░░░░\n'
        '░░░░░░░░░█░░░░█░░░░░░░░░░░░░\n'
        '██████▄▄█░░░░░██████▄░░░░░░░\n'
        '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
        '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
        '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
        '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
        '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
        '▓▓▓▓▓▓█████░░░░░░░░░██░░░░░░\n'
        '█████▀░░░░▀▀████████░░░░░░░░\n'
        '░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n'
        '╔════╗░░╔════╗╔═══╗░░░░░░░░░\n'
        '║████║░░║████║║███╠═══╦═════╗\n'
        '╚╗██╔╝░░╚╗██╔╩╣██╠╝███║█████║\n'
        '░║██║░░░░║██║╔╝██║███╔╣██══╦╝\n'
        '░║██║╔══╗║██║║██████═╣║████║\n'
        '╔╝██╚╝██╠╝██╚╬═██║███╚╣██══╩╗\n'
        '║███████║████║████║███║█████║\n'
        '╚═══════╩════╩════════╩═════╝\n')
    instagramm.run_browser()
    instagramm.login_go()
    instagramm.get_all_followers()


if __name__ == "__main__":
    Process(target=run, args=('Rabota_v_dekreteizdoma', '123456789q')).start()

    # Process(target=run, args=('dekret_rabota_olga', '123456789q')).start()

    # Process(target=run, args=('rabo.tavradosti', '123456789qQ')).start()
