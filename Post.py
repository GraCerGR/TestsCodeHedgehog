from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from Exeptions import *


class Post:
    def __init__(self, name, description, author, datetime):
        self.name = name
        self.description = description
        self.author = author
        self.datetime = datetime

def posts(browser, post, role):
    printInfo(f"Начало теста вкладки posts")
    if not go_to_the_post_tab(browser):
        return False
    if role == "Teacher":
        newPost = creating_post(browser, post)
        if not newPost:
            return False
        if not search_by_post_name_and_check_data(browser, newPost, role):
            return False
        if not delete_post(browser, newPost):
            return False
        if search_by_post_name_and_check_data(browser, newPost, role):
            return True
    else:
        if not search_by_post_name_and_check_data(browser, post, role):
            return False
    return True
# Переход на вкладку "Посты"
def go_to_the_post_tab(browser):
    try:
        postButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[1]"))
        )
        postButton.click()
        return True
    except Exception:
        printExeption("Ошибка: Кнопка поста не была найдена или не стала доступной.")
        return False

# Поиск поста и проверка соотвтствия данных
def search_by_post_name_and_check_data(browser, post, role):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[1]/span/input"))
        )
        searchButton.send_keys(post.name)
#        postLinkName = WebDriverWait(browser, 10).until(
#            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'ButtonNonUi_button_non_ui__Mn9Zr') and h3[text()='{post.name}']]"))
#        )
        postLinkName = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//div[contains(@class, 'PostCard_post_card__uuefG') and contains(., '{post.name}') and contains(., '{post.author}, {post.datetime}')]"
            ))
        )
        printInfo(f"Пост '{post.name}' c данными '{post.author}, {post.datetime}' найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пост '{post.name}' c данными '{post.author}, {post.datetime}' не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    postLinkName.find_element(By.XPATH, f"//button[contains(@class, 'ButtonNonUi_button_non_ui__Mn9Zr') and h3[text()='{post.name}']]").click()

    # Проверка соответсвия во вкладке "Перейти к полному тексту"
    # Детальный просмотр поста
    try:
        nameInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[1]/h3"))
        ).get_attribute('innerHTML')
        check(post.name, nameInfo, 'Post.info.name')

        if role == "Teacher":
            descriptionInfo = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/div[3]/div/div[2]/div[3]/div"))
            ).get_attribute('innerHTML')
        else:
            descriptionInfo = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/div[3]/div/div[2]/div[2]/div"))
            ).get_attribute('innerHTML')
        check(post.description, descriptionInfo, 'Post.info.description')

        if role == "Teacher":
            authorInfo = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[4]"))
            )
        else:
            authorInfo = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[3]"))
            )
        author_label = authorInfo.find_element(By.XPATH, ".//p[text()='Автор поста']").text
        author_name = authorInfo.find_element(By.XPATH, f".//p[text()='{post.author}']").text
        check("Автор поста", author_label, 'Post.info.author')
        check(post.author, author_name, 'Post.info.author')

        if role == "Teacher":
            timeInfo = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/div[3]/div/div[2]/div[5]"))
            )
        else:
            timeInfo = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/div[3]/div/div[2]/div[4]"))
            )
        time_label = timeInfo.find_element(By.XPATH, ".//p[text()='Время публикации']").text
        time_value = timeInfo.find_element(By.XPATH, f".//p[text()='{post.datetime}']").text
        check("Время публикации", time_label, 'Post.info.datetime')
        check(post.datetime, time_value, 'Post.info.datetime')

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Проблема поиска данных поста")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

# Выход
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Закрыть']]"))
        ).click()
        printSuccess(f'Данные поста {post.name} верны')
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка выхода не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        closeButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input-clear-icon'))
        )
        closeButton.click()
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    return True

