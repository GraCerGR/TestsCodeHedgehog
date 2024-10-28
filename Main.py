from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

from Class import *
from Login import *
from Post import *
from Tasks import *
from Queue import *

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        login_to_profile(self.browser,"https://dev.code.kupriyanov.space/", "ctrhtnysq.afqk@gmail.com", "Ro91684912")
        login_to_class(self.browser, 'test')

    def test_posts(self):
        result = posts(self.browser, Post('Тестовый пост',
                    '<p>Тест</p><p>Тест<br>Тесттесттесттесттесттесттест</p><p>РЕДАКТ</p>',
                    'test-admin',
                    '10.09.2024 17:02:38'))
        self.assertTrue(result, "Тест не пройден")

    def test_tasks(self):
        result = tasks(self.browser, Module('Арифметика',
                      0,
                      6,
                      0,
                      126973,
                      Section(
                          'Новая секция 3',
                          0,
                          1,
                          0,
                          123,
                              Task(
                                  'Найти первые N простых чисел',
                                  123))))
        self.assertTrue(result, "Тест не пройден")

    def test_queues(self):
        result = queues(self.browser, "Найти первые N простых чисел", "Student")
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()




#browser = webdriver.Chrome()

#login_to_profile(browser,"https://dev.code.kupriyanov.space/", "ctrhtnysq.afqk@gmail.com", "Ro91684912")

#login_to_class(browser, 'test')


'''posts(browser, Post('Тестовый пост',
                    '<p>Тест</p><p>Тест<br>Тесттесттесттесттесттесттест</p><p>РЕДАКТ</p>',
                    'test-admin',
                    '10.09.2024 17:02:38'))'''

'''tasks(browser, Module('Арифметика',
                      0,
                      6,
                      0,
                      126973,
                      Section(
                          'Новая секция 3',
                          0,
                          1,
                          0,
                          123,
                              Task(
                                  'Найти первые N простых чисел',
                                  123))))'''

# script_making_a_solution_of_task(browser, Task('Найти первые N простых чисел', 0))

#queues(browser, "Найти первые N простых чисел", "Student")

#input("Нажмите Enter, чтобы закрыть браузер...")