import random
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from multiprocessing import Process
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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
        browser.set_window_rect(width=750, height=1050)

        browser.get(self.url_instagramm)
        sleep(self.time_sleep_login)
        user_input = browser.find_element_by_css_selector('input[name="username"]')
        user_input.send_keys(self.login)
        password_input = browser.find_element_by_css_selector('input[name="password"]')
        password_input.send_keys(self.password)
        login = browser.find_element_by_css_selector('button[type="submit"]')
        login.click()
        sleep(self.time_sleep_login)

        while True:

            my_hashtags = self.tags()
            my_coments = self.coments()

            print(f'{self.datatime} [{self.login}] - Используем тег - [{my_hashtags}]')
            print(f'{self.datatime} [{self.login}] - Используем сообщение - [{my_coments}]')

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

                post_urls = set(post_urls)
                post_urls = list(post_urls)

                if len(post_urls) > 53:  # todo времнное значение, больше 54 ссылок не могу спарсить
                    print(f'{self.datatime} [{self.login}] - Ссылок для работы - {len(post_urls)}')
                    print(f'{self.datatime} [{self.login}] - Список ссылок {post_urls}')
                    poisk = False
                else:
                    print(f'{self.datatime} [{self.login}] - Ссылок не хватает - {len(post_urls)}, поищу еще')
                    continue
            ac = 0  # счетчик ссылок на акаунты тех кто лайкнул
            link = 0  # счетчик ссылок полученных с тега
            lik1 = 0  # счетчик лайка
            com1 = 0  # счетчик комментариев
            flow1 = 0  # счетчик подписок

            for url in post_urls:
                browser.get(url)
                print(f'{self.datatime} [{self.login}] - Идем по ссылке с тегов - {url}')
                sleep(self.time_sleep)

                try:
                    browser.find_element_by_css_selector('a[class="sqdOP yWX7d     _8A5w5   ZIAjV "]').click()
                    print(f'{self.datatime} [{self.login}] - Зашли на аккаунт пользователя этой фотографии {url}')
                    sleep(self.time_sleep)
                    link += 1
                except:
                    print(f'{self.datatime} [{self.login}] - Перейти по ссылке не удалось беру следующую')
                    link += 1
                    continue

                if link == post_urls:
                    print(f'{self.datatime} [{self.login}] - Использованы все ссылки с тега, ищем по новому тегу')
                    continue

                print(f'{self.datatime} [{self.login}] - Ищем ссылки на фото в аке выбираем фото (одно)')
                hrefs_foto_account = browser.find_elements_by_tag_name('a')
                post_urls_foto_account = []
                for i in hrefs_foto_account:
                    href_foto_account = i.get_attribute('href')
                    if '/p/' in href_foto_account:
                        post_urls_foto_account.append(href_foto_account)
                print(
                    f'{self.datatime} [{self.login}] - Фото выбрали, смотрим кто лайкал {post_urls_foto_account[0:1]}')
                for url_foto_account in post_urls_foto_account[0:1]:
                    browser.get(url_foto_account)
                    print(f'{self.datatime} [{self.login}] - Смотрим количество лайков под фото')
                    sleep(self.time_sleep)
                    try:
                        count_like_button = browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span')
                    except:
                        print(
                            f'{self.datatime} [{self.login}] - Не нашли количество лайков берем другую ссылку с тегов')
                        link += 1
                        break
                    if count_like_button:
                        count_like_button_text = count_like_button.text
                        count_like = int(count_like_button_text.split(' ')[0])
                        print(f'{self.datatime} [{self.login}] - Количество лайков под фото - {count_like}')
                        if count_like < 12:
                            loop_count = 12
                        else:
                            loop_count = int(count_like / 12)
                    else:
                        print(
                            f'{self.datatime} [{self.login}] - Не нашли количество лайков берем другую ссылку с тегов')
                        link += 1
                        break
                    print(
                        f'{self.datatime} [{self.login}] - Создаем список всех кто лайкнул {post_urls_foto_account[0:1]}')

                    count_like_button.click()
                    sleep(3)
                    # todo нужно продумать скролинг и те ссылки которые он парсит ниже
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

                    print(f'{self.datatime} [{self.login}] - Ссылки на тех кто лайкнул {like_pipl_urls}')
                    print(f'{self.datatime} [{self.login}] - Количество ссылок {len(like_pipl_urls)}')
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

                    print(f'{self.datatime} [{self.login}] - Обработаные ссылки на тех кто лайкнул {like_pipl_urls}')
                    print(f'{self.datatime} [{self.login}] - Обработаное количество ссылок {len(like_pipl_urls)}')

                    for pipl_new in like_pipl_urls:

                        print(f'{self.datatime} [{self.login}] - Заходим в гости к - {pipl_new}')
                        browser.get(pipl_new)
                        sleep(self.time_sleep)

                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/section/main/div/div[2]/article/div/div/h2').text = 'Это закрытый аккаунт'
                            print(f'{self.datatime} [{self.login}] - Аккаунт - {pipl_new}  закрытый, идем к следующему')
                            ac += 1
                            break
                        except:
                            pass
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[2]/h1').text = 'Публикаций пока нет'
                            print(
                                f'{self.datatime} [{self.login}] - Аккаунт - {pipl_new} Публикаций нет, идем к следующему')
                            ac += 1
                            break
                        except:
                            pass
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div/h2').text = 'К сожалению, эта страница недоступна.'
                            print(
                                f'{self.datatime} [{self.login}] - Аккаунт - {pipl_new} страница недоступна, идем к следующей')
                            ac += 1
                            break
                        except:
                            pass

                        if ac == len(like_pipl_urls):
                            print(
                                f'{self.datatime} [{self.login}] - Закончились все кто лайкал идем на следую ссылку тега')
                            link += 1
                            break
                        print(f'{self.datatime} [{self.login}] - Начинается магия | подписка | коменты | лайки |')

                        button = browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div/section/main/div/header/section/div[2]/div/div/button')
                        button.click()
                        flow1 += 1
                        print(f'{self.datatime} [{self.login}] - Подписок за сутки [{flow1}/{self.max_like_day}]')
                        sleep(self.time_sleep)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        print(f'{self.datatime} [{self.login}] - Ищем ссылки на фото в аке выбираем фото (одно)')
                        new_hrefs_foto_account = browser.find_elements_by_tag_name('a')
                        new_post_urls_foto_account = []
                        for r in new_hrefs_foto_account:
                            new_href_foto_account = r.get_attribute('href')
                            if '/p/' in new_href_foto_account:
                                new_post_urls_foto_account.append(new_href_foto_account)
                        print(f'{self.datatime} [{self.login}] - Нашли фото')
                        for new_url_foto_account in new_post_urls_foto_account[0:1]:
                            browser.get(new_url_foto_account)
                            sleep(self.time_sleep)
                            comment = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[2]/button/div/svg').click()
                            comment.send_keys(my_coments)
                            ckick = browser.find_element_by_css_selector('button[type="submit"]')
                            ckick.click()
                            com1 += 1
                            print(f'{self.datatime} [{self.login}] - Комментариев за сутки [{com1}/{self.max_like_day}]')
                            sleep(self.time_sleep)

                            browser.find_element_by_xpath(
                                # '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
                                '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
                            lik1 += 1
                            sleep(self.time_sleep)
                            print(f'{self.datatime} [{self.login}] - Лайков за сутки [{lik1}/{self.max_like_day}]')
                            sleep(self.time_sleep_like)

            if lik1 >= self.max_like_day and com1 >= self.max_like_day and flow1 >= self.max_like_day:
                print(f'{self.datatime} [{self.login}] - Cуточный лимит лайков комментариев и подписок')
                print(f'{self.datatime} [{self.login}] - Нужно отдохнуть и дальше работать')
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

    print(f'==================================================================================================')
    print(f'                                  Привет {login}')
    print(f'==================================================================================================')
    print(f'====================================== Запустились ===============================================')
    print(f'================================ Я работать иди отдыхай ==========================================')
    print(f'====================================== Мои натройки ==============================================')

    instagramm.insta()


if __name__ == "__main__":
    # Process(target=run, args=('Rabota_v_dekreteizdoma', '123456789q')).start()
    # sleep(5)
    # Process(target=run, args=('dekret_rabota_olga', '123456789q')).start()
    # sleep(5)
    Process(target=run, args=('rabo.tavradosti', '123456789qQ')).start()
