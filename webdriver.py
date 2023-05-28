import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json

opt = webdriver.ChromeOptions()
opt.add_argument('user-agent=Mozila/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0')
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=opt)
driver.get('https://school.admoblkaluga.ru/esia')
time.sleep(5)
driver.find_element(By.CLASS_NAME, 'style_intro-form_action__btn__2M9jV').click()
time.sleep(5)
driver.find_element(By.ID, 'login').send_keys('+79533299805')
time.sleep(5)
driver.find_element(By.ID, 'password').send_keys('Bessudnov!08')
time.sleep(5)
driver.find_element(By.CLASS_NAME, 'plain-button plain-button_wide').click()

input()

#
# wait = WebDriverWait(driver, 10)
# inp = wait.until(EC.element_to_be_clickable((By.ID, 'textarea')))
# driver.get(url)
# inpd = driver.find_element_by_id('textarea')
# input()
# url = 'https://translate.yandex.ru/'
