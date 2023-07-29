from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


url = 'https://github.com/1flipstar1/Students-calendar'
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url=url)
    time.sleep(233)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
