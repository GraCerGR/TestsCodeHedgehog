from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import inspect

def get_caller_function_name():
    # Получаем информацию о стеке вызовов
    stack = inspect.stack()
    # stack[2] - это вызвавшая функцию текущей функции
    caller = stack[2]
    return caller.function

def check(expectation, actual, place):
    if expectation == actual:
        print(f"[{get_caller_function_name()}] Данные в {place} совпадают.")
    else:
        raise ValueError (f"{"\033[31m"}[{get_caller_function_name()}] Данные в {place} не совпадают. Ожидаемое: {expectation}, Фактическое: {actual}{"\033[0m"}")

def printExeption(text: str):
    print(f"{"\033[31m"}[{get_caller_function_name()}] {text}{"\033[0m"}")

def printInfo(text: str):
    print(f"[{get_caller_function_name()}] {text}")

def printSuccess(text: str):
    print(f"{"\033[32m"}[{get_caller_function_name()}] {text}{"\033[0m"}")