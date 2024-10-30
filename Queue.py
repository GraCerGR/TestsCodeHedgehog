from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Exeptions import *

def queues(browser, task_name, role):
    printInfo(f"Начало теста вкладки queues")
    if not go_to_the_queue_tab(browser):
        return False
    if not displaying_a_page_with_solutions(browser, role):
        return False
    if not updating_the_page_without_updating_browser(browser):
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
        printInfo(f"Переход на страницу 'Очередь' выполнен")
        return True
    except Exception:
        printExeption(f"Ошибка: Кнопка задач не была найдена или не стала доступной.")
        return False

# Тест отображения сообщения об отсутствии данных
def displaying_a_page_with_no_solutions(browser):
    try:
        empty_data_message = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//td[contains(@class, 'ant-table-cell')]//p[contains(text(), 'Кажется, здесь пока нет данных')]"))
        )
        printInfo(f"Элемент с сообщением об отсутствии данных найден.")
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"Элемент с сообщением об отсутствии данных не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


# Тест отображения очереди решений
def displaying_a_page_with_solutions(browser, role):
    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )
        count = len(elements)
        printInfo(f"Решения найдены: {count}")

    except TimeoutException or NoSuchElementException:
        printExeption(f"Решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

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
                printInfo(f"Найден элемент с автором: {cell.text}")
            except Exception as e:
                printExeption(f"Элемент не пренадлежит студенту {username}:", e)
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
        printInfo(f"Максимальное число элементов на странице: {page_size}")

        if count > page_size:
            raise ValueError(f"На странице больше элементов чем {page_size}")
            return False

        printInfo(f"Очередь отображается")
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"Элемент не найден. {e}")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


# Обновление страницы без обновления окна браузера. Пока не заню как проверять
def updating_the_page_without_updating_browser(browser):
    try:
        rows = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row')]"))
        )
        count = len(rows)
        printInfo(f"Решения найдены: {count}")

    except TimeoutException or NoSuchElementException:
        printExeption(f"Решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        fourth_cell_values = []
        for row in rows:
            # Находим четвертую ячейку
            fourth_cell = row.find_elements(By.TAG_NAME, "td")[3]
            cell_text = fourth_cell.text
            fourth_cell_values.append(cell_text)

    except TimeoutException or NoSuchElementException:
        printExeption(f"Ячейка с датой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

# ----------- Поиск кнопки обновления -----------
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Обновить страницу']]"))
        ).click()

    except TimeoutException or NoSuchElementException:
        printExeption(f"Кнопка обновления не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

#----------- Повторный поиск -----------
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        ) # Это нужно, чтобы дождаться загрузки таблицы
        rows_new = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row')]"))
        )
        count_new = len(rows_new)
        printInfo(f"Обновлённые решения найдены: {count_new}")

    except TimeoutException or NoSuchElementException:
        printExeption(f"Обновлённые решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

# ----------- Проверка соответствия дат -----------
    try:
        if (count_new != count):
            printExeption(f"Число элементов не совпадает ({count_new}, {count})")
            return False
        for i, row in enumerate(rows_new):

            try:
                cell = row.find_element(By.XPATH,
                                            f".//span[contains(@class, 'Paragraph_paragraph__vZceR') and text()='{fourth_cell_values[i]}']")
                printInfo(f"Найден элемент с датой: {cell.text}")
            except Exception:
                printExeption(f"Элемент с датой {fourth_cell_values[i]} не найден")
                return False
        printInfo(f"Обновление страницы прошло успешно")
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"Ячейка с датой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


# Переход на страницу деталей задачи при нажатии на название задачи в попытке
def going_to_the_task_details_when_clicking_on_the_task_name(browser, task_name):
    try:
        taskLink = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{task_name}']"))
        )
        taskLink.click()

    except TimeoutException or NoSuchElementException:
        printExeption(f"Элемент '{task_name}' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        taskTitle = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h2[text()='{task_name}']"))
        )
        printInfo(f"Переход на страницу деталей выполнен")
    except TimeoutException or NoSuchElementException:
        printExeption(f"Элемент '{task_name}' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        back_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Назад']]"
            ))
        )
        back_button.click()
        return True
    except TimeoutException or NoSuchElementException:
        printExeption(f"Элемент 'Назад' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Выход из деталей задачи не выполнен: {e}")
