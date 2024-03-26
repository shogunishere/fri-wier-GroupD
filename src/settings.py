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

SEED = ["http://gov.si", "http://evem.gov.si", "http://e-uprava.gov.si", "http://e-prostor.gov.si"]

DRIVER_LOCATION = "./driver/chromedriver.exe"

TIMEOUT = 5
