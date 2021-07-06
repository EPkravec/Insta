
from time import sleep
from selenium import webdriver


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
user_input.send_keys('rabo.tavradosti')
password_input = browser.find_element_by_css_selector('input[name="password"]')
password_input.send_keys('123456789qQ')
login = browser.find_element_by_css_selector('button[type="submit"]')
login.click()
sleep(3)
b= browser.get('https://www.instagram.com/p/CQ_ZEhQnLsC/')
sleep(3)
a = browser.find_elements_by_xpath('/html/body/div[1]/div/div/section/main/div/div[1]/article/header/div[2]/div[1]/div/span/a')
a = a[0]
print(f'{b}------ ваделец {a}')
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
