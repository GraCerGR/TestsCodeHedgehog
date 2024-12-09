from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from Exeptions import *
from Main import create_new_browser_window
from Users import go_to_the_users_tab, search_by_user_name_without_cleaning_searchfield
from InvitationLinks import link_creating, open_links
from Tasks import Section, go_to_the_tasks_tab
from time import sleep
from settings import *

def adding_and_deleting_from_class(browser, classname, taskInSection):
    printInfo(f"Начало теста добавления/удаления из гугл класса")
    if not go_to_the_users_tab(browser):
        return False
    print()

    if not manually_adding_users(browser, EMAIL_INVENTED_PERSON):
        return False
    print()
    if not adding_and_deleting_from_class_in_new_browser_window(SITELINK, classname, taskInSection):
        return False
    printSuccess("Пользователь был успешно добавлен в класс вручную")
    print()

    browser.refresh() # Для обновления списка пользователей в классе после добавления нового пользователя

    if not deleting_user_from_class(browser, USERNAME_INVENTED_PERSON, ROLE_INVENTED_PERSON):
        return False
    print()
    if adding_and_deleting_from_class_in_new_browser_window(SITELINK, classname):
        return False
    printSuccess("Пользователь был успешно удалён из класса")
    print()


    if not open_links(browser):
        return False
    link = link_creating(browser, ROLE_INVENTED_PERSON, True)
    if not link:
        return False
    print()
    if not adding_and_deleting_from_class_in_new_browser_window(link, classname, taskInSection):
        return False
    printSuccess("Пользователь был успешно добавлен в класс по ссылке")

    return True



def adding_and_deleting_from_class_in_new_browser_window(sitelink, classname, taskInSection: Section = None):

    browser = create_new_browser_window(sitelink, EMAIL_INVENTED_PERSON, PASSWORD_INVENTED_PERSON, classname, False)
    if not browser:
        return False
    print()

    if Section:
        if not return_in_class_with_progress(browser, taskInSection):
            return False

    browser.quit()
    return True

def return_in_class_with_progress(browser, section):
    if not go_to_the_tasks_tab(browser):
        return False
    if not viewing_task_details(browser, section):
        browser.quit()
        return False
    printSuccess("Возвращение в тот же класс с сохранением прогресса работает")
    return True


# Ручное добавление пользователей
def manually_adding_users(browser, email):
    try:
        addingUserButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'Button_button__4z3Rc') and .//span[text()='Добавить пользователя']]"))
        )
        addingUserButton.click()
        sleep(1)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка добавления пользователей не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки. {e}")
        return False

    try:
        drawerWindow = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-drawer-body.Drawer_body__eSiGt"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        sleep(1)
        emailInput = WebDriverWait(drawerWindow, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
        )
        emailInput.send_keys(email)
        sleep(2)
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поле ввода имени не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки. {e}")
        return False

    try:
        WebDriverWait(drawerWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//tr[contains(@class, 'ant-table-row') and .//td[(text()='{email}')]]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пользователь с почтой '{email}' не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска пользователя. {e}")
        return False

    try:
        WebDriverWait(drawerWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button_type_accent__NGYDO') and .//span[text()='Подтвердить']]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка приглашения не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка создания приглашения: {e}")
        return False

    try:
        notification = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Изменения успешно сохранены')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление создания приглашения не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка поиска уведомления: {e}")
        return False

    printSuccess("Пользователь успешно приглашён (со стороны приглашающего)")
    return True

# Удаление пользователя из класса
def deleting_user_from_class(browser, username, roleWasDeleting):
    if not search_by_user_name_without_cleaning_searchfield(browser, username, roleWasDeleting):
        return False

    try:
        cellWithDeleteButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'IconButton_icon_button_danger__kgOt7')]"))
        ).click()
        printInfo(f"Пользователь найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка удаления пользователя не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска кнопки удаления. {e}")
        return False

    try:
        sleep(1)
        modalWindow = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal-content.Modal_content__miRwP"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно не было найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        WebDriverWait(modalWindow, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class, 'Button_button_type_accent__NGYDO') and .//span[text()='Подтвердить']]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка подтверждения удаления не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка удаления пользователя: {e}")
        return False

    try:
        notification = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Успешно удалено')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление удаления пользователя не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка поиска уведомления: {e}")
        return False

    printSuccess("Пользователь успешно удалён (со стороны приглашающего)")
    return True


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
                printSuccess("Предыдущие решения задачи существуют")
                return True

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Задача ранее не решалась. Нет вердиктов")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False



