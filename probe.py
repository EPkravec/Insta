import random
from configLPT import my_tags
from selenium import webdriver

random.shuffle(my_tags)
my_hashtags = my_tags[:1]
my_hashtags = ''.join(my_hashtags)
options = webdriver.ChromeOptions()

options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/91.0.4472.77 Safari/537.36')

options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')

browser = webdriver.Chrome(options=options)
browser.set_window_rect(width=630, height=930)

browser.get(f"https://www.instagram.com/explore/tags/{my_hashtags}/")