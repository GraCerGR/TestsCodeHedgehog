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

class TaskData:
    def __init__(self, user, task_name, language, submission_date, verdict):
        self.user = user
        self.task_name = task_name
        self.language = language
        self.submission_date = submission_date
        self.verdict = verdict

def postmoderation(browser, task_name, role):
    printInfo(f"Начало теста вкладки queues")
    if not go_to_the_postmoderation_tab(browser):
        return False
    if not search_by_task_name(browser, task_name):
        return False
    sleep(2)
    if not displaying_a_page_with_solutions(browser, role):
        return False
    sleep(2)
    if not displaying_the_page_with_details(browser, task_name):
        return False
    sleep(2)
    if not updating_the_page_without_updating_browser(browser):
        return False
    sleep(2)
    if not going_to_the_task_details_when_clicking_on_the_task_name(browser, task_name):
        return False
    sleep(2)
    if not going_to_the_result_when_clicking_on_the_user_name(browser):
        return False
    return True  # Возвращаем True, если все проверки пройдены

# Переход на вкладку "Постмодерация"
def go_to_the_postmoderation_tab(browser):
    try:
        Button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[4]"))
        )
        Button.click()
        printSuccess(f"Переход на страницу 'Постмодерация (ожидающие проверку решения)' выполнен")
        return True
    except Exception:
        printExeption(f"Ошибка: Кнопка постмодерации не была найдена или не стала доступной.")
        return False

# Тест отображения сообщения об отсутствии данных
def displaying_a_page_with_no_solutions(browser):
    try:
        empty_data_message = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//td[contains(@class, 'ant-table-cell')]//p[contains(text(), 'Кажется, здесь пока нет данных')]"))
        )
        printSuccess(f"Элемент с сообщением об отсутствии данных найден.")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент с сообщением об отсутствии данных не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


# Тест отображения постмодерации решений
def displaying_a_page_with_solutions(browser, role):
    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )
        count = len(elements)
        printInfo(f"Решения найдены: {count}")

    except (TimeoutException, NoSuchElementException):
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

        printSuccess(f"Очередь в постмодерации отображается")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент не найден. {e}")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


# Обновление страницы без обновления окна браузера.
def updating_the_page_without_updating_browser(browser):
    try:
        rows = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row')]"))
        )
        count = len(rows)
        printInfo(f"Решения найдены: {count}")

    except (TimeoutException, NoSuchElementException):
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

    except (TimeoutException, NoSuchElementException):
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

    except (TimeoutException, NoSuchElementException):
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

    except (TimeoutException, NoSuchElementException):
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
        printSuccess(f"Обновление страницы прошло успешно")
        return True
    except (TimeoutException, NoSuchElementException):
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

    except (TimeoutException, NoSuchElementException):
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
        printSuccess(f"Переход на страницу деталей выполнен")
    except (TimeoutException, NoSuchElementException):
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
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент 'Назад' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Выход из деталей задачи не выполнен: {e}")


# Переход на страницу результатов при нажатии на имя пользователя в попытке
def going_to_the_result_when_clicking_on_the_user_name(browser):
    try:
        element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )
        first_column = element.find_element(By.XPATH, ".//td[1]//span")  # Находим <span> внутри первого <td>
        first_column_text = first_column.text  # Получаем текст
        printInfo(f"Имя автора решения: {first_column_text}")
        first_column.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Имя автора решения или решение не найдено")
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

# Поиск по названию задачи
def search_by_task_name(browser, task_name):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div/div/span/input"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода поиска не найдено.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:

        for char in task_name:
            searchButton.send_keys(char)
            time.sleep(0.1)
        sleep(2)
        task_element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[span[text()='{task_name}']]"))
        )
        printInfo(f"Задача найдена")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Задача '{task_name}' не найдна.")
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
        return True
    else:
        printInfo(f"Ошибка: Поле поиска не отчищено")
        return False

# Отображение страницы с деталями попытки
def displaying_the_page_with_details(browser, task_name):
    name = None
    date = None
    language = None
    is_sorted = True
# -------------- Поиск задачи --------------
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div/div/span/input"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода поиска не найдено.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        for char in task_name:
            searchButton.send_keys(char)
            time.sleep(0.1)

        task_element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[span[text()='{task_name}']]"))
        )
        printInfo(f"Задача найдена")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Задача '{task_name}' не найдна.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False
