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

def rating(browser, role, module_name, user_name):
    printInfo(f"Начало теста вкладки users")
    if not go_to_the_rating_tab(browser):
        return False
    if not displaying_a_page_with_rating(browser, role):
        return False
    if not search_by_module_name(browser, module_name, user_name, role):
        return False
    if role == 'Teacher':
        if not going_to_the_result_when_clicking_on_the_user_name(browser):
            return False
    return True


# Переход на вкладку "Пользователи"
def go_to_the_rating_tab(browser):
    try:
        queueButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[6]"))
        )
        queueButton.click()
        printSuccess(f"Переход на страницу 'Рейтинг' выполнен")
        return True
    except Exception:
        printExeption(f"Ошибка: Кнопка Рейтинг не была найдена или не стала доступной.")
        return False

def displaying_a_page_with_rating(browser, role):
    try:
        # Ожидание, пока элемент загрузки исчезнет
        WebDriverWait(browser, 10).until(
            EC.invisibility_of_element((By.CLASS_NAME, 'ant-skeleton'))
        )
        printInfo("Таблица загрузки пропала")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Таблица загрузки не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        # Ожидание, пока родительский элемент будет доступен
#        parent_element = WebDriverWait(browser, 10).until(
#            EC.presence_of_element_located((By.CLASS_NAME, 'ant-table-content'))
#        )
#        WebDriverWait(browser, 10).until(
#            lambda d: parent_element.find_element(By.CLASS_NAME, 'Paragraph_paragraph__vZceR')
#        )
#        printInfo(f"Элемент с классом 'Paragraph_paragraph__vZceR' появился внутри родительского элемента.")
#        sleep(1) # Таблица с данными не успевает отрисоваться после исчезновения загрузочной таблицы
#        table_element = WebDriverWait(browser, 10).until(
#            EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy RatingTable_cell_link__khXgH')]]"))
#        )
        sleep(1)
        if role == 'Teacher':
            table_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy RatingTable_cell_link__khXgH')]]"))
            )
        else:
            table_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//div[contains(@class, 'RatingTable_cell_link__khXgH')]]"))
            )
        table = table_element.find_element(By.XPATH, "..")

        # print(table)
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
        data_list = []

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            data = [col.text for col in columns]
            printInfo(f"{data}")
            data_list.append(data)

        # Проверка порядка мест и баллов
        places = [int(item[0]) for item in data_list]
        scores = [int(item[2]) for item in data_list]

        places_sorted = sorted(places)
        if places == places_sorted:
            printInfo("Места идут в порядке возрастания.")
        else:
            printExeption(f"Места не идут в порядке возрастания")
            return False

        scores_sorted = sorted(scores, reverse=True)
        if scores == scores_sorted:
            printInfo("Баллы идут в порядке убывания.")
        else:
            printExeption("Баллы не идут в порядке убывания.")
            return False
        printSuccess(f"Страница рейтинга отображается")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Таблица не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


def search_by_module_name(browser, module_name, user_name, role):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div[1]/div[3]/input"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода поиска не найдено.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска. {e}")
        return False

    try:

        for char in module_name:
            searchButton.send_keys(char)
            time.sleep(0.05)
        searchButton.send_keys(Keys.ENTER)
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[{'a' if role == 'Teacher' else 'div'}[p[text()='{user_name}']]]"))
        )
        printInfo(f"Пользователь найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователь '{user_name}' не найден.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    #нажатие на крестик
    try:
        closeButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-8mmkcg'))
        )
        closeButton.click()

        printSuccess(f"Поиск работает")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"closeButton не найден.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

# Переход на страницу результатов при нажатии на имя пользователя
def going_to_the_result_when_clicking_on_the_user_name(browser):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy RatingTable_cell_link__khXgH')]]"))
        )
        first_column = element.find_element(By.XPATH, ".//td[2]//p")
        first_column_text = first_column.text
        printInfo(f"Имя пользователя: {first_column_text}")
        first_column.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Имя пользователя не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h2[text()='Результаты']"))
        )
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'ant-flex') and .//p[text()='Пользователь:'] and .//a[text()='{first_column_text}']]"
            ))
        )
        printSuccess(f"Переход на страницу результатов пользователя {first_column_text} выполнен")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Переход на страницу результатов пользователя {first_column_text} не выполнен.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        sleep(1)
        back_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Назад']]"
            ))
        )
        back_button.click()
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент 'Назад' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Выход из деталей задачи не выполнен: {e}")