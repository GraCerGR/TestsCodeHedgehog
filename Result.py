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

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class TaskInRating:
    def __init__(self, moduleName, sectionName, taskName):
        self.moduleName = moduleName
        self.sectionName = sectionName
        self.taskName = taskName

def result(browser, user: User, task):
    printInfo(f"Начало теста страницы рейтинга")
    if not go_to_the_result_tab(browser, user):
        return False
    print()

    if not displaying_modules_and_sections_names(browser):
        return False
    print()

    if not displaying_tasks_with_attempts(browser, task):
        return False
    return True


# Переход на вкладку "Результаты"
def go_to_the_result_tab(browser, user):
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[5]"))
        ).click()
    except Exception:
        printExeption(f"Ошибка: Кнопка Рейтинг не была найдена или не стала доступной.")
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
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ant-flex') and contains(., 'Пользователь:') and .//a[contains(text(), 'Срибный Григорий')]]"))
        )

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поля информации о результатах (заголовок, имя пользователя) не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    printSuccess(f"Страница результатов пользователя '{user.name}' открыта")
    return True

# Отображение страницы с названииями модулей и секций
def displaying_modules_and_sections_names(browser):
    try:
        modules = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'ModuleStructure_module_structure__Dd7NK'))
            )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модули не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        for module in modules:
            moduleName = module.find_element(By.CSS_SELECTOR,
                                                'p.Paragraph_paragraph__vZceR.Paragraph_paragraph_weight_bold__uSpls').text.strip()
            printInfo(f"Модйль найден: {moduleName}")
            sectionNames = []
            sections = module.find_elements(By.CLASS_NAME, 'SectionStructure_section_structure_button__zUl-G')
            for section in sections:
                sectionName = section.find_element(By.CSS_SELECTOR, 'p.Paragraph_paragraph__vZceR.Paragraph_paragraph_weight_bold__uSpls').text
                sectionNames.append(sectionName)
            printInfo(f"Секции модуля: {sectionNames}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поля информации о результатах (название модулей, секции) не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False
    printSuccess(f"Страница результатов с модулями и секциями отображается корректно")
    return True

# Отображение задач, имеющих хотя бы одну попытку, в секции
def displaying_tasks_with_attempts(browser, task: TaskInRating):
    try:
        module = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,f"//div[contains(@class, 'ModuleStructure_module_structure__Dd7NK')]"
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
        section = module.find_element(By.XPATH,f"//div[contains(@class, 'SectionStructure_section_structure__oiisl') and .//p[text()='{task.sectionName}']]")
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
            EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'ant-table-row') "
                                                      f"and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy ClassTasksSectionTable_cell_link__lOcSE') and //p[text()='{task.taskName}']]]"))
        )
        printInfo(f"Задача '{task.taskName}' найдена")

        cells = taskElement.find_elements(By.TAG_NAME, "td")

        data = f"""
                №: {cells[0].text}, 
                Имя: {cells[1].text}, 
                Баллы: {cells[2].text}, 
                Срок: {cells[3].text}, 
                Вердикты: {cells[4].text.replace("\n", ", ")},
                Последний комментарий: {cells[5].text}"""

        printInfo(f"Данные решения найдены: {data}")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Задача '{task.taskName}' не найдена в секции '{task.sectionName}' модуля '{task.moduleName}'")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    printSuccess(f"Отображение задач функционирует")
    return True