# -------------- Получение данных задачи --------------
    try:
        # Находим родительский элемент (строку таблицы)
        row_element = task_element.find_element(By.XPATH, "./ancestor::tr")

        # Извлекаем все ячейки из строки таблицы
        cells = row_element.find_elements(By.TAG_NAME, "td")

        taskdata = TaskData(
            user = cells[0].text,
            task_name = cells[1].text,
            language = cells[2].text,
            submission_date = cells[3].text,
            verdict = cells[4].text,
        )

        data = {
            'user': cells[0].text,
            'task_name': cells[1].text,
            'language': cells[2].text,
            'submission_date': cells[3].text,
            'verdict': cells[4].text,
        }

        printInfo(f"Данные задачи '{task_name}' найдены: {data}")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Данные задачи '{task_name}' не найдны.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False
# -------------- Переход в детали --------------
    try:
        button_details = task_element.find_element(By.XPATH, ".//following::button[1]")
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
        name = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h3[contains(text(), 'Постмодерация') and .//a[text()='{taskdata.task_name}']]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Заголовок не найден, или название задачи не соответствует заголовку")

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        date = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//p[contains(text(), '{taskdata.submission_date}') and contains(., '{taskdata.user}')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Дата или имя пользователя не найдены или не соответствуют данным")

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        language = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//p[contains(text(), 'Язык: {taskdata.language}')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Язык не найден или не соответствует данным")

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

# -------------- Проверка последовательности тестов --------------
    try:
        testButton = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-collapse-header') and .//span[text()='Развернуть список тестов']]"))
        )
        testButton.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Меню тестов не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        table_container = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Развернуть список тестов']/ancestor::div[contains(@class, 'ant-collapse-item')]"))
        )
        sleep(1)
        rows = table_container.find_elements(By.CSS_SELECTOR, ".ant-table-tbody tr")

        test_numbers = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:  # Убедитесь, что ячейки существуют
                test_number = cells[0].text.strip()  # Получаем текст из первой ячейки
                if(test_number == 'Кажется, здесь пока нет данных 🔎\nНо мы работаем над их появлением 👀'):
                    printInfo("Тесты отсутствуют")
                    break
                test_numbers.append(int(test_number))  # Преобразуем в целое число
        if test_numbers:
            # Проверяем, что номера тестов расположены в порядке возрастания
            is_sorted = all(test_numbers[i] <= test_numbers[i + 1] for i in range(len(test_numbers) - 1))

            if is_sorted:
                printSuccess("Номера тестов расположены в порядке возрастания.")
            else:
                printExeption("Номера тестов не расположены в порядке возрастания.")

    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False
    if  ((name is not None) and (date is not None) and (language is not None) and is_sorted):
        printSuccess(f"Детали задачи '{taskdata.task_name}' соответствуют данным")
    else:
        printExeption(f"Детали задачи '{taskdata.task_name}' не соответствуют данным")

# Выход
    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc')]/span[text()='Закрыть']"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка выхода не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
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
        browser.refresh()
        return True
    else:
        printInfo(f"Ошибка: Поле поиска не отчищено")
        return False


# Настройка фильтрации
def set_p_filter(browser, filters: list, task_name):
    go_to_the_postmoderation_tab(browser)
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

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Сбросить']"))
    ).click() # Отчистить фильтр от прошлых тестов (если прошлые тесты обвалятся)
    # Перебор списка фильтров
    for filter in filters:
        try:
            filtering_section.find_element(By.XPATH,
                                           f".//p[text()='{filter}' and contains(@class, 'Paragraph_paragraph__vZceR')]").click()
            sleep(1)
            printInfo(f"Фильтр '{filter}' найден")
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
                           f".//span[text()='{task_name}']]"))
        )
        printInfo(f"Задача '{task_name}' найдена")
    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Задача '{task_name}' c фильтрами '{', '.join(filters)}' не была найдена или не стала доступной.")
        return False # Уберу, чтобы остальные тесты не валились
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        for i in range(len(filters) - 1, -1, -1):
            filter = filters[i]
            filtering_section.find_element(By.XPATH,
                                           f".//p[text()='{filter}' and contains(@class, 'Paragraph_paragraph__vZceR')]").click()
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