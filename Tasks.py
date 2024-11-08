from fileinput import close
from importlib.metadata import files
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from Exeptions import *

class Task:
    def __init__(self, name, points):
        self.name = name
        self.points = points

class Section:
    def __init__(self, name, taskCountCurrent, taskCountAll, pointCountCurrent, pointCountAll, task: Task):
        self.name = name
        self.taskCountCurrent = taskCountCurrent
        self.taskCountAll = taskCountAll
        self.pointCountCurrent = pointCountCurrent
        self.pointCountAll = pointCountAll
        self.task = task

class Module:
    def __init__(self, name, taskCountCurrent, taskCountAll, pointCountCurrent, pointCountAll, section: Section):
        self.name = name
        self.taskCountCurrent = taskCountCurrent
        self.taskCountAll = taskCountAll
        self.pointCountCurrent = pointCountCurrent
        self.pointCountAll = pointCountAll
        self.section = section

def tasks(browser, module):
    # Тесты
    printInfo(f"Начало теста вкладки tasks")
    # Переход на вкладку "Задачи"
    if not go_to_the_tasks_tab(browser):
        return False
    if not viewing_task_details(browser, module.section):
        return False
    if not search_by_task_name(browser, module.section):
        return False
    if not viewing_statistics_in_the_module(browser, module):
        return False
    if not viewing_statistics_in_the_section(browser, module.section):
        return False
    return True  # Возвращаем True, если все проверки пройдены

# Переход на вкладку "Задачи"
def go_to_the_tasks_tab(browser):
    try:
        taskButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[2]"))
        )
        taskButton.click()
        printSuccess(f"Переход на страницу 'Задачи' выполнен")
        return True
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Кнопка задач не была найдена или не стала доступной.")
        return False


# Поиск по названию задачи
def search_by_task_name(browser, section):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div[1]/span/input"))
        )

        # При быстром вводе предыдующие символы не успевают отобразиться (в поисковике остаётся только последний символ)
        # searchButton.send_keys(section.task.name)
        # Поэтому посимвольный ввод
        for char in section.task.name:
            searchButton.send_keys(char)
            time.sleep(0.1)

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(@class, 'SectionStructure_section_structure_button__ZU4zy') and "
                           f".//p[text()='{section.name}'] and "
                           f".//following::p[text()='{section.task.name}'] and "
                           f".//following::p[text()='{section.task.points}']]"))
        )
        printInfo(f"Задача найдена")

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Секция '{section.name}' с задачей '{section.task.name}' и очками '{section.task.points}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
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
        printSuccess(f"Поиск работает.")
        sleep(3)
        return True
    else:
        printInfo(f"Ошибка: Поле поиска не отчищено")
        return False

# Просмотр статистики по количеству баллов и решённых задач в модуле
def viewing_statistics_in_the_module(browser, module: Module):
    try:
        # Ожидание элемента с заданными значениями
        module_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                          f"//div[contains(@class, 'ant-flex') and "
                          f"p[text()='{module.name}'] and "
                          f"div[contains(text(), '{module.taskCountCurrent}/{module.taskCountAll} задач')] and "
                          f"div[contains(text(), '{module.pointCountCurrent}/{module.pointCountAll} баллов')]]"
            ))
        )
        printSuccess(f"Модуль найден")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Модуль {module.name} с задачами {module.taskCountCurrent}/{module.taskCountAll} и баллами {module.pointCountCurrent}/{module.pointCountAll} не был найден или не стал доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска модуля. {e}")
        return False

# Просмотр статистики по количеству баллов и решённых задач в секции
def viewing_statistics_in_the_section(browser, section):
    try:
        section_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                        f"//div[contains(@class, 'ant-flex') and "
                        f"p[text()='{section.name}'] and "
                        f"div[contains(text(), '{section.taskCountCurrent}/{section.taskCountAll} задач')] and "
                        f"div[contains(text(), '{section.pointCountCurrent}/{section.pointCountAll} баллов')]]"
                ))
            )
        printSuccess(f"Секеция найдена")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Ошибка: Секция {section.name} с задачами {section.taskCountCurrent}/{section.taskCountAll} и баллами {section.pointCountCurrent}/{section.pointCountAll} не была найдена или не стала доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска секции. {e}")
        return False

# Просмотр дедлайнов
# На фронте пока не реализовано

# Настройка фильтрации
def set_t_filter(browser, filters: list, task: Task):
    go_to_the_tasks_tab(browser)
    try:
        filter_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Фильтрации']]"
            ))
        )
        filter_button.click()
        printInfo(f"Кнопка Фильтрации найдена")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент 'Фильтрация' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

