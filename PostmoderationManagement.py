import random
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

from Queue import go_to_the_queue_tab
from Tasks import *
from Postmoderation import *

def postmoderation_management(browser, verdict):
    printInfo(f"Начало теста процесса постмодерации")

    # Для лучшего теста нужно заранее хоть одно решение создать
    #if not making_a_solution_for_tests(browser):
    #    return False

    if not go_to_the_postmoderation_tab(browser):
        return False
    if not viewing_tests(browser):
        return False
    return False
    # Переотправку решения делаю в очереди, т. к. предсозданная задача с автоматической установкой вердикта
    if not go_to_the_queue_tab(browser):
        return False
    if not resending_the_students_decision(browser):
        return False

    sleep(30)  # Задержка для успешной компиляции и выставления вердикта
    if not update_page(browser):
        printExeption("Ошибка обновления страницы")
        return False
    # Удаление вердикта делаю в очереди, т. к. в постмодерации у всех решений не вердикта
    if not go_to_the_queue_tab(browser):
        return False
    if not issuing_a_delete_verdict(browser):
        return False

    if not go_to_the_postmoderation_tab(browser):
        return False
    if not viewing_tests(browser):
        return False
    if not issuing_a_verdict(browser, verdict):
        return False

    # Просмотр тестов - Чтобы элементы с пройденными классами отображались, нужен рабочий компилятор. На текущий момент класса с ролью преподавателя и рабочим компилятором нет. Единственный выход - смотреть тесты в классе с ролью студента.
    # Просмотр деталей тестов - Чтобы элемент с деталями тестов отображался, нужен рабочий компилятор и роль преподавателя. На текущий момент класса с ролью преподавателя и рабочим компилятором нет.
    return True


# Переотправка решения студента
def resending_the_students_decision(browser):
    solutiondata = searchElementOfTable(browser)
    if not solutiondata:
        printExeption(f"Решения не найдены")
        return False
    try:
        attempt = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.ant-table-row.ant-table-row-level-0'))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Строка с попыткой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")


    # -------------- Переотправка решения --------------
    try:
        buttons_attempt = attempt.find_elements(By.CSS_SELECTOR, '.ant-btn.css-14h5sa0.ant-btn-text.ant-btn-lg.ant-btn-icon-only.IconButton_icon_button__7vyd9')
        if len(buttons_attempt) != 2:
            printExeption("Кнопка переотправки решения не найдена или кол-во кнопок не равно 2")
            return False
        buttons_attempt[1].click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка переотправки решения не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # -------------- Ожидание notification и перезагрузка страницы --------------
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-message')]//p[contains(text(), 'Решение успешно отправлено')]"))
        )

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
    # -------------- sleep для появления в очереди --------------
    sleep(9)
    # -------------- Перезагрузка страницы, Поиск прошлого решения и Проверка отсутствия вердиктов --------------

    # ----------- Поиск кнопки обновления -----------
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Обновить страницу']]"))
        ).click()

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка обновления не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # ----------- Повторный поиск и проверка отсутствия вердиктов -----------
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )  # Это нужно, чтобы дождаться загрузки таблицы
        row = browser.find_element(By.XPATH,
                                  f"//tr[.//span[contains(text(), '{solutiondata.user}')] and .//span[contains(text(), '{solutiondata.task_name}')] and .//span[contains(text(), '{solutiondata.language}')] and .//span[contains(text(), '{solutiondata.submission_date}')]]")

        printInfo(f"Прошлое решение найдено")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Обновлённое решение не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        # Извлекаем все ячейки из строки таблицы
        cells = row.find_elements(By.TAG_NAME, "td")
        verdicts = cells[4].text
        if verdicts == '-\n-':
            printInfo("У решения обновились вердикты (решение компилируется)")
        else:
            printExeption("У решения не обновились вердикты, либо задержка перед перезагрузкой страницы недостаточно большая")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Вердикты обновлённого решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    printSuccess(f"Переотправка решения студента работает")
    return True

