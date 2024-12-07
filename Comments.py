from email.header import Header
from time import sleep
from datetime import datetime

from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Exeptions import *
from settings import *
from Login import create_new_browser_window
from Class import *
from Tasks import go_to_the_tasks_tab
import time
import re
from selenium.webdriver import ActionChains

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class TaskInRating:
    def __init__(self, moduleName, sectionName, taskName):
        self.moduleName = moduleName
        self.sectionName = sectionName
        self.taskName = taskName

def comments(browser, user: User, task, commentPrivate, classname):
    printInfo(f"Начало теста комментариев")
    if not go_to_the_history_tab(browser, user, task):
        return False
    print()

    newComment = comment_maker(browser, commentPrivate)
    if not newComment:
        return False
    print()

   # browser.quit()

    printInfo(
        f"ВНИМАНИЕ! Для выполнения данного теста необходимо указать USERNAME и PASSWORD пользователя '{user.name}'")
    if not test_comments_in_new_browser_window(task, newComment, commentPrivate, classname):
        return False
    print()

    newComment = rewrite_comment(browser, newComment)
    if not newComment:
        return False
    if not test_comments_in_new_browser_window(task, newComment, commentPrivate, classname):
        return False
    print()

    if not delete_comment(browser, newComment):
        return False
    if not test_comments_in_new_browser_window(task, newComment, "delete", classname):
        return False
    print()

    return True

def test_comments_in_new_browser_window(task, comment, commentPrivate, classname):

    browser = create_new_browser_window(SITELINK2, USERNAME_RECEIVED_COMMENT, PASSWORD_RECEIVED_COMMENT, classname)
    if not browser:
        return False

    if not go_to_the_tasks_tab(browser):
        return False

    if not search_by_task_name(browser, task):
        return False

    if not check_comments(browser, task, comment, commentPrivate):
        return False

    browser.quit()
    return True


# Переход в историю решений
def go_to_the_history_tab(browser, user, task):
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[5]"))
        ).click()
    except Exception:
        printExeption(f"Ошибка: Кнопка Пользователи не была найдена или не стала доступной.")
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
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'ant-flex') and contains(., 'Пользователь:') and .//a[contains(text(), '{user.name}')]]"))
        )
        printInfo(f"Страница результатов пользователя '{user.name}' открыта")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поля информации о результатах (заголовок, имя пользователя) не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        module = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class, 'ModuleStructure_module_structure__Dd7NK')]"
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
        section = module.find_element(By.XPATH,
                                      f"//div[contains(@class, 'SectionStructure_section_structure__oiisl') and .//p[text()='{task.sectionName}']]")
        printInfo(f"Секция '{task.sectionName}' найдена")

        scrolling_to_element(browser, section)
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
            EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'ant-table-row') and contains(@class, 'ant-table-row-level-0') and td[2]//p[text()='{task.taskName}']]"))
        )
        printInfo(f"Задача '{task.taskName}' найдена")

        scrolling_to_element(browser, taskElement)
        taskElement.click()

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Задача '{task.taskName}' не найдена в секции '{task.sectionName}' модуля '{task.moduleName}'")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH,
                                            f"//h3[contains(text(), 'История попыток') and .//a[contains(text(), '{task.taskName}')]]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Заголовок страницы истории решений не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка перехода в историю решений задачи. {e}")
        return False

    printSuccess(f"Переход на страницу с историей решений задачи выполнен")
    return True

