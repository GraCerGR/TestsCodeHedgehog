import logging
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Postmoderation import postmoderation
from settings import *
import unittest

from Class import *
from Login import *
from Post import *
from Tasks import *
from Queue import *
from Users import *
from Rating import *
from Postmoderation import *

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
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def test_users(self):
        result = users(self.browser, "Срибный Григорий Романович", "Студенты", "Student")
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

    def test_tasks(self):
        result = tasks(self.browser, Module('Арифметика',
                      0,
                      5,
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
        filter1 = set_t_filter(self.browser, ['Check Failed'], Task('Найти первые N простых чисел', 123))
        filter2 = set_t_filter(self.browser, ['Отклонено'], Task('Найти первые N простых чисел', 123))
        filter4 = set_t_filter(self.browser, ['Отклонено', 'Check Failed'], Task('Найти первые N простых чисел', 123))
        self.assertTrue(filter1 and filter2 and filter4, "Тест не пройден")

    def test_queues(self):
        result = queues(self.browser, "Найти первые N простых чисел", "Teacher")
        self.assertTrue(result, "Тест не пройден")

    def test_queue_filters(self):
        filter1 = set_q_filter(self.browser, ['Check Failed'], 'Найти первые N простых чисел')
        filter2 = set_q_filter(self.browser, ['C++'], '2131')
        filter3 = set_q_filter(self.browser, ['Compilation Error'], 'Найти первые N простых чисел')
        filter4 = set_q_filter(self.browser, ['Арифметика', '42135'], '2131')
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def test_users(self):
        result = users(self.browser, "test-admin", "Преподаватели", "Teacher")
        self.assertTrue(result, "Тест не пройден")

    def test_postmoderation_management(self):
        result = postmoderation_management(self.browser, "Принято")
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()


class TestStudent_On_Main_Site(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        login_to_profile(self.browser,SITELINK2, USERNAME, PASSWORD)
        login_to_class(self.browser, 'Программирование(Тестовый класс для Фич)')

    def test_postmoderation(self):
        result = postmoderation(self.browser, "Нахождение элемента в массиве, который больше своих соседей", "Student")
        self.assertTrue(result, "Тест не пройден")
# Задача "Из списка рёбер в список смежности" не находится по полному названию, так как содержит символы &nbsp; Использовать \u00a0
    def test_postmoderation_filters(self):
        filter1 = set_p_filter(self.browser, ['Поиск и сортировка (Модуль 2)', 'Алгоритмы поиска'], 'Нахождение элемента в массиве, который больше своих соседей')
        filter2 = set_p_filter(self.browser, ['Графы (Модуль 4)', 'Графы основа'], 'Из списка\u00a0рёбер\u00a0в список смежности\u00a0')
        filter3 = set_p_filter(self.browser, ['C# (mono 6.12)'], 'Из списка\u00a0рёбер\u00a0в список смежности\u00a0')
        filter4 = set_p_filter(self.browser, ['Python3 (python 3.12)'], 'Нахождение элемента в массиве, который больше своих соседей')
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()
