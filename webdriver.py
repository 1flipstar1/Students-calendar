import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json

opt = webdriver.ChromeOptions()
opt.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=opt)
driver.get('https://school.admoblkaluga.ru/esia')
time.sleep(5)
driver.find_element(By.CLASS_NAME, 'style_intro-form_action__btn__2M9jV').click()
time.sleep(5)
driver.find_element(By.ID, 'login').send_keys('+79533299805')
pas = driver.find_element(By.ID, 'password')
pas.send_keys('Bessudnov!08')
time.sleep(5)
pas.send_keys(Keys.ENTER)
auth_key = input()
key_sel = []

driver.find_element(By.CLASS_NAME, 'code-input text-left').send_keys(auth_key)
# driver.find_element(By.LINK_TEXT, 'Позже').click()
# try:
#     driver.find_element(By.CLASS_NAME, 'plain-button-inline').click()
# except:
#     print(54)
input()

#
# wait = WebDriverWait(driver, 10)
# inp = wait.until(EC.element_to_be_clickable((By.ID, 'textarea')))
# driver.get(url)
# inpd = driver.find_element_by_id('textarea')
# input()
# url = 'https://translate.yandex.ru/'