# Выставление вердикта
def issuing_a_verdict(browser, verdict):
    solutiondata = searchElementOfTable(browser)
    if not solutiondata:
        printExeption(f"Решения не найдены")
        return False
    try:
        attempt = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.ant-table-row.ant-table-row-level-0'))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Строка с попыткой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # -------------- Выставление вердикта --------------
    try:
        buttons_attempt = attempt.find_elements(By.CSS_SELECTOR, '.ant-btn.css-14h5sa0.ant-btn-text.ant-btn-lg.ant-btn-icon-only.IconButton_icon_button__7vyd9')
        if len(buttons_attempt) != 2:
            printExeption("Кнопка деталей решения не найдена или кол-во кнопок не равно 2")
            return False
        buttons_attempt[0].click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка деталей решения не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        verdictList = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-flex') and (descendant::button[span[text()='Принято']] or descendant::button[span[text()='Отклонено']] or descendant::button[span[text()='Свяжитесь с преподавателем']] or descendant::button[span[text()='Списано']])]"))
        )
        verdictList.find_element(By.XPATH, f"//button[span[text()='{verdict}']]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption("Список решений не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # -------------- Ожидание notification и перезагрузка страницы --------------
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-message')]//p[contains(text(), 'Изменения успешно сохранены')]"))
        )

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'VerdictSection_current_verdict__K-ILx') and .//p[text()='{verdict}']]"))
        )
        printInfo(f"Вердикт '{verdict}' отображён в деталях решения")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка выхода не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

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

    # ----------- Поиск кнопки обновления -----------
    if not update_page(browser):
        printExeption("Ошибка обновления страницы")
        return False

    # ----------- Повторный поиск (убедиться, что задача пропала из постмодерации)) -----------
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )  # Это нужно, чтобы дождаться загрузки таблицы
        row = browser.find_element(By.XPATH,
                                   f"//tr[.//span[contains(text(), '{solutiondata.user}')] and .//span[contains(text(), '{solutiondata.task_name}')] and .//span[contains(text(), '{solutiondata.language}')] and .//span[contains(text(), '{solutiondata.submission_date}')]]")

        printExeption(f"Прошлое решение найдено")
        return False

    except (TimeoutException, NoSuchElementException):
        printInfo(f"Обновлённое решение не найдено")
        printSuccess(f"Выставление вердикта работает")
        return True
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

''' try:
        # Извлекаем все ячейки из строки таблицы
        cells = row.find_elements(By.TAG_NAME, "td")
        verdicts = cells[4].text.split('\n')
        verdictNew = verdictMaker(verdicts[1])
        if verdictNew == verdict:
            printInfo("У решения обновился вердикт")
        else:
            printExeption("У решения не обновился вердикт")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Вердикты обновлённого решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    printSuccess(f"Выставление вердикта работает")
    return True'''


