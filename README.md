## DB Setup

0. Create ```.env``` file with following content:

```
DB_HOST=localhost
DB_USER=postgres
DB_NAME=govcrawler
DB_PASSWORD=psswd
DB_PORT=5432
```

1. Create empty ```pg_data``` directory

2. ```docker exec -it govcrawler bash```

3. ```psql -U postgres```

4. ```CREATE DATABASE govcrawler;```

If you want to inspect remember to use: ```\c govcrawler``` before querying tables.

5. ```docker cp ./db/crawldb.sql govcrawler:/docker-entrypoint-initdb.d/crawldb.sql```

6. Start container:
```docker run --name govcrawler -e POSTGRES_PASSWORD=psswd -e POSTGRES_USER=postgres -e POSTGRES_DB=govcrawler -v ${PWD}/pgdata:/var/lib/postgresql/data -v ${PWD}/db:/docker-entrypoint-initdb.d -p 5432:5432 -d postgres:12.2```

7. Execute initialization SQL script:
   ```docker exec -it govcrawler psql -U postgres -d govcrawler -f /docker-entrypoint-initdb.d/crawldb.sql```

#Installation on local Machine
Install Python 3.10 from here: https://sourceforge.net/projects/portable-python/files/Portable%20Python%203.10/Portable%20Python-3.10.0%20x64.exe/download

Extraxt ur files from App\Python to example: C:\PortablePython\python310
If u are on Windows 7 copy this DLL fix from here: https://github.com/nalexandru/api-ms-win-core-path-HACK/releases/download/0.3.1/api-ms-win-core-path-blender-0.3.1.zip (x64 folder since we use x64 python)
  inside C:\PortablePython\python310

put this inside DevelopmentEnviroment.bat and put it inside C:\PortablePython\
```
@rem
@rem OpenCV command line with appropriate paths set
@rem
@echo OpenCV Shell
@set PATH=C:\PortablePython\python310;C:\PortablePython\python310\Scripts;%PATH%
@doskey pip=python -m pip $*
@CD ..
@cmd
```


open DevelopmentEnviroment.bat and install requirements: pip install -r requirements.txt

Install Selenium driver (if u are on Windows 7 you have to use firefox driver, because Chrome driver uses PrefetchVirtualMemory and  SetThreadInformation from C:\Windows\SysWOW64\kernel32.dll which Windows7 does not have (there is a way to add those with this: https://github.com/vxiiduu/VxKex
	U can manualy download api-ms-win-core-winrt-l1-1-0.dll and put it in the same dir (%UserProfile%\.wdm\drivers\chromedriver\win64\120.0.6099.109\chromedriver-win32) as chromedriver.exe to fix the other missing dll

Get firefox driver from here: https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-win32.zip

Test ur setup with this script
```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
#from selenium.webdriver.chrome.service import Service as ChromeService
#from selenium.webdriver.chrome.options import Options as ChromeOptions

WEB_BROWSER_LOCATION = r'C:\Program Files\Mozilla Firefox\firefox.exe'
WEB_DRIVER_LOCATION = "./geckodriver.exe"
WEB_PAGE_ADDRESS = 'https://vreme.arso.gov.si/napoved'
TIMEOUT = 5


web_driver_options = FirefoxOptions()
#web_driver_options = ChromeOptions()

#Tell where browser is
web_driver_options.binary_location = WEB_BROWSER_LOCATION

# If you comment the following line, a browser will show ...
web_driver_options.add_argument("--headless")

#Adding a specific user agent
web_driver_options.add_argument("user-agent=fri-ieps-TEST")

print(f"Retrieving web page URL '{WEB_PAGE_ADDRESS}'")
#driver = webdriver.Firefox(executable_path=WEB_DRIVER_LOCATION, options=web_driver_options)
#driver = webdriver.Chrome(executable_path=WEB_DRIVER_LOCATION, options=web_driver_options)
service = FirefoxService(executable_path=WEB_DRIVER_LOCATION)
#service = ChromeService(executable_path=WEB_DRIVER_LOCATION)
driver = webdriver.Firefox(service=service, options=web_driver_options)
#driver = webdriver.Chrome(service=service, options=web_driver_options)
driver.get(WEB_PAGE_ADDRESS)

# Timeout needed for Web page to render (read more about it)
time.sleep(TIMEOUT)

html = driver.page_source

print(f"Retrieved Web content (truncated to first 900 chars): \n\n'\n{html[:900]}\n'\n")

page_msg = driver.find_element(By.CSS_SELECTOR, ".panel-header")

print(f"Web page message: '{page_msg.text}'")

driver.close()
```

Install PosgressSQL v14 (if u are on Windows 7 uncheck pgAdmin installation and install separatly from here: https://www.postgresql.org/ftp/pgadmin/pgadmin4/v4.30/windows/ )
and launch it

then create database: CREATE DATABASE govcrawler;
then import db: psql -U postgres -d govcrawler -f /path_to_your_script.sql (example: psql -U postgres -d govcrawler -f crawldb.sql

Go to Step 0

launch main.py (python main.py) and wait a long time
