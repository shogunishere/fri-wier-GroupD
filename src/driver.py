from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from settings import DRIVER_LOCATION

driver_instance = None

def setup_driver():
    global driver_instance
    chrome_options = ChromeOptions()
    # chrome_options.add_argument("--headless")

    service = ChromeService(executable_path=DRIVER_LOCATION)
    driver_instance = webdriver.Chrome(service=service, options=chrome_options)

def get_driver():
    global driver_instance
    if driver_instance is None:
        setup_driver()
    return driver_instance
    
def get_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    service = ChromeService(executable_path=DRIVER_LOCATION)
    return webdriver.Chrome(service=service, options=chrome_options)