# Выставление вердикта
def issuing_a_delete_verdict(browser):
    solutiondata = searchElementOfTable(browser)
    if not solutiondata:
        printExeption(f"Решения не найдены")
        return False
    try:
        attempt = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.ant-table-row.ant-table-row-level-0'))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Строка с попыткой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # -------------- Удаление вердикта --------------
    try:
        buttons_attempt = attempt.find_elements(By.CSS_SELECTOR, '.ant-btn.css-14h5sa0.ant-btn-text.ant-btn-lg.ant-btn-icon-only.IconButton_icon_button__7vyd9')
        if len(buttons_attempt) != 2:
            printExeption("Кнопка деталей решения не найдена или кол-во кнопок не равно 2")
            return False
        buttons_attempt[0].click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка деталей решения не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        verdict = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'VerdictSection_current_verdict__K-ILx')]"))
        )
        verdict.find_element(By.XPATH, "..//button[contains(@class, 'ButtonNonUi_button_non_ui__Mn9Zr')]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption("Нынешний вердикт не найден или уже отсутствует")
        # Выход
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc')]/span[text()='Закрыть']"))
            ).click()
        except (TimeoutException, NoSuchElementException):
            printExeption(f"Кнопка выхода не найдена")
            return False
        except Exception as e:
            printExeption(f"Тип ошибки: {type(e).__name__}")
            printExeption(f"Сообщение ошибки: {e}")
            return False
        return True
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # -------------- Ожидание notification и перезагрузка страницы --------------
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-message')]//p[contains(text(), 'Изменения успешно сохранены')]"))
        )

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'VerdictSection_current_verdict__K-ILx') and .//p[text()='Ожидание вердикта']]"))
        )
        printInfo(f"Вердикт 'Ожидание вердикта' отображён в деталях решения")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка выхода не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

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

    # ----------- Поиск кнопки обновления -----------
    if not update_page(browser):
        printExeption("Ошибка обновления страницы")
        return False

    # ----------- Повторный поиск и проверка смены вердикта -----------
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )  # Это нужно, чтобы дождаться загрузки таблицы
        row = browser.find_element(By.XPATH,
                                   f"//tr[.//span[contains(text(), '{solutiondata.user}')] and .//span[contains(text(), '{solutiondata.task_name}')] and .//span[contains(text(), '{solutiondata.language}')] and .//span[contains(text(), '{solutiondata.submission_date}')]]")

        printInfo(f"Прошлое решение найдено")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Обновлённое решение не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        # Извлекаем все ячейки из строки таблицы
        cells = row.find_elements(By.TAG_NAME, "td")
        verdicts = cells[4].text.split('\n')
        verdictNew = verdictMaker(verdicts[1])
        if verdictNew == "Ожидание вердикта":
            printInfo("У решения обновился вердикт")
        else:
            printExeption("У решения не обновился вердикт")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Вердикты обновлённого решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    printSuccess(f"Удаление вердикта работает")
    return True

# Просмотр тестов
def viewing_tests(browser):
    solutiondata = searchElementOfTable(browser)
    if not solutiondata:
        printExeption(f"Решения не найдены")
        return False
    try:
        attempt = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.ant-table-row.ant-table-row-level-0'))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Строка с попыткой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        buttons_attempt = attempt.find_elements(By.CSS_SELECTOR, '.ant-btn.css-14h5sa0.ant-btn-text.ant-btn-lg.ant-btn-icon-only.IconButton_icon_button__7vyd9')
        if len(buttons_attempt) != 2:
            printExeption("Кнопка деталей решения не найдена или кол-во кнопок не равно 2")
            return False
        buttons_attempt[0].click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка деталей решения не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    sleep(0.5)

