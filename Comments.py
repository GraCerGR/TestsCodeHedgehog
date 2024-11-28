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
import time
from selenium.webdriver import ActionChains

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class TaskInRating:
    def __init__(self, moduleName, sectionName, taskName):
        self.moduleName = moduleName
        self.sectionName = sectionName
        self.taskName = taskName

def comments(browser, user: User, task):
    printInfo(f"Начало теста страницы рейтинга")
    if not go_to_the_history_tab(browser, user, task):
        return False
    print()

    if not comment_maker(browser, "public"):
        return False
    print()

    return True


# Переход в историю решений
def go_to_the_history_tab(browser, user, task):
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[5]"))
        ).click()
    except Exception:
        printExeption(f"Ошибка: Кнопка Пользователи не была найдена или не стала доступной.")
        return False

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
        selector.find_element(By.XPATH, f"//p[contains(text(), '{user.role}')]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор '{user.role}' не найден")
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

        for char in user.name:
            searchButton.send_keys(char)
            time.sleep(0.05)

        userInTable = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[a[p[text()='{user.name}']]]"))
        )
        printInfo(f"Пользователь найден")
        userInTable.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователь '{user.name}' не найден.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        resultHead = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                       "//div[contains(@class, 'ResultsUserPageHeader_results_user_page_header__ww3Rh')]"))
        )
        WebDriverWait(resultHead, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//h2[contains(text(), 'Результаты')]"))
        )
        WebDriverWait(resultHead, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'ant-flex') and contains(., 'Пользователь:') and .//a[contains(text(), '{user.name}')]]"))
        )
        printInfo(f"Страница результатов пользователя '{user.name}' открыта")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поля информации о результатах (заголовок, имя пользователя) не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        module = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class, 'ModuleStructure_module_structure__Dd7NK')]"
                           f"//div[contains(@class, 'ModuleStructure_module_header__vzobJ')]"
                           f"//p[contains(@class, 'Paragraph_paragraph__vZceR') and "
                           f"contains(@class, 'Paragraph_paragraph_weight_bold__uSpls') and "
                           f"text()='{task.moduleName}']"))
        )
        printInfo(f"Модуль '{task.moduleName}' найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модуль '{task.moduleName}' не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        section = module.find_element(By.XPATH,
                                      f"//div[contains(@class, 'SectionStructure_section_structure__oiisl') and .//p[text()='{task.sectionName}']]")
        printInfo(f"Секция '{task.sectionName}' найдена")
        section.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Секция '{task.sectionName}' модуля '{task.moduleName}' не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        taskElement = WebDriverWait(module, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'ant-table-row') and contains(@class, 'ant-table-row-level-0') and td[2]//p[text()='{task.taskName}']]"))
        )
        printInfo(f"Задача '{task.taskName}' найдена")
        taskElement.click()

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Задача '{task.taskName}' не найдена в секции '{task.sectionName}' модуля '{task.moduleName}'")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

        printInfo(f"Отображение задач функционирует")
        return taskElement

    try:
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH,
                                            f"//h3[contains(text(), 'История попыток') and .//a[contains(text(), '{task.taskName}')]]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Заголовок страницы истории решений не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка перехода в историю решений задачи. {e}")
        return False

    printSuccess(f"Переход на страницу с историей решений задачи выполнен")
    return True

def comment_maker(browser, protection):
    try:
        commentProtectionSelector = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Segmented_segmented__VNG0y')]"))
        )
        commentProtections = commentProtectionSelector.find_elements(By.TAG_NAME, 'label')
        commentText = ""
        if (protection == "public"):
            commentProtections[0].click()
            commentText = "Публичный комментарий"
        elif (protection == "private"):
            commentProtections[1].click()
            commentText = "Приватный комментарий"
        else:
            printExeption("Неверный аргумент приватности комментария")
            return False

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор приватности комментариев не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        comment = browser.find_elements(By.CSS_SELECTOR, '.jodit-wysiwyg[contenteditable="true"]')
        comment = comment[-1]
        comment.send_keys(f"{commentText}")
        sleep(1)
        browser.find_element(By.CSS_SELECTOR, '.CommentAddForm_send_button__E21VQ').click()
        notification = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Успешно создано')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Одна из областей создания комментария не найдена (ввод комментария, кнопка, уведомление)")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        commentNew = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and contains(., 'Срибный Григорий') and .//p[contains(text(), '{commentText}')]]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Созданный комментарий не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    printSuccess(f"{commentText.replace(" комментарий", "")} комментарий успешно создан")
    return True