# Создание комментария
def comment_maker(browser, protection):
    try:
        userNameClass = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "UserSection_user_section__Y45e8"))
        )
        username_element = userNameClass.find_element(By.XPATH, ".//p[contains(@class, 'Paragraph_paragraph__vZceR')]")
        username = username_element.text

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Имя пользователя сессии не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    try:
        commentProtectionSelector = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Segmented_segmented__VNG0y')]"))
        )
        commentProtections = commentProtectionSelector.find_elements(By.TAG_NAME, 'label')
        scrolling_to_element(browser, commentProtectionSelector)
        commentText = ""
        if (protection == "public"):
            commentProtections[0].click()
            commentText = f"Публичный комментарий от {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} пользователя {username}"
        elif (protection == "private"):
            commentProtections[1].click()
            commentText = f"Приватный комментарий от {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} пользователя {username}"
        else:
            printExeption("Неверный аргумент приватности комментария")
            return False

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Селектор приватности комментариев не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        comment = browser.find_elements(By.CSS_SELECTOR, '.jodit-wysiwyg[contenteditable="true"]')
        comment = comment[-1]
        scrolling_to_element(browser, comment)
        comment.send_keys(f"{commentText}")
        sleep(1)
        sendButton = browser.find_element(By.CSS_SELECTOR, '.CommentAddForm_send_button__E21VQ')
        scrolling_to_element(browser, sendButton)
        sendButton.click()
        notification = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Успешно создано')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Одна из областей создания комментария не найдена (ввод комментария, кнопка, уведомление)")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        commentNew = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and contains(., '{username}') and .//p[contains(text(), '{commentText}')]]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Созданный комментарий не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    printSuccess(f"{commentText.split(" комментарий")[0]} комментарий успешно создан")
    return commentText

def scrolling_to_element(browser, element):
    window_height = browser.execute_script("return window.innerHeight;")
    window_width = browser.execute_script("return window.innerWidth;")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    element_rect = browser.execute_script("return arguments[0].getBoundingClientRect();", element)
    browser.execute_script("window.scrollBy(0, -arguments[0] / 2);", window_height)
    browser.execute_script("window.scrollBy(-arguments[0], 0);", element_rect['left'] + (element_rect['width'] / 2) - (window_width / 2))
    sleep(0.5)

def search_by_task_name(browser, task: TaskInRating):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/form/div/div[1]/div/div[2]/div[1]/span/input"))
        )

        for char in task.taskName:
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
                           f".//p[text()='{task.sectionName}'] and "
                           f".//following::p[text()='{task.taskName}']]"))
        )
        printInfo(f"Задача найдена")
        return True

    except (TimeoutException, NoSuchElementException):
        printExeption(
            f"Ошибка: Секция '{task.sectionName}' с задачей '{task.taskName}' не была найдена или не стала доступной.")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

def check_comments(browser, task: TaskInRating, comment, private):
    try:
        taskElement = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'ant-table-row') and contains(@class, 'ant-table-row-level-0') and td[2]//p[text()='{task.taskName}']]"))
        )
        printInfo(f"Задача '{task.taskName}' найдена")

        cells = taskElement.find_elements(By.TAG_NAME, "td")

        lastCommentCell = cells[5].text

        if private == "private":
            if lastCommentCell == comment:
                printExeption(f"Приватный комментарий отображается в последнем комментарии задачи")
                return False
            else:
                printInfo(f"Приватный комментарий не отобразился в последнем комментарии задачи")
                printInfo(f"Отображаемый комментарий: {lastCommentCell}")
        elif private == "public":
            if lastCommentCell == comment:
                printInfo(f"Публичный комментарий отобразился в последнем комментарии задачи")
                printInfo(f"Отображаемый комментарий: {lastCommentCell}")
            else:
                printExeption(f"Публичный комментарий не отображается в последнем комментарии задачи")
                return False
        elif private == "delete":
            if lastCommentCell == comment:
                printExeption(f"Удалённый комментарий отображается в последнем комментарии задачи")
                return False
            else:
                printInfo(f"Удалённый комментарий не отобразился в последнем комментарии задачи")
                printInfo(f"Отображаемый комментарий: {lastCommentCell}")
        else:
            printExeption("Параметр private комментария задан неккоректно")
            return False

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Задача '{task.taskName}' или её комментарий не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: Ошибка поиска задачи. {e}")
        return False

    try:
        scrolling_to_element(browser, taskElement)
        taskElement.click()
        taskTitle = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h2[text()='{task.taskName}']"))
        )
        printInfo(f"Переход на страницу деталей выполнен")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Элемент '{task.taskName}' не найден.")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        linkToLastSolution = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'TaskClassVerdicts_solution_link__7OKmA') and //p[text()='Перейти к моему последнему решению']]"))
        )
        linkToLastSolution.click()
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h2[contains(text(), 'Постмодерация') and .//a[text()='{task.taskName}']]"))
        )
        printInfo(f"Переход в постмодерацию задачи '{task.taskName}' выполнен")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Заголовок не найден, или название задачи не соответствует заголовку")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False

    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and .//p[contains(text(), '{comment}')]]"))
        )
        if private == "public":
            printInfo(f"Публичный комментарий найден")
        elif private == "private":
            printInfo(f"Приватный комментарий найден")
            return False
        elif private == "delete":
            printInfo(f"Удалённый комментарий найден")
            return False
    except (TimeoutException, NoSuchElementException):
        if private == "private":
            printInfo(f"Приватный комментарий не найден")
        elif private == "public":
            printExeption(f"Публичный комментарий не найден")
            return False
        elif private == "delete":
            printInfo(f"Удалённый комментарий не найден")
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
        return False
    printSuccess(f"Отображение {"приватных" if private == "private" else "публичных" if private == "public" else "удалённых" if private == "delete" else "неизвестных"} комментариев функционирует исправно")
    return True

