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

def users(browser, user_name, roleSelector, role):
    printInfo(f"Начало теста вкладки users")
    if not go_to_the_users_tab(browser):
        return False
    if not displaying_a_page_with_users(browser, role):
        return False
    if not search_by_user_name(browser, user_name, roleSelector):
        return False
    return True


# Переход на вкладку "Пользователи"
def go_to_the_users_tab(browser):
    try:
        queueButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[5]"))
        )
        queueButton.click()
        printSuccess(f"Переход на страницу 'Пользователи' выполнен")
        return True
    except Exception as e:
        printExeption(f"Ошибка: Кнопка Пользователи не была найдена или не стала доступной. {e}")
        return False

# Тест отображения списка пользователей
def displaying_a_page_with_users(browser, role):
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

    if not user_role_selector(browser, table, "Преподаватели", role):
        return False
    if not user_role_selector(browser, table, "Студенты", role):
        return False
    printSuccess("Страница пользователей отображается")
    return True

# Переключение между преподавателями и студентами
def user_role_selector(browser, table, roleSelector, role):
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
        selector.find_element(By.XPATH, f"//p[contains(text(), '{roleSelector}')]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор '{roleSelector}' не найден")
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
        if role == "Student":
            user_cells = table.find_elements(By.CSS_SELECTOR, "td.ant-table-cell div.UsersSection_cell_link__c1oRg:not([class*=' '])")

            printInfo(f"{roleSelector} найдены, первые 10:")
            for cell in user_cells[:10]:
                printInfo(f"{cell.find_element(By.TAG_NAME, "p").text}")
        else:
            rows = table.find_elements(By.CSS_SELECTOR, 'tr.ant-table-row')
            users_info = []

            for row in rows[:10]:
                name_element = row.find_element(By.CSS_SELECTOR, 'td.ant-table-cell a p.Paragraph_paragraph__vZceR')
                email_element = row.find_elements(By.CSS_SELECTOR, 'td.ant-table-cell a p.Paragraph_paragraph__vZceR')[1]
                name = name_element.text
                email = email_element.text
                users_info.append(f"{name}, почта: {email}")

            printInfo(f"{roleSelector} найдены, первые 10:")
            for user in users_info:
                printInfo(user)

        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователи не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


# Поиск по имени пользователя
def search_by_user_name(browser, user_name, roleSelector):
    if not search_by_user_name_without_cleaning_searchfield(browser, user_name, roleSelector):
        return False
    if not cleaning_searchfield(browser):
        return False
    printSuccess("Поиск работает")
    return True


def search_by_user_name_without_cleaning_searchfield(browser, user_name, roleSelector):
    if roleSelector == "Student":
        roleSelector = "Студенты"
    elif roleSelector == "Teacher":
        roleSelector = "Преподаватели"
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
        selector.find_element(By.XPATH, f"//p[contains(text(), '{roleSelector}')]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор '{roleSelector}' не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div[1]/div/div[2]/span/input"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода поиска не найдено.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска. {e}")
        return False

    try:

        for char in user_name:
            searchButton.send_keys(char)
            time.sleep(0.05)

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[div[p[text()='{user_name}']]] | //td[a[p[text()='{user_name}']]]"))
        )
        printInfo(f"Пользователь найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователь '{user_name}' не найден.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False
    return True


# Отчиска поля поиска
def cleaning_searchfield(browser):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div/div[1]/div/div[2]/span/input"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода поиска не найдено.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска. {e}")
        return False
    #нажатие на крестик
    try:
        closeButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input-clear-icon'))
        )
        closeButton.click()
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    #Проверка, что поле поиска отчистилось
    value = searchButton.get_attribute('value')
    if value == '':
        printInfo(f"Поле поиска отчищено")
        return True
    else:
        printInfo(f"Ошибка: Поле поиска не отчищено")
        return False