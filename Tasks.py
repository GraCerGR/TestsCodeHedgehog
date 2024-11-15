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
from datetime import datetime
import sys
from Exeptions import *
from Queue import go_to_the_queue_tab

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

class Solution:
    def __init__(self, solution, language):
        self.solution = solution
        self.language = language

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
            f"Ошибка: Задача '{task.name}' с очками '{task.points}' и фильтрами '{', '.join(filters)}' не была найдена или не стала доступной.")
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
        printSuccess(f"Фильтр(-ы) '{filters_string}' работает(-ют)")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка скрытия фильтрации или отключения фильтра не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

def viewing_task_details(browser, section):
    solution = 0 # переменная для определения выполнения теста страницы последнего решения
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
        browser.execute_script("arguments[0].scrollIntoView();", taskButton)
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
        check(section.task.name, title, "Название задачи")

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
            else:
                solution = info

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Не удалось получить информацию о вердиктах.")
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    if solution:
        solution.click()
        if not last_solution(browser, section):
            return False

# --------------- Возврат на предыдущую страницу -------------------
    printSuccess(f"Детали задачи {title} отображаются")
    browser.back()
    go_to_the_tasks_tab(browser)
    return True
    """
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
    """

def last_solution(browser, section):
    try:
        header_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//h2[contains(@class, 'Title_title__Hbrke') and contains(@class, 'Title_title_level_2__mrJuT')]"))
        )
        task_name = header_element.find_element(By.TAG_NAME, 'a').text
        check(section.task.name, task_name, "Название задачи")
        printInfo(f"Название задачи: {task_name}")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Заголовок не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        description_info = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'TextInfo_text_info__spbMJ'))
        ).text
        description_info = description_info.replace("Перейти к списку решений других студентов", "").strip()
        # Разделение текста на части
        date, user_info, attempts_info = description_info.split(' | ')
        printInfo(f"Дата отправки: {date}")
        printInfo(f"Автор решения: {user_info} ")
        printInfo(f"{attempts_info}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Дата, имя пользователя и попытки не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        infos = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'FactsBlock_facts_block__dmWEx'))
        )
        info = infos.find_elements(By.TAG_NAME, 'p')
        for i in info:
            printInfo(f"{i.text}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Данные (язык, лимиты, баллы) не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        verdict = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'VerdictSection_current_verdict__K-ILx')]//p"))
        ).text
        printInfo(f"Вердикт: {verdict}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Вердикт не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        code_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ace_text-layer"))
        )
        # Извлечение текста из найденного элемента
        code_lines = code_element.find_elements(By.CSS_SELECTOR, ".ace_line")
        code_text = " ".join([line.text for line in code_lines])

#        code_lines = code_element.find_elements(By.CSS_SELECTOR, ".ace_line") # Код для вывода солюшена с переносами
#        code_text = "\n".join([line.text for line in code_lines])

        printInfo(f"Решение: {code_text[:50]}...")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Решение не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    printSuccess("Детали попытки доступны для просмотра")
    return True


def time_now():
    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")
    return formatted_datetime


def making_a_solution_of_task(browser, task, solution):

    go_to_the_tasks_tab(browser)

# Поиск задачи
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div[1]/span/input"))
        )

        for char in task.name:
            searchButton.send_keys(char)
            time.sleep(0.05)

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Поле поиска не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

# Вход в описание задачи
    try:
        taskButton = WebDriverWait(browser, 20).until(
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
    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Кнопка 'Отправить' не была найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки 'Отправить'. {e}")
        return False
# Установка языка
    try:
        language = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "Select_select__control__Z4598"))
        )
        browser.execute_script("arguments[0].scrollIntoView();", language)
        language.click()
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{solution.language}')]"))
        ).click()

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка при вводе языка")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
# Ввод решения
    try:
        text_area = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ace_text-input"))
        )

        text_area.send_keys(solution.solution)

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка при вводе решения")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        SendSolutionButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class, 'ant-btn') and contains(@class, 'Button_button__4z3Rc') and contains(@class, 'Button_button_type_accent__NGYDO') and span[text()='Отправить решение']]"
            ))
        )
        SendSolutionButton.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Ошибка отправки решения")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    # -------------- Ожидание notification и перезагрузка страницы --------------
    try:
        timeNow = time_now()
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//div[contains(@class, 'ant-notification-notice-message')]//p[contains(text(), 'Решение успешно отправлено')]"))
        )
        printSuccess("Решение успешно создано")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


def check_solution_in_queue(browser, timeNow, solution):

    # -------------- Переход в очередь и поиск данного решения --------------
    try:
        sleep(6)
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Обновить страницу']]"))
        ).click()
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )
        date_text = elements[0].find_element(By.XPATH, ".//td[contains(@class, 'ant-table-cell')][4]//span").text
        if date_text >= timeNow:
            # -------------- Переход в детали --------------
            try:
                button_details = elements[0].find_element(By.XPATH, ".//following::button[1]")
                button_details.click()
                printInfo(f"Кнопка деталей нажата")
            except (TimeoutException, NoSuchElementException):
                printExeption(f"Кнопка деталей не найдена")
                return False
            except Exception as e:
                printExeption(f"Тип ошибки: {type(e).__name__}")
                printExeption(f"Сообщение ошибки: {e}")
                return False

            try:
                code_element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ace_text-layer"))
                )
                # Извлечение текста из найденного элемента
                code_lines = code_element.find_elements(By.CSS_SELECTOR, ".ace_line")
                code_text = "\n".join([line.text for line in code_lines])

                code_text = code_text.lstrip('\n')
                if code_text.startswith('\n'):
                    code_text = code_text[1:]

                printInfo(f"{code_text}")
                printInfo(f"{solution.solution}")

            except (TimeoutException, NoSuchElementException):
                printExeption(f"Вердикт не найден")
                return False
            except Exception as e:
                printExeption(f"Тип ошибки: {type(e).__name__}")
                printExeption(f"Сообщение ошибки: {e}")
                return False
        else:
            printExeption(f"Созданное решение не найдено")
            return False

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Ошибка поиска решения в очереди")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
