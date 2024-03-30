from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME')
}

USER_AGENT = "fri-wier-D"

SEED = ["http://sitranet.si/navodila-sivis2.pdf", "https://spot.gov.si/assets/sitemap/sitemap.xml" , "http://gov.si", "http://evem.gov.si", "http://e-uprava.gov.si", "http://e-prostor.gov.si"]

DRIVER_LOCATION = "./driver/chromedriver.exe"

TIMEOUT = 5

WORKERS = 1
