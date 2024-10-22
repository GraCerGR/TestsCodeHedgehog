from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Post:
    def __init__(self, name, description, author, datetime):
        self.name = name
        self.description = description
        self.author = author
        self.datetime = datetime

def posts(browser, post):

    postButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button[1]"))
    )
    postButton.click()

    searchButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[1]/span/input"))
    )
    searchButton.send_keys(post.name)
    postLinkName = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'ButtonNonUi_button_non_ui__Mn9Zr') and h3[text()='{post.name}']]"))
    )
    #Здесь будет проверка соответсвия получаемого результата с исходным
    postLinkName.click()

