import logging
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *
import unittest

from Class import *
from Login import *
from Post import *
from Tasks import *
from Queue import *
from Users import *
from Rating import *

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        login_to_profile(self.browser,SITELINK, USERNAME, PASSWORD)
        login_to_class(self.browser, 'test')

    def test_posts(self):
        result = posts(self.browser, Post('Тестовый пост',
                    '<p>Тест</p><p>Тест<br>Тесттесттесттесттесттесттест</p><p>РЕДАКТ</p>',
                    'test-admin',
                    '10.09.2024 17:02:38'), "Student")
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

    def test_tasks_filters(self):
        filter1 = set_t_filter(self.browser, ['Compilation Error'], Task('Найти первые N простых чисел', 123))
        filter2 = set_t_filter(self.browser, ['Отклонено'], Task('Найти первые N простых чисел', 123))
        filter3 = set_t_filter(self.browser, ['Ожидание вердикта'], Task('2131', 94151))
        filter4 = set_t_filter(self.browser, ['Отклонено', 'Compilation Error'], Task('Найти первые N простых чисел', 123))
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def test_queues(self):
        result = queues(self.browser, "Найти первые N простых чисел", "Student")
        self.assertTrue(result, "Тест не пройден")

    def test_queue_filters(self):
        filter1 = set_q_filter(self.browser, ['Compilation Error'], 'Найти первые N простых чисел')
        filter2 = set_q_filter(self.browser, ['C++'], 'Найти первые N простых чисел')
        filter3 = set_q_filter(self.browser, ['Check Failed'], '2131')
        filter4 = set_q_filter(self.browser, ['Арифметика', '42135'], '2131')
        self.assertTrue(filter1 and filter2 and filter3, "Тест не пройден")

    def test_users(self):
        result = users(self.browser, "Срибный Григорий Романович", "Студенты")
        self.assertTrue(result, "Тест не пройден")

    def test_rating(self):
        result = rating(self.browser,  "Student","Арифметика", "test-admin")
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()


class TestTeacher(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        login_to_profile(self.browser,SITELINK, USERNAME, PASSWORD)
        login_to_class(self.browser, 'Test machine learning class')

    def test_rating(self):
        result = rating(self.browser,  "Teacher","Арифметика", "Трофимова Екатерина Дмитриевна")
        self.assertTrue(result, "Тест не пройден")

    def test_post(self):
        result = posts(self.browser, Post('Тестовый пост',
                    '<p>Тест</p><p>Тест<br>Тесттесттесттесттесттесттест</p><p>РЕДАКТ</p>',
                    'test-admin',
                    '10.09.2024 17:02:38'), "Teacher")
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()
#browser = webdriver.Chrome()

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