def delete_comment(browser, newComment):
    try:
        commentNew = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and .//p[contains(text(), '{newComment}')]]"))
        )
        printInfo("Комментарий найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Созданный комментарий не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        commentButtons = WebDriverWait(commentNew, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ButtonNonUi_button_non_ui__Mn9Zr"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопки комментария не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    try:
        scrolling_to_element(browser, commentButtons[1])
        commentButtons[1].click()
        modalWindowToDeleteComment = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal-content.Modal_content__miRwP"))
        )
        printInfo(f"Модальное окно открыто")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно удаления комментария не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        submitButton = WebDriverWait(modalWindowToDeleteComment, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-btn.css-14h5sa0.ant-btn-default.Button_button__4z3Rc.Button_button_type_accent__NGYDO"))
        )
        submitButton.click()
        notification = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Успешно удалено')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно удаления комментария не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and .//p[contains(text(), '{newComment}')]]"))
        )
    except (TimeoutException, NoSuchElementException):
        printSuccess(f"Комментарий успешно удалён")
        return True
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    printExeption(f"Комментарий не удалён")
    return False

def rewrite_comment(browser, newComment):
    try:
        commentNew = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and .//p[contains(text(), '{newComment}')]]"))
        )
        printInfo("Комментарий найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Созданный комментарий не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        commentButtons = WebDriverWait(commentNew, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ButtonNonUi_button_non_ui__Mn9Zr"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопки комментария не найдены")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    try:
        scrolling_to_element(browser, commentButtons[1])
        commentButtons[0].click()
        sleep(1)
        comment = browser.find_element(By.XPATH, "//div[contains(@class, 'jodit-wysiwyg') and @contenteditable='true']"
                                                 f"//p[contains(text(), '{newComment}')]")
        scrolling_to_element(browser, comment)
        comment.clear()
        updatedComment = re.sub(r'(комментарий от).*?(пользователя)',
                                r'\1 ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + r' \2', newComment)
        comment.send_keys(updatedComment)
        printInfo(updatedComment)

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Редактирование комментария не выполнено. Элемент не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка редактирования комментария: {e}")
        return False

    try:
        commentBody = comment.find_elements(By.XPATH, "..//..//..//..")
        sendButton = commentBody[0].find_element(By.CSS_SELECTOR, ".ant-btn.css-14h5sa0.ant-btn-default.Button_button__4z3Rc.Button_button_type_accent__NGYDO")
        scrolling_to_element(browser, sendButton)
        sendButton.click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка отправки комментария не найдена")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка редактирования комментария: {e}")
        return False

    try:
        notification = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-notification-notice-wrapper')]//p[contains(text(), 'Изменения успешно сохранены')]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Уведомление об изменении комментария не найдено")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    try:
        commentNew = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'Comment_comment__baGMa') and .//p[contains(text(), '{updatedComment}')]]"))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Изменённый комментарий не найден")
        return False
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False

    printSuccess(f"Комментарий успешно изменён")
    return updatedComment