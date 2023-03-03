from seleniumwire import webdriver
from _global.configs import config


def make_driver_option():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    return chrome_options

def get_webdriver(headers=None) -> webdriver.Chrome:

    chrome_options = make_driver_option()
    driver = webdriver.Chrome(config.PATH_CHROME_DRIVER, chrome_options=chrome_options)
    # driver.implicitly_wait(time_to_wait=3)
    if headers is not None:
        driver.header_overrides = headers
        
    return driver