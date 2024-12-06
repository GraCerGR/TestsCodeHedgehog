from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from Exeptions import *
from Main import create_new_browser_window
from Users import go_to_the_users_tab
from time import sleep
from settings import *

def addingToClass(browser, classname):
    printInfo(f"Начало теста добавления в гугл класс")
    if not go_to_the_users_tab(browser):
        return False
    print()

    if not manually_adding_users(browser, USERNAME_INVENTED_PERSON):
        return False
    print()
    if not test_addingToClass_in_new_browser_window(classname):
        return False
    printSuccess("Пользователь был успешно добавлен в класс вручную")
    print()

    return True


def test_addingToClass_in_new_browser_window(classname):

    browser = create_new_browser_window(SITELINK, USERNAME_INVENTED_PERSON, PASSWORD_INVENTED_PERSON, classname, False)
    if not browser:
        return False
    print()

    browser.quit()
    return True


# Ручное добавление пользователей
def manually_adding_users(browser, email):
    try:
        addingUserButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'Button_button__4z3Rc') and .//span[text()='Добавить пользователя']]"))
        )
        addingUserButton.click()
        sleep(1)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка добавления пользователей не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки. {e}")
        return False

    try:
        drawerWindow = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-drawer-body.Drawer_body__eSiGt"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        emailInput = WebDriverWait(drawerWindow, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
        )
        emailInput.send_keys(email)
        sleep(2)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода имени не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки. {e}")
        return False

    try:
        WebDriverWait(drawerWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//tr[contains(@class, 'ant-table-row') and .//td[(text()='{email}')]]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователь с почтой '{email}' не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска пользователя. {e}")
        return False

    try:
        WebDriverWait(drawerWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button_type_accent__NGYDO') and .//span[text()='Подтвердить']]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка приглашения не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка создания приглашения: {e}")
        return False

    try:
        notification = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Изменения успешно сохранены')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление создания приглашения не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка поиска уведомления: {e}")
        return False

    printSuccess("Пользователь успешно приглашён (со стороны приглашающего)")
    return True
