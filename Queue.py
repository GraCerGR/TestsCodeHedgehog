from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Exeptions import printExeption

import sys

def queues(browser, task_name, role):
    print(f"[{sys._getframe().f_code.co_name}] Начало теста вкладки queues")
    if not go_to_the_queue_tab(browser):
        return False
    if not displaying_a_page_with_solutions(browser, role):
        return False
    if not going_to_the_task_details_when_clicking_on_the_task_name(browser, task_name):
        return False
    return True  # Возвращаем True, если все проверки пройдены

# Переход на вкладку "Очередь"
def go_to_the_queue_tab(browser):
    try:
        queueButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[3]"))
        )
        queueButton.click()
        print(f"[{sys._getframe().f_code.co_name}] Переход на страницу 'Очередь' выполнен")
        return True
    except Exception:
        printExeption(f"[{sys._getframe().f_code.co_name}] Ошибка: Кнопка задач не была найдена или не стала доступной.")
        return False

# Тест отображения сообщения об отсутствии данных
def displaying_a_page_with_no_solutions(browser):
    try:
        empty_data_message = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//td[contains(@class, 'ant-table-cell')]//p[contains(text(), 'Кажется, здесь пока нет данных')]"))
        )
        print(f"[{sys._getframe().f_code.co_name}] Элемент с сообщением об отсутствии данных найден.")
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"[{sys._getframe().f_code.co_name}] Элемент с сообщением об отсутствии данных не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"[{sys._getframe().f_code.co_name}]Тип ошибки: {type(e).__name__}")
        printExeption(f"[{sys._getframe().f_code.co_name}]Сообщение ошибки: {e}")


# Тест отображения очереди решений
def displaying_a_page_with_solutions(browser, role):
    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )
        count = len(elements)
        print(f"[{sys._getframe().f_code.co_name}] Решения найдены: {count}")

    except TimeoutException or NoSuchElementException:
        printExeption(f"[{sys._getframe().f_code.co_name}] Решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"[{sys._getframe().f_code.co_name}]Тип ошибки: {type(e).__name__}")
        printExeption(f"[{sys._getframe().f_code.co_name}]Сообщение ошибки: {e}")

    if (role == "Student"):
        userNameClass = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "UserSection_user_section__Y45e8"))
        )
        username_element = userNameClass.find_element(By.XPATH, ".//p[contains(@class, 'Paragraph_paragraph__vZceR')]")
        username = username_element.text

        for element in elements:
            try:
                cell = element.find_element(By.XPATH,
                                            f".//span[contains(@class, 'Paragraph_paragraph__vZceR') and text()='{username}']")
                print(f"[{sys._getframe().f_code.co_name}] Найден элемент с автором:", cell.text)
            except Exception as e:
                printExeption(f"[{sys._getframe().f_code.co_name}] Элемент не пренадлежит студенту {username}:", e)
                return False

    try:
        page_size_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME,
                "ant-select-selection-item"  # Это класс для элемента, который отображает выбранный размер страницы
            ))
        )

        page_size_text = page_size_element.text
        page_size = int(page_size_text.split()[0])
        print(f"[{sys._getframe().f_code.co_name}] Максимальное число элементов на странице:", page_size)

        if count > page_size:
            raise ValueError(f"[{sys._getframe().f_code.co_name}] На странице больше элементов чем {page_size}")
            return False

        print(f"[{sys._getframe().f_code.co_name}] Очередь отображается")
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"[{sys._getframe().f_code.co_name}] Элемент не найден. {e}")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"[{sys._getframe().f_code.co_name}]Тип ошибки: {type(e).__name__}")
        printExeption(f"[{sys._getframe().f_code.co_name}]Сообщение ошибки: {e}")


# Обновление страницы без обновления окна браузера. Пока не заню как проверять
# def updating_the_page_without_updating_browser(browser):

# Переход на страницу деталей задачи при нажатии на название задачи в попытке
def going_to_the_task_details_when_clicking_on_the_task_name(browser, task_name):
    try:
        taskLink = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{task_name}']"))
        )
        taskLink.click()

    except TimeoutException or NoSuchElementException:
        printExeption(f"[{sys._getframe().f_code.co_name}] Элемент '{task_name}' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"[{sys._getframe().f_code.co_name}]Тип ошибки: {type(e).__name__}")
        printExeption(f"[{sys._getframe().f_code.co_name}]Сообщение ошибки: {e}")

    try:
        taskTitle = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h2[text()='{task_name}']"))
        )
        print(f"[{sys._getframe().f_code.co_name}] Переход на страницу деталей выполнен")
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"[{sys._getframe().f_code.co_name}] Элемент '{task_name}' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"[{sys._getframe().f_code.co_name}]Тип ошибки: {type(e).__name__}")
        printExeption(f"[{sys._getframe().f_code.co_name}]Сообщение ошибки: {e}")