# -------------- Проверка первого поля тестов --------------
    try:
        testField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'TestCasesOverview_test_cases_overview__9c6ww')]"))
        )

        acceptButtons = testField.find_elements(By.XPATH,".//button[contains(@class, 'TestCasesOverview_tooltip_success__8AUpi')]")
        errorButtons = testField.find_elements(By.XPATH,".//button[contains(@class, 'TestCasesOverview_tooltip_error__c0+yt')]")
        emptyButtons = testField.find_elements(By.XPATH,".//div[contains(@class, 'TestCasesOverview_test_case_item_stub__ogiAI')]")


        acceptButtons_count = len(acceptButtons)
        errorButtons_count = len(errorButtons)
        emptyButtons_count = len(emptyButtons)

        printInfo(f"(Первое поле) Количество пройденных тестов: {acceptButtons_count}")
        printInfo(f"(Первое поле) Количество проваленных тестов: {errorButtons_count}")
        printInfo(f"(Первое поле) Общее число квадратов: {emptyButtons_count + errorButtons_count + acceptButtons_count}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Область отображения тестов или сами тесты не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

# -------------- Проверка второго поля тестов --------------
    try:
        testButton = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//div[contains(@class, 'ant-collapse-header') and .//span[text()='Развернуть список тестов']]"))
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
                (By.XPATH,
                 "//span[text()='Развернуть список тестов']/ancestor::div[contains(@class, 'ant-collapse-item')]"))
        )
        sleep(0.5)
        allTests = table_container.find_elements(By.CSS_SELECTOR, ".ant-table-tbody tr")
        acceptedTests = table_container.find_elements(By.XPATH, "//tr[td/div/p[text()='Accepted']]")
        errorTests = table_container.find_elements(By.XPATH, "//tr[td/div[contains(@class, 'Verdict_verdict_red__zOVn1')]]")

        allTests_count = len(allTests)
        acceptedTests_count = len(acceptedTests)
        errorTests_count = len(errorTests)

        printInfo(f"(Второе поле) Количество пройденных тестов: {acceptedTests_count}")
        printInfo(f"(Второе поле) Количество проваленных тестов: {errorTests_count}")
        printInfo(f"(Второе поле) Общее число тестов: {allTests_count}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Меню тестов не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    printSuccess(f"Просмотр тестов решения функционирует")

# -------------- Проверка деталей тестов --------------
    mainFieldPostmoderation = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-drawer-body.Drawer_body__eSiGt"))
    )
    try:
        allButtons = acceptButtons + errorButtons
        if allButtons:
            random.choice(allButtons).click()
        else:
            printExeption(f"Кнопок тестов не существует")
            return False
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Меню тестов не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    sleep(0.5)

    # Поиск окна тестов
    # Всплывающие окна имеют одинаковые классы, поэтому нахожу сначала окно с деталями решения, потом все всплывающие окна (их получается 2)
    # и вытаскиваю из них окно с деталями решения, получая окно деталей теста
    try:
        allMainFieldPostmoderation = WebDriverWait(browser, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ant-drawer-body.Drawer_body__eSiGt"))
        )
        allMainFieldPostmoderation.remove(mainFieldPostmoderation)
        second_element = allMainFieldPostmoderation[0]

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Окно деталей тестов не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        taskName = second_element.find_element(By.CSS_SELECTOR, ".Title_title__Hbrke.Title_title_level_3__qwYsi").text
        printInfo(f"Заголовок деталей теста: {taskName}")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Заголовок деталей теста не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False



def searchElementOfTable(browser):
    try:
        elements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'ant-table-row') and .//a[contains(@class, 'LinkRouter_link_router__UL4Jy QueueTable_cell_link__ZnHtE')]]"))
        )
        # count = len(elements)
        # printInfo(f"Решения найдены: {count}")

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Решения не найдены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
    try:
        attempt = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.ant-table-row.ant-table-row-level-0'))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Строка с попыткой не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # -------------- Получение данных задачи --------------
    try:
        # Извлекаем все ячейки из строки таблицы
        cells = attempt.find_elements(By.TAG_NAME, "td")

        solutiondata = TaskData(
            user=cells[0].text,
            task_name=cells[1].text,
            language=cells[2].text,
            submission_date=cells[3].text,
            verdict=cells[4].text,
        )

        data = f"""
                user: {solutiondata.user}, 
                task_name: {solutiondata.task_name}, 
                language: {solutiondata.language}, 
                submission_date: {solutiondata.submission_date}, 
                verdict: {solutiondata.verdict.replace("\n", ", ")}"""

        printInfo(f"Данные решения найдены: {data}")
        return solutiondata
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Данные решения не найдены.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

def verdictMaker(verdict):
    if verdict == "Accepted":
        return "Принято"
    if verdict == "Rejected":
        return "Отклонено"
    if verdict == "Contact the teacher":
        return "Свяжитесь с преподавателем"
    if verdict == "Cheated":
        return "Списано"
    if verdict == "Pending":
        return "Ожидание вердикта"
    else:
        return verdict

def making_a_solution_for_tests(browser):
    if not making_a_solution_of_task(browser, Task(
        'Hello, world!',
        1), Solution(f'print("Hello, world!")', "Python3 (python 3.12)")):
        return False

    sleep(30) # Задержка для успешной компиляции и выставления вердикта

    if not update_page(browser):
        printExeption("Ошибка обновления страницы")
        return False

def update_page(browser):
    # ----------- Поиск кнопки обновления -----------
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'Button_button__4z3Rc') and span[text()='Обновить страницу']]"))
        ).click()
        printInfo(f"Данные обновлены")
        return True
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка обновления не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")