def creating_post(browser, post):
    try:
        userNameClass = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "UserSection_user_section__Y45e8"))
        )
        username_element = userNameClass.find_element(By.XPATH, ".//p[contains(@class, 'Paragraph_paragraph__vZceR')]")
        username = username_element.text
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Класс с именем пользователя не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[1]/div/button"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка создания поста не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    sleep(0.5)
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div/span/input"))
        ).send_keys(post.name)
        inputDescription = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div/div[2]/div[1]"))
        )

        browser.execute_script("arguments[0].innerHTML = arguments[1];", inputDescription, f'{post.description}')
        inputDescription.click() # Если просто вставлять скрипт в код, то пост создаётся без описания

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поля ввода не были заполнены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/form/button/span"))
        ).click()
        sleep(1) # Если не подождать, то запрос на создание поста не отправится и не откроется страница с информацией о новом посте
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Поля ввода не были заполнены")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        nameInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[1]/h3"))
        ).get_attribute('innerHTML')
        check(post.name, nameInfo, 'Post.info.name')

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Имя поста не было найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        descriptionInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[3]/div"))
        ).get_attribute('innerHTML')
        check(post.description, descriptionInfo, 'Post.info.description')
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Описание поста не было найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        authorInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[4]"))
        )
        author_label = authorInfo.find_element(By.XPATH, ".//p[text()='Автор поста']").text
        author_name = authorInfo.find_elements(By.CLASS_NAME, "Paragraph_paragraph__vZceR")[1].text
        check("Автор поста", author_label, 'Post.info.author')
        check(username, author_name, 'Post.info.author')
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Имя автора не было найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        timeInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[5]"))
        )
        time_label = timeInfo.find_element(By.XPATH, ".//p[text()='Время публикации']").text
        time_value = timeInfo.find_elements(By.CLASS_NAME, "Paragraph_paragraph__vZceR")[1].text
        check("Время публикации", time_label, 'Post.info.datetime')

    except (TimeoutException, NoSuchElementException):
        printExeption(f"Время публикации не было найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    # Выход
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Закрыть']]"))
        ).click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка выхода не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    post = Post(nameInfo, descriptionInfo, author_name, time_value)
    printSuccess(f"Пост '{post.name}' создан")
    sleep(1)
    return post

def delete_post(browser, post):
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[1]/span/input"))
        )
        searchButton.send_keys(post.name)
        #        postLinkName = WebDriverWait(browser, 10).until(
        #            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'ButtonNonUi_button_non_ui__Mn9Zr') and h3[text()='{post.name}']]"))
        #        )
        postLinkName = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//div[contains(@class, 'PostCard_post_card__uuefG') and contains(., '{post.name}') and contains(., '{post.author}, {post.datetime}')]"
            ))
        )
        printInfo(f"Пост '{post.name}' c данными '{post.author}, {post.datetime}' найден")
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Пост '{post.name}' c данными '{post.author}, {post.datetime}' не найден")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")
    try:
        postLinkName.find_element(By.XPATH,
                                  f"//button[contains(@class, 'PostCard_delete_button__OWery')]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка удаления поста '{post.name}' не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    sleep(0.5) # Задержка для открытия окна
    try:
        deletePostDiv = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//div[contains(@class, 'Modal_content__miRwP') and contains(., 'Удаление поста. Вы уверены?')]"
            ))
        )
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Модальное окно подтверждения удаления поста не найдено")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    try:
        deletePostDiv.find_element(By.XPATH,
                                  f"//button[contains(@class, 'Button_button_type_accent__NGYDO') and span[text()='{'Подтвердить'}']]").click()
    except (TimeoutException, NoSuchElementException):
        printExeption(f"Кнопка удаления поста '{post.name}' в модальном окне не найдена")
        return False
    except Exception as e:
        # Выводим тип ошибки и сообщение
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Сообщение ошибки: {e}")

    sleep(0.5) # Задержка для открытия окна
    try:
        closeButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input-clear-icon'))
        )
        closeButton.click()
    except Exception as e:
        printExeption(f"Тип ошибки: {type(e).__name__}")
        printExeption(f"Ошибка: {e}")
        return False
    printSuccess(f"Пост {post.name} c данными '{post.author}, {post.datetime}' успешно удалён")
    return True