from email.header import Header
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Exeptions import *
from Comments import scrolling_to_element
from Users import go_to_the_users_tab
import time
from datetime import datetime, timedelta

def links(browser):
    printInfo(f"Начало теста CRUD ссылки-приглашения")
    if not go_to_the_users_tab(browser):
        return False
    print()

    if not open_links(browser):
        return False

    link = link_creating(browser, "Student")
    if not link:
        return False
    print()
    if not link_deleting(browser, link):
        return False
    link = None
    print()

    link = link_creating(browser, "Teacher")
    if not link:
        return False
    print()
    if not link_deleting(browser, link):
        return False
    link = None
    print()

    link = link_creating(browser, "Student", True)
    if not link:
        return False
    print()
    if not link_deleting(browser, link):
        return False
    link = None
    print()

    link = link_creating(browser, "Teacher", True, date())
    if not link:
        return False
    print()
    if not link_deleting(browser, link):
        return False
    link = None
    print()

    return True

def open_links(browser):
    try:
        button_to_show_links = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//h3[text()='Ссылки-приглашения']"))
        )
        button_to_show_links.click()
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка показа ссылок не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки. {e}")
        return False

def link_creating(browser, role, individual: bool = False, date: str = None):

    try:
        existingLinks = []
        existingLinks = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//tr[contains(@class, 'ant-table-row') and .//p[contains(@class, 'Paragraph_hidden__oR1JA Paragraph_paragraph__vZceR')]]"))
        )
        count = len(existingLinks)
        printInfo(f"Существующие ссылки: {count}")
    except (TimeoutException, NoSuchElementException):
        printInfo(f"Существующие ссылки не найдены")
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска существующих ссылок. {e}")
        return False

    try:
        creating_link_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'Button_button__4z3Rc') and .//span[text()='Создать ссылку']]"))
        )
        creating_link_button.click()
        sleep(1)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка создания ссылок не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки. {e}")
        return False

    try:
        modalWindow = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal-content.Modal_content__miRwP"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    try:
        WebDriverWait(modalWindow, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Select_select__control__Z4598"))
        ).click()
        WebDriverWait(modalWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{roleFormat(role)}')]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле селектора не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        if individual:
            WebDriverWait(modalWindow, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Индивидуальная']"))
            ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле 'Индивидуальная' не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка установки чекера 'Индивидуальная': {e}")
        return False

    try:
        if date:
            WebDriverWait(modalWindow, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Временная']"))
            ).click()
#            dateNewFormat = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            WebDriverWait(modalWindow, 10).until(
                EC.presence_of_element_located((By.NAME, "validTime"))
            ).send_keys(date)
            modalWindow.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле 'Временная' и/или поле ввода даты не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка установки чекера 'Временная': {e}")
        return False

    try:
        WebDriverWait(modalWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button_type_accent__NGYDO') and .//span[text()='Подтвердить']]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка создания ссылки не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка создания ссылки: {e}")
        return False

    try:
        notification = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Успешно создано')]"))
        )
        sleep(5)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление создания ссылки не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка поиска уведомления: {e}")
        return False

    try:
        NewExistingLinks = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//tr[contains(@class, 'ant-table-row') and .//p[contains(@class, 'Paragraph_hidden__oR1JA Paragraph_paragraph__vZceR')]]"))
        )
        printInfo(f"Существующие ссылки: {len(NewExistingLinks)}")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Новые ссылки не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска новых ссылок. {e}")
        return False

    try:
        if existingLinks:
            for item in existingLinks:
                if item in NewExistingLinks:
                    NewExistingLinks.remove(item)
        newLink = WebDriverWait(NewExistingLinks[0], 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//tr[contains(@class, 'ant-table-row')]//p[contains(@class, 'Paragraph_hidden__oR1JA')]"))
        ).text
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Новая ссылка в элементе таблицы не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка выделения новой строки из всех существующих строк. {e}")
        return False

    printSuccess(f"Ссылка для {'студента' if roleFormat(role) == 'Студент' else 'преподавателя' if roleFormat(role) == 'Преподаватель' else roleFormat(role)}{", индивидуальная" if individual else ""}{f", временная (до {date})" if date else ""} успешно создана: {newLink}")
    return newLink

def link_deleting(browser, link):
    try:
        linkTableCell = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH,
                                                 f"//tr[contains(@class, 'ant-table-row')]//p[contains(@class, 'Paragraph_hidden__oR1JA') and //p[contains(text(), '{link}')]]"))
        )
        linkTableString = linkTableCell.find_element(By.XPATH, "..//..//..")
        td_elements = linkTableString.find_elements(By.TAG_NAME, 'td')
        deleteButton = td_elements[4].find_element(By.TAG_NAME, 'button')
        scrolling_to_element(browser, deleteButton)
        deleteButton.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка удаления ссылки не была найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка нажатия кнопки удаления ссылки. {e}")
        return False

    try:
        modalWindow = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal-content.Modal_content__miRwP"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        WebDriverWait(modalWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button_type_accent__NGYDO') and .//span[text()='Подтвердить']]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка создания ссылки не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка создания ссылки: {e}")
        return False

    try:
        notification = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Успешно удалено')]"))
        )
        sleep(5)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление удаления ссылки не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка поиска уведомления: {e}")
        return False

    try:
        WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.XPATH,
                                                 f"//tr[contains(@class, 'ant-table-row')]//p[contains(@class, 'Paragraph_hidden__oR1JA') and //p[contains(text(), '{link}')]]"))
        )
        printExeption("Ссылка снова найдена. Она не удалена")
        return False
    except (TimeoutException, NoSuchElementException):
        printSuccess(f"Ссылка успешно удалена")
        return True
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка нажатия кнопки удаления ссылки. {e}")
        return False

def date():
    futureDate = datetime.now() + timedelta(days=7)
    formattedDate = futureDate.strftime('%Y-%m-%d %H:%M:%S')
    return formattedDate

def roleFormat(role):
    if role == "Student":
        role = "Студент"
    elif role == "Teacher":
        role = "Преподаватель"
    return role