import random
import datetime
from time import sleep
from datetime import datetime
from selenium import webdriver
from multiprocessing import Process

from configLPT import my_tags, my_coments


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
        self.max_action_hour = self.max_action // 24
        self.min_time_wait_for_action = (60 // self.max_action_hour) * 60
        self.sleeping: int = random.randint(self.min_time_wait_for_action - 20, self.min_time_wait_for_action + 20)

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

    def insta(self):
        """
        Ф-я созадания сессии подключения в инстаграмм, осуществление входа под учетными данными.
        по тегу ищем фотографии, заходим на автора этих фото --> смотрим его / ее фото -->
        смотрим количество лайков, смотрим кто лайкал, заходим на каждого кто лайкал,
        подписываемся, смотрим фото --> у фотоски ставим лайк и коммент

        выводим из этого цикла при привышении количесва max_action
        """
        # запуск брузера для работы
        browser = webdriver.Chrome(options=self.options_argument())
        browser.set_window_rect(width=750, height=1050)

        print(f'{datatime_m()} [{self.login}] - Привет приступаем, ну что ж приступим к работе')
        print(f'{datatime_m()} [{self.login}] - Пауза между основными операциями ~ {self.time_sleep} сек')
        print(f'{datatime_m()} [{self.login}] - Пауза между скролами ~ {self.time_sleep_scroll} сек')
        print(f'{datatime_m()} [{self.login}] - Пауза между действиями ~ {self.sleeping:}')
        print(f'{datatime_m()} [{self.login}] - Количество действий в сутки {self.max_action}')
        print(f'{datatime_m()} [{self.login}] - Количество действий в час {self.max_action_hour}')
        print(f'{datatime_m()} [{self.login}] - Количество используемых тегов {self.count_tags}')
        print(f'{datatime_m()} [{self.login}] - Количество используемых коментариев {self.count_coments}')
        # вход в инстраграм
        browser.get(self.url_instagramm)
        sleep(self.time_sleep_login)

        user_input = browser.find_element_by_css_selector('input[name="username"]')
        user_input.send_keys(self.login)

        password_input = browser.find_element_by_css_selector('input[name="password"]')
        password_input.send_keys(self.password)

        login = browser.find_element_by_css_selector('button[type="submit"]')
        login.click()
        sleep(self.time_sleep_login)

        # запускаем бесконечный цикл
        while True:
            my_hashtags = self.tags()
            my_coments = self.coments()
            print(f'{datatime_m()} [{self.login}] - Ищем материал по тегу - [{my_hashtags}]')
            print(f'{datatime_m()} [{self.login}] - Комментировать будем так - [{my_coments}]')

            browser.get(f'https://www.instagram.com/explore/tags/{my_hashtags}/')
            sleep(self.time_sleep_scroll)

            # скролим фото для качивания ссылок
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

                post_urls = set(post_urls)
                post_urls = list(post_urls)

                if len(post_urls) > 53:  # todo времнное значение, больше 54 ссылок не могу спарсить
                    poisk = False
                else:
                    continue

            ac = 0  # счетчик ссылок на акаунты тех кто лайкнул
            link = 0  # счетчик ссылок полученных с тега
            lik1 = 0  # счетчик лайка
            com1 = 0  # счетчик комментариев
            flow1 = 0  # счетчик подписок

            # заходим на полученные ссылки
            for url in post_urls:
                browser.get(url)
                print(f'{datatime_m()} [{self.login}] - Берем в работу - {url}')
                sleep(self.time_sleep)

                if link == post_urls:
                    print(
                        f'{datatime_m()} [{self.login}] - Использованы все ссылки с тега - {my_hashtags}')
                    continue

                try:
                    browser.find_element_by_css_selector('a[class="sqdOP yWX7d     _8A5w5   ZIAjV "]').click()
                    sleep(self.time_sleep)
                    link += 1
                except:
                    link += 1
                    continue

                hrefs_foto_account = browser.find_elements_by_tag_name('a')
                post_urls_foto_account = []
                for i in hrefs_foto_account:
                    href_foto_account = i.get_attribute('href')
                    if '/p/' in href_foto_account:
                        post_urls_foto_account.append(href_foto_account)

                for url_foto_account in post_urls_foto_account[0:1]:
                    browser.get(url_foto_account)
                    print(f'{datatime_m()} [{self.login}] - Смотрим есть ли лайки на - {url_foto_account}')
                    sleep(self.time_sleep)
                    # todo логику почистить
                    try:
                        count_like_button = browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span')
                    except:
                        link += 1
                        break
                    if count_like_button:
                        count_like_button_text = count_like_button.text
                        count_like = int(count_like_button_text.split(' ')[0])
                        print(f'{datatime_m()} [{self.login}] - Количество лайков - {count_like}')
                        if count_like < 12:
                            loop_count = 12
                        else:
                            loop_count = int(count_like / 12)
                    else:
                        print(
                            f'{datatime_m()} [{self.login}] - Лайков нету на - {url_foto_account}')
                        link += 1
                        break
                    count_like_button.click()
                    sleep(3)

                    # todo нужно продумать скролинг и те ссылки которые он парсит ниже alert = driver.switch_to_alert() &&&
                    #  фокус в селениум на эту iframe - используя webdriver.switchTo().frame(...)
                    a = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div/div')
                    like_pipl_urls = []
                    # todo нужно продумать скролинг и те ссылки которые он парсит ниже проблема с с тем что заходим
                    #  на ссылу повторно для магии а этого делать не нужно
                    for j in range(0, loop_count + 1):
                        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);", a)

                        sleep(2)

                        browser.find_element_by_css_selector('a[class ="FPmhX notranslate MBL3Z"]')
                        all_hrefs = browser.find_elements_by_tag_name('a')

                        for url1 in all_hrefs:
                            url1 = url1.get_attribute('href')
                            like_pipl_urls.append(url1)

                    like_pipl_urls = set(like_pipl_urls)
                    like_pipl_urls = list(like_pipl_urls)

                    for i in range(0, len(like_pipl_urls)):
                        for pipl in like_pipl_urls:
                            if '/explore/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/p/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/directory/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/legal/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/accounts/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/direct/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/blog/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/docs/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if '/about/' in pipl:
                                like_pipl_urls.remove(pipl)
                            if 'https://about.instagram.com/' == pipl:
                                like_pipl_urls.remove(pipl)
                            if 'https://help.instagram.com/' == pipl:
                                like_pipl_urls.remove(pipl)
                            if 'https://www.instagram.com/' == pipl:
                                like_pipl_urls.remove(pipl)

                    # print(f'{datatime_m()} [{self.login}] - Обработаные ссылки на тех кто лайкнул {like_pipl_urls}')
                    # print(f'{datatime_m()} [{self.login}] - Обработаное количество ссылок {len(like_pipl_urls)}')

                    for pipl_new in like_pipl_urls:
                        if ac == len(like_pipl_urls):
                            print(
                                f'{datatime_m()} [{self.login}] - Закончились все кто лайкал идем на следую ссылку тега')
                            link += 1
                            break

                        print(f'{datatime_m()} [{self.login}] - Заходим в гости к - {pipl_new}')
                        browser.get(pipl_new)
                        sleep(self.time_sleep)
                        # todo лучше сделать через иф browser. //// == 'это ....'
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/section/main/div/div[2]/article/div/div/h2').text = 'Это закрытый аккаунт'
                            print(f'{datatime_m()} [{self.login}] - Аккаунт - {pipl_new}  закрытый, идем к следующему')
                            ac += 1
                            break
                        except:
                            pass
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[2]/h1').text = 'Публикаций пока нет'
                            print(
                                f'{datatime_m()} [{self.login}] - Аккаунт - {pipl_new} Публикаций нет, идем к следующему')
                            ac += 1
                            break
                        except:
                            pass
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div/h2').text = 'К сожалению, эта страница недоступна.'
                            print(
                                f'{datatime_m()} [{self.login}] - Аккаунт - {pipl_new} страница недоступна, идем к следующей')
                            ac += 1
                            break
                        except:
                            pass

                        print(f'{datatime_m()} [{self.login}] - Начинается магия | подписка | коменты | лайки |')
                        # подписка
                        button = browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div/section/main/div/header/section/div[2]/div/div/button')
                        button.click()
                        flow1 += 1
                        print(f'{datatime_m()} [{self.login}] - Подписок за сутки [{flow1}/{self.max_action}]')
                        sleep(self.time_sleep)
                        # лайк
                        new_hrefs_foto_account = browser.find_elements_by_tag_name('a')
                        new_post_urls_foto_account = []

                        for r in new_hrefs_foto_account:
                            new_href_foto_account = r.get_attribute('href')
                            if '/p/' in new_href_foto_account:
                                new_post_urls_foto_account.append(new_href_foto_account)

                        new_post_urls_foto_account = set(new_post_urls_foto_account)
                        new_post_urls_foto_account = list(new_post_urls_foto_account)

                        for new_url_foto_account in new_post_urls_foto_account[0:1]:
                            browser.get(new_url_foto_account)
                            sleep(self.time_sleep)

                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
                            lik1 += 1
                            print(f'{datatime_m()} [{self.login}] - Лайков за сутки [{lik1}/{self.max_action}]')
                            sleep(self.time_sleep)
                            # комментарии
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button').click()
                            sleep(self.time_sleep)
                            browser.find_element_by_xpath('//textarea').click()
                            comment = browser.find_element_by_tag_name('textarea')
                            comment.send_keys(my_coments)
                            sleep(self.time_sleep)
                            browser.find_element_by_css_selector('button[type="submit"]').click()
                            com1 += 1
                            print(
                                f'{datatime_m()} [{self.login}] - Комментариев за сутки [{com1}/{self.max_action}]')
                            sleep(self.sleeping)

            if lik1 >= self.max_action or com1 >= self.max_action or flow1 >= self.max_action:
                print(f'{datatime_m()} [{self.login}] - Исчерпан суточный лимит лайков | комментариев | подписок')
                print(f'{datatime_m()} [{self.login}] - Нужно отдохнуть и дальше работать')
                continue
            else:
                continue


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

    instagramm.insta()


if __name__ == "__main__":
    Process(target=run, args=('Rabota_v_dekreteizdoma', '123456789q')).start()
    sleep(5)
    Process(target=run, args=('dekret_rabota_olga', '123456789q')).start()
    sleep(5)
    Process(target=run, args=('rabo.tavradosti', '123456789qQ')).start()