# ----------------------- Поиск нужного фильтра -----------------------
    try:
        sleep(1)
        filtering_section = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div"))
        )
        filtering_section.find_element(By.XPATH, "//h3[text()='Фильтрации']")
        printInfo(f"Окно фильтрации найдено")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Окно 'Фильтрации' не найдено.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # Перебор списка фильтров
    for filter in filters:
        try:
            filtering_section.find_element(By.XPATH, f".//p[text()='{filter}' and contains(@class, 'Paragraph_paragraph__vZceR')]").click()
            printInfo(f"Фильтр '{filter}' найден")
            sleep(1)
        except (TimeoutException, NoSuchElementException):
            printExeption(f"Фильтр '{filter}' не найден.")
            return False
        except Exception as e:
            printExeption(f"Тип ошибки: {type(e).__name__}")
            printExeption(f"Сообщение ошибки: {e}")
            return False

    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//tbody[contains(@class, 'ant-table-tbody') and "
                           f".//p[text()='{task.name}'] and "
                           f".//following::p[text()='{task.points}']]"))
        )
        printInfo(f"Задача '{task.name}' найдена")
    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Задача '{task.name}' с очками '{task.points}' и фильтром '{filter}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        for filter in filters:
            filtering_section.find_element(By.XPATH,f".//p[text()='{filter}' and contains(@class, 'Paragraph_paragraph__vZceR')]").click()
        filter_button.click()
        filters_string = ", ".join(filters)
        printSuccess(f"Фильтр {filters_string} работает")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка скрытия фильтрации или отключения фильтра не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


def script_making_a_solution_of_task(browser, task):

    go_to_the_tasks_tab(browser)

# Поиск задачи
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div[1]/span/input"))
        )

        for char in task.name:
            searchButton.send_keys(char)
            time.sleep(0.1)

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

# Вход в описание задачи
    try:
        taskButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//p[@class='Paragraph_paragraph__vZceR' and text()='{task.name}']"))
        )
        taskButton.click()

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Задача '{task.name}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

# Нажатие "Отправить"
    try:
        sendButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'ant-btn') and contains(@class, 'Button_button__4z3Rc') and span[text()='Отправить']]"
            ))
        )
        sendButton.click()
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки 'Отправить'. {e}")
        return False

    try:
        language = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, '/html/body/div/div/div[2]/div/div/form/div/div[2]/div[1]/div/div[1]/div/div[1]/div[3]/input'
            ))
        )
        language.click()
        language.send_keys("C++")
        language.send_keys(Keys.ENTER)

        SendSolutionButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class, 'ant-btn') and contains(@class, 'Button_button__4z3Rc') and contains(@class, 'Button_button_type_accent__NGYDO') and span[text()='Отправить решение']]"
            ))
        )
        SendSolutionButton.click()
        printSuccess(f"Решение создано")

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка отправки решения. {e}")
        return False


def viewing_task_details(browser, section):
    # Поиск задачи
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div[1]/span/input"))
        )

        # При быстром вводе предыдующие символы не успевают отобразиться (в поисковике остаётся только последний символ)
        # searchButton.send_keys(section.task.name)
        # Поэтому посимвольный ввод
        for char in section.task.name:
            searchButton.send_keys(char)
            time.sleep(0.05)

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False
    try:
        taskButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(@class, 'SectionStructure_section_structure_button__ZU4zy') and "
                           f".//p[text()='{section.name}'] and "
                           f".//following::p[text()='{section.task.name}'] and "
                           f".//following::p[text()='{section.task.points}']]"))
        )
        printInfo(f"Задача найдена")
    # Вход в описание задачи
        taskButton.find_element(By.XPATH, f".//following::p[text()='{section.task.name}']").click()
        printInfo(f"Вход в детали задачи '{section.task.name}' выполнен")
    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Задача '{section.task.name}' в секции {section.name} с баллами '{section.task.points}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        title_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "HeaderPage_header_page__k3oIt"))
        )
        title = title_element.find_element(By.TAG_NAME, "h2").text
        printInfo(f"Название: {title}")

        infos = title_element.find_elements(By.CLASS_NAME, "Paragraph_paragraph__vZceR")
        for info in infos:
            printInfo(f"{info.text}")

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Не удалось получить информацию о назавнии, баллах и/или успешных решениях.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        verdict_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "TaskClassVerdicts_task_class_verdicts_card__ak4r6"))
        )

        infos = verdict_element.find_elements(By.CLASS_NAME, "Paragraph_paragraph__vZceR")
        for info in infos:
            text = info.text
            if text != "Перейти к моему последнему решению":
                printInfo(f"Вердикт: {info.text}")

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Не удалось получить информацию о назавнии, баллах и/или успешных решениях.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        back_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Назад']]"
            ))
        )
        back_button.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент 'Назад' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Выход из деталей задачи не выполнен: {e}")
    return True