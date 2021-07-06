from time import sleep
from selenium import webdriver
import random
from configLPT import my_coments


def coments(coments=my_coments):
    """
    Ф-я определения комментариев из основного списка, зависит от настройки self.count_coments по умолчанию 1
    """
    random.shuffle(coments)
    my_coments = coments[:1]
    my_coments = ''.join(my_coments)
    return my_coments


com = coments()
print(com)
options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/91.0.4472.77 Safari/537.36')
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(options=options)
browser.set_window_rect(width=750, height=1050)

browser.get('https://www.instagram.com/')
sleep(2)
user_input = browser.find_element_by_css_selector('input[name="username"]')
user_input.send_keys('Rabota_v_dekreteizdoma')
password_input = browser.find_element_by_css_selector('input[name="password"]')
password_input.send_keys('123456789q')
login = browser.find_element_by_css_selector('button[type="submit"]')
login.click()
sleep(3)
browser.get('https://www.instagram.com/p/CQ_ZEhQnLsC/')
sleep(3)
browser.find_element_by_xpath(

    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button'

).click()
sleep(3)
browser.find_element_by_xpath('//textarea').click()
comment = browser.find_element_by_tag_name('textarea')
comment.send_keys(com)
sleep(3)
browser.find_element_by_css_selector('button[type="submit"]').click()
# print(
#         '░░░░░░░░░░░░▄▄░░░░░░░░░░░░░░\n'
#         '░░░░░░░░░░░█░░█░░░░░░░░░░░░░\n'
#         '░░░░░░░░░░░█░░█░░░░░░░░░░░░░\n'
#         '░░░░░░░░░░█░░░█░░░░░░░░░░░░░\n'
#         '░░░░░░░░░█░░░░█░░░░░░░░░░░░░\n'
#         '██████▄▄█░░░░░██████▄░░░░░░░\n'
#         '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
#         '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
#         '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
#         '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
#         '▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░░░░░\n'
#         '▓▓▓▓▓▓█████░░░░░░░░░██░░░░░░\n'
#         '█████▀░░░░▀▀████████░░░░░░░░\n'
#         '░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n'
#         '╔════╗░░╔════╗╔═══╗░░░░░░░░░\n'
#         '║████║░░║████║║███╠═══╦═════╗\n'
#         '╚╗██╔╝░░╚╗██╔╩╣██╠╝███║█████║\n'
#         '░║██║░░░░║██║╔╝██║███╔╣██══╦╝\n'
#         '░║██║╔══╗║██║║██████═╣║████║\n'
#         '╔╝██╚╝██╠╝██╚╬═██║███╚╣██══╩╗\n'
#         '║███████║████║████║███║█████║\n'
#         '╚═══════╩════╩════════╩═════╝\n')
