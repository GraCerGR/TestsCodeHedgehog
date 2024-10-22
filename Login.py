from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_profile(link, username, password):
    # Код входа в профиль
    browser = webdriver.Chrome()
    browser.get(link)

    # Ожидание загрузки страницы
    TSUButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/form/div/div[3]/a"))
    )
    TSUButton.click()

    # Ввод данных ТГУ
    EnterButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div/div/section/form/div[3]/input[4]"))
    )
    login = browser.find_element(By.XPATH, "/html/body/div/main/div/div/div/div/section/form/div[1]/input").send_keys(username)
    password = browser.find_element(By.XPATH, "/html/body/div/main/div/div/div/div/section/form/div[2]/input").send_keys(password)
    EnterButton.click()
