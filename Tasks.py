from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
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
    def __init__(self, name, task: Task):
        self.name = name
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
    try:
        taskButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[2]"))
        )
        taskButton.click()
    except Exception:
        print("Ошибка: Кнопка задач не была найдена или не стала доступной.")
        return

    search_by_task_name(browser, module.section)
    viewing_statistics_in_the_module(browser, module)


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
        return

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
        return
    except Exception as e:
        print(f"Ошибка: Ошибка поиска задачи. {e}")
        return


# Просмотр статистики по количеству баллов и решённых задач в модуле
def viewing_statistics_in_the_module(browser, module: Module):
    try:
        # Ожидание элемента с заданными значениями
        section_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH, f"//div[contains(@class, 'ant-flex') and "
                          f"p[text()='{module.name}'] and "
                          f"following-sibling::div[contains(text(), '{module.taskCountCurrent}/{module.taskCountAll} задач')] and "
                          f"following-sibling::div[contains(text(), '{module.pointCountCurrent}/{module.pointCountAll} баллов')]]"
            ))
        )
        print("Модуль найден")

    except TimeoutException or NoSuchElementException:
        print(
            f"Ошибка: Модуль {module.name} с задачами {module.taskCountCurrent}/{module.taskCountAll} и баллами {module.pointCountCurrent}/{module.pointCountAll} не был найден или не стал доступной.")
        return
    except Exception as e:
        print(f"Ошибка: Ошибка поиска модуля. {e}")
        return