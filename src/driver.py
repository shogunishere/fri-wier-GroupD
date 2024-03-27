from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from settings import DRIVER_LOCATION, BROWSER_LOCATION, WHAT_BROWSER

driver_instance = None

def setup_driver():
    global driver_instance
    if WHAT_BROWSER == "Chrome":
        browser_options = ChromeOptions()
    elif WHAT_BROWSER == "Firefox":
        browser_options = FirefoxOptions()
        if BROWSER_LOCATION != None:
            browser_options.binary_location = BROWSER_LOCATION
    
    browser_options.add_argument("--headless")

    service = ChromeService(executable_path=DRIVER_LOCATION)
    driver_instance = webdriver.Chrome(service=service, options=browser_options)

def get_driver():
    global driver_instance
    if driver_instance is None:
        setup_driver()
    return driver_instance

