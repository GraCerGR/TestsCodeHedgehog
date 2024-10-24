from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Class import *
from Login import *
from Post import *
from Tasks import *

browser = webdriver.Chrome()

login_to_profile(browser,"https://dev.code.kupriyanov.space/", "ctrhtnysq.afqk@gmail.com", "Ro91684912")

login_to_class(browser, 'test')

'''posts(browser, Post('Тестовый пост',
                    '<p>Тест</p><p>Тест<br>Тесттесттесттесттесттесттест</p><p>РЕДАКТ</p>',
                    'test-admin',
                    '10.09.2024 17:02:38'))'''

tasks(browser, Module('Арифметика',
                      0,
                      6,
                      0,
                      126973,
                      Section(
                          'Новая секция 3',
                              Task(
                                  'Найти первые N простых чисел',
                                  '123'))))

input("Нажмите Enter, чтобы закрыть браузер...")