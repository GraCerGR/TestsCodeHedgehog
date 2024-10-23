from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check(expectation, actual, place):
    if expectation == actual:
        print(f"Данные в {place} совпадают.")
    else:
        raise ValueError (f"Данные в {place} не совпадают. Ожидаемое: {expectation}, Фактическое: {actual}")