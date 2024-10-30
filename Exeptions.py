from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def check(expectation, actual, place):
    if expectation == actual:
        print(f"Данные в {place} совпадают.")
    else:
        raise ValueError (f"Данные в {place} не совпадают. Ожидаемое: {expectation}, Фактическое: {actual}")

def printExeption(text: str):
    print(f"{"\033[31m"}{text}{"\033[0m"}")