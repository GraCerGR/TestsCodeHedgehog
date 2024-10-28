from fileinput import close

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    # Переход на вкладку "Задачи"
    go_to_the_tasks_tab(browser)

    # Тесты
    search_by_task_name(browser, module.section)
    viewing_statistics_in_the_module(browser, module)
    viewing_statistics_in_the_section(browser, module.section)

# Переход на вкладку "Задачи"
def go_to_the_tasks_tab(browser):
    try:
        taskButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[2]"))
        )
        taskButton.click()
    except Exception:
        print("Ошибка: Кнопка задач не была найдена или не стала доступной.")
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
        print(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(@class, 'SectionStructure_section_structure_button__ZU4zy') and "
                           f".//p[text()='{section.name}'] and "
                           f".//following::p[text()='{section.task.name}'] and "
                           f".//following::p[text()='{section.task.points}']]"))
        )
        print("Задача найдена")

    except TimeoutException or NoSuchElementException:
        print(
            f"Ошибка: Секция '{section.name}' с задачей '{section.task.name}' и очками '{section.task.points}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        print(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    #нажатие на крестик
    try:
        closeButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input-clear-icon'))
        )
        closeButton.click()
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

    #Проверка, что поле поиска отчистилось
    value = searchButton.get_attribute('value')
    if value == '':
        print("Поле поиска отчищено.")
    else:
        print("Ошибка: Поле поиско не отчищено")
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
        print("Модуль найден")

    except TimeoutException or NoSuchElementException:
        print(
            f"Ошибка: Модуль {module.name} с задачами {module.taskCountCurrent}/{module.taskCountAll} и баллами {module.pointCountCurrent}/{module.pointCountAll} не был найден или не стал доступной.")
        return False
    except Exception as e:
        print(f"Ошибка: Ошибка поиска модуля. {e}")
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
        print("Секеция найдена")

    except TimeoutException or NoSuchElementException:
        print(f"Ошибка: Секция {section.name} с задачами {section.taskCountCurrent}/{section.taskCountAll} и баллами {section.pointCountCurrent}/{section.pointCountAll} не была найдена или не стала доступной.")
        return False
    except Exception as e:
        print(f"Ошибка: Ошибка поиска секции. {e}")
        return False

# Просмотр дедлайнов
# На фронте пока не реализовано

# Настройка фильтрации
# Задачи по умолчанию пока +- одинаковые (нерешены, без попыток).
# Если какое-то решение отправить, то будет Ожидает вердикта, после Отклонено (компилятор не работает)
# Чтобы протестировать фильтрацию, нужно иметь предсозданные задачи со своими вердиктами тестирования и постмодерации.
# Автоматизировать это долго и пока не известно, есть ли смысл вообще это делать, поэтому пока не буду.


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
        print(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

# Вход в описание задачи
    try:
        taskButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//p[@class='Paragraph_paragraph__vZceR' and text()='{task.name}']"))
        )
        taskButton.click()

    except TimeoutException or NoSuchElementException:
        print(
            f"Ошибка: Задача '{task.name}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        print(f"Ошибка: Ошибка поиска задачи. {e}")
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
        print(f'Ошибка: Ошибка поиска кнопки "Отправить". {e}')
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
        print('Решение создано')

    except Exception as e:
        print(f'Ошибка: Ошибка отправки решения. {e}')
        return False