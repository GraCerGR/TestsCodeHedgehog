from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Exeptions import *


class Post:
    def __init__(self, name, description, author, datetime):
        self.name = name
        self.description = description
        self.author = author
        self.datetime = datetime

def posts(browser, post):
    #Переход на вкладку "Посты"
    try:
        postButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[1]"))
        )
        postButton.click()
    except Exception:
        printExeption("Ошибка: Кнопка поста не была найдена или не стала доступной.")
        return

    # Поиск поста
    try:
        searchButton = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[1]/span/input"))
        )
        searchButton.send_keys(post.name)
        postLinkName = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'ButtonNonUi_button_non_ui__Mn9Zr') and h3[text()='{post.name}']]"))
        )
        printInfo(f"Пост {post.name} найден")
    except Exception as e:
        printExeption(f"Ошибка: Ошибка поиска поста. {e}")
        return

    # Проверка соответсвия получаемого результата с исходным
    # Просмотр списка постов в классе
    try:
        description = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/span").get_attribute('innerHTML')  # Получаем HTML-содержимое элемента
        datetime = browser.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[2]/div/div/div[3]/p").get_attribute('innerHTML')

        check(post.description, description, 'Post')
        check(f"{post.author}, {post.datetime}", datetime, 'Post')
    except Exception as e:
        printExeption(f"Ошибка: {e}")
        return
    postLinkName.click()

    # Проверка соответсвия во вкладке "Перейти к полному тексту"
    # Детальный просмотр поста
    try:
        nameInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[1]/h3"))
        ).get_attribute('innerHTML')
        check(post.name, nameInfo, 'Post.info.name')

        descriptionInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[2]/div"))
        ).get_attribute('innerHTML')
        check(post.description, descriptionInfo, 'Post.info.description')

        authorInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[3]"))
        )
        author_label = authorInfo.find_element(By.XPATH, ".//p[text()='Автор поста']").text
        author_name = authorInfo.find_element(By.XPATH, f".//p[text()='{post.author}']").text
        check("Автор поста", author_label, 'Post.info.author')
        check(post.author, author_name, 'Post.info.author')

        timeInfo = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[4]"))
        )
        time_label = timeInfo.find_element(By.XPATH, ".//p[text()='Время публикации']").text
        time_value = timeInfo.find_element(By.XPATH, f".//p[text()='{post.datetime}']").text
        check("Время публикации", time_label, 'Post.info.datetime')
        check(post.datetime, time_value, 'Post.info.datetime')

    except Exception as e:
        printExeption(f"Ошибка: {e}")
        return

    # Выход
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/div[1]/div/button"))
    ).click()

    return True