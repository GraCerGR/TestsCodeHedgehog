from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Exeptions import *
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException


def create_new_browser_window(SITELINK, USERNAME, PASSWORD, CLASS, TSUACC = True):
    try:
        browser = webdriver.Chrome()
        if TSUACC:
            browser = login_to_profile(browser, SITELINK, USERNAME, PASSWORD)
        else:
            browser = login_to_profile_without_TSUAccount(browser, SITELINK, USERNAME, PASSWORD)

        if not browser:
            browser.quit()
            printExeption(f"Ошибка открытия нового окна и входа")
            return False
        printSuccess("Открытие нового окна браузера и вход выполнены успешно")
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка открытия нового окна и входа: {e}")
        return False

    try:
        browser = login_to_class(browser, CLASS)
        if not browser:
            browser.quit()
            printExeption(f"Ошибка открытия класса")
            return False
        print()
        return browser
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка открытия нового окна пользователя: {e}")
        return False


def login_to_profile(browser, link, username, password):
    # Код входа в профиль
    #browser = webdriver.Chrome()
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
    return browser

def login_to_profile_without_TSUAccount(browser, link, username, password):
    # Код входа в профиль
    #browser = webdriver.Chrome()
    browser.get(link)

    # Ожидание загрузки страницы
    TSUButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/form/div/div[3]/a"))
    )

    # Ввод данных ТГУ
    EnterButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/form/div/div[3]/button"))
    )
    login = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/form/div/div[1]/div/span/input").send_keys(username)
    password = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/form/div/div[2]/div/span/input").send_keys(password)
    EnterButton.click()
    return browser


def login_to_class(browser, classname):
    try:
        classButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//p[contains(@class, 'Paragraph_paragraph__vZceR') and contains(@class, 'Paragraph_paragraph_weight_bold__uSpls') and text()='{classname}']"))
        )
        classButton.click()
        printSuccess(f"Вход в класс {classname} успешно выполнен")
        return browser
    except Exception as e:
        printExeption(f"Ошибка входа в класс '{classname}'. {e}")
        browser.quit()
        return False


