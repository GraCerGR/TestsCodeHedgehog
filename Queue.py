from fileinput import close

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def queues(browser):
    go_to_the_queue_tab(browser)
    displaying_a_page_with_solutions(browser)

# Переход на вкладку "Очередь"
def go_to_the_queue_tab(browser):
    try:
        queueButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[3]"))
        )
        queueButton.click()
    except Exception:
        print("Ошибка: Кнопка задач не была найдена или не стала доступной.")
        return False

# Тест отображения сообщения об отсутствии данных
def displaying_a_page_with_no_solutions(browser):
    try:
        empty_data_message = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//td[contains(@class, 'ant-table-cell')]//p[contains(text(), 'Кажется, здесь пока нет данных')]"))
        )
        print("Элемент с сообщением об отсутствии данных найден.")
        return True
    except NoSuchElementException or TimeoutException:
        print("Элемент с сообщением об отсутствии данных не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


# Тест отображения очереди решений
def displaying_a_page_with_solutions(browser):
    try:
        elements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'ant-table-row') and contains(@class, 'ant-table-row-level-0')]"))
        )
        print("Решения найдены")

    except NoSuchElementException or TimeoutException:
        print("Решения не найдены")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

    try:
        page_size_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@class='ant-select ant-select-outlined ant-pagination-options-size-changer css-14h5sa0 ant-select-single ant-select-show-arrow ant-select-show-search']//span[@class='ant-select-selection-item' and @title='50  / страница']")
            ))

        # Получение текста элемента
        page_size_text = page_size_element.text
        print("Количество страниц:", page_size_text)

    except Exception as e:
        print(f"Произошла ошибка: {e}")