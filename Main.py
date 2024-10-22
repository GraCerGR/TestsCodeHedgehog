from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Class import login_to_class
from Login import login_to_profile

browser = webdriver.Chrome()
login_to_profile(browser,"https://dev.code.kupriyanov.space/", "ctrhtnysq.afqk@gmail.com", "Ro91684912")

login_to_class(browser, 'test')

input("Нажмите Enter, чтобы закрыть браузер...")