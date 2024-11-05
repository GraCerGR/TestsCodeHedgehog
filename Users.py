from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Exeptions import *
import time

def users(browser, username):
    printInfo(f"Начало теста вкладки users")
    if not go_to_the_users_tab(browser):
        return False
    if not displaying_a_page_with_users(browser):
        return False
    return True


# Переход на вкладку "Очередь"
def go_to_the_users_tab(browser):
    try:
        queueButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[5]"))
        )
        queueButton.click()
        printSuccess(f"Переход на страницу 'Пользователи' выполнен")
        return True
    except Exception:
        printExeption(f"Ошибка: Кнопка Пользователи не была найдена или не стала доступной.")
        return False


def displaying_a_page_with_users(browser):
    try:
        table = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "UsersSection_table__Mb8Rv"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Таблица с пользователями не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    if not user_role_selector(browser, table, "Преподаватели"):
        return False
    if not user_role_selector(browser, table, "Студенты"):
        return False
    printSuccess("Страница пользователей отображается")
    return True


def user_role_selector(browser, table, role):
    try:
        selector = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-segmented.Segmented_segmented__VNG0y.css-14h5sa0"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор роли не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        selector.find_element(By.XPATH, f"//p[contains(text(), '{role}')]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор '{role}' не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".ant-segmented.Segmented_segmented__VNG0y.css-14h5sa0"))
        )
        user_cells = table.find_elements(By.CSS_SELECTOR, "td.ant-table-cell div.UsersSection_cell_link__c1oRg:not([class*=' '])")

        printInfo(f"{role} найдены, первые 10:")
        for cell in user_cells[:10]:
            printInfo(f"{cell.find_element(By.TAG_NAME, "p").text}")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователи не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")