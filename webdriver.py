import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json

opt = webdriver.ChromeOptions()
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://school.admoblkaluga.ru/esia')
time.sleep(2)
driver.find_element(By.ID, 'details-button').click()
driver.find_element(By.ID, 'proceed-link').click()
time.sleep(2)

driver.find_element(By.CLASS_NAME, 'style_intro-form_action__btn__2M9jV').click()
time.sleep(2)
driver.find_element(By.ID, 'login').send_keys('+79533299805')
pas = driver.find_element(By.ID, 'password')
pas.send_keys('Bessudnov!08')
time.sleep(2)
pas.send_keys(Keys.ENTER)
for request in driver.requests:
    if request.method == "type_of_method_you_want" and request.url == "request_url_you_want":
        if request.headers.get("name_of_token_you_want"): #to confirm it exists before assigning a variable to it.
            token = request.headers.get("name_of_token_you_want")
            print(token)
""" auth_key = input()
key_sel = []

driver.find_element(By.CLASS_NAME, 'code-input text-left').send_keys(auth_key) """
# driver.find_element(By.LINK_TEXT, 'Позже').click()
# try:
#     driver.find_element(By.CLASS_NAME, 'plain-button-inline').click()
# except:
#     print(54)


#
# wait = WebDriverWait(driver, 10)
# inp = wait.until(EC.element_to_be_clickable((By.ID, 'textarea')))
# driver.get(url)
# inpd = driver.find_element_by_id('textarea')
# input()
# url = 'https://translate.yandex.ru/'
