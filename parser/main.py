from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from .utils import get_products


def configure_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")

    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def start_parser() -> Tuple[Optional[bool], Optional[str]]:
    try:
        driver = configure_driver()
        url = "https://www.dewu.com"
        driver.get(url)
        get_products(driver)
        return True, None
    except Exception as e:
        return None, str(e)
    finally:
        driver.quit()
