from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Login import login_to_profile

login_to_profile("https://dev.code.kupriyanov.space/", "не скажу", "пароль")
input("Нажмите Enter, чтобы закрыть браузер...")