import logging

from click import option
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from InvitationLinks import links
from Postmoderation import postmoderation
from settings import *
import unittest

from Login import *
from Post import *
from Tasks import *
from Queue import *
from Users import *
from Rating import *
from Postmoderation import *
from PostmoderationManagement import *
from Result import *
from Comments import *
from AddingToClassAndDeleting import *

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.browser = create_new_browser_window(SITELINK, USERNAME, PASSWORD, "test")

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
        print()
        self.browser.refresh()
        filter2 = set_t_filter(self.browser, ['Отклонено'], Task('Найти первые N простых чисел', 123))
        print()
        self.browser.refresh()
        filter3 = set_t_filter(self.browser, ['Ожидание вердикта'], Task('2131', 94151))
        print()
        self.browser.refresh()
        filter4 = set_t_filter(self.browser, ['Отклонено', 'Compilation Error'], Task('Найти первые N простых чисел', 123))
        print()
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def test_queues(self):
        result = queues(self.browser, "Найти первые N простых чисел", "Student")
        self.assertTrue(result, "Тест не пройден")

    def test_queue_filters(self):
        filter1 = set_q_filter(self.browser, ['Compilation Error'], 'Найти первые N простых чисел')
        print()
        self.browser.refresh()
        filter2 = set_q_filter(self.browser, ['C++'], 'Найти первые N простых чисел')
        print()
        self.browser.refresh()
        filter3 = set_q_filter(self.browser, ['Check Failed'], '2131')
        print()
        self.browser.refresh()
        filter4 = set_q_filter(self.browser, ['Арифметика', '42135'], '2131')
        print()
        self.browser.refresh()
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def test_users(self):
        result = users(self.browser, "Срибный Григорий Романович", "Student", "Student")
        self.assertTrue(result, "Тест не пройден")

    def test_rating(self):
        result = rating(self.browser,  "Student","Арифметика", "test-admin")
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()


class TestTeacher(unittest.TestCase):

    def setUp(self):
        self.browser = create_new_browser_window(SITELINK, USERNAME, PASSWORD, "Test machine learning class")

    def test_rating(self):
        result = rating(self.browser,  "Teacher","Арифметика", "Трофимова Екатерина Дмитриевна")
        self.assertTrue(result, "Тест не пройден")

    def test_post(self):
        result = posts(self.browser, Post('Тестовый пост',
                    '<p>Тест</p><p>Тест<br>Тесттесттесттесттесттесттест</p><p>РЕДАКТ</p>',
                    'test-admin',
                    '10.09.2024 17:02:38'), "Teacher")
        self.assertTrue(result, "Тест не пройден")

    def test_create_task(self):
        result = making_a_solution_of_task(self.browser, Task(
                                  'Найти первые N простых чисел',
                                  123), Solution(f"a, b = map(int, input().split())\nresult = a + b\nprint(result)", "C++"))
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
        print()
        self.browser.refresh()
        filter2 = set_t_filter(self.browser, ['Отклонено'], Task('Найти первые N простых чисел', 123))
        print()
        self.browser.refresh()
        filter3 = set_t_filter(self.browser, ['Отклонено', 'Check Failed'], Task('Найти первые N простых чисел', 123))
        print()
        self.browser.refresh()
        self.assertTrue(filter1 and filter2 and filter3, "Тест не пройден")

    def test_queues(self):
        result = queues(self.browser, "Найти первые N простых чисел", "Teacher")
        self.assertTrue(result, "Тест не пройден")

    def test_queue_filters(self):
        filter1 = set_q_filter(self.browser, ['Check Failed'], 'Найти первые N простых чисел')
        print()
        self.browser.refresh()
        filter2 = set_q_filter(self.browser, ['C++'], '2131')
        print()
        self.browser.refresh()
        filter3 = set_q_filter(self.browser, ['Compilation Error'], 'Найти первые N простых чисел')
        print()
        self.browser.refresh()
        filter4 = set_q_filter(self.browser, ['Арифметика', '42135'], '2131')
        print()
        self.browser.refresh()
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def test_users(self):
        result = users(self.browser, "test-admin", "Teacher", "Teacher")
        self.assertTrue(result, "Тест не пройден")

    def test_invite_links(self):
        result = links(self.browser)
        self.assertTrue(result, "Тест не пройден")

    def test_adding_and_deleting_from_class(self):
        result = adding_and_deleting_from_class(self.browser, 'Test machine learning class', Section(
                                  'Новая секция 3',
                                  0,
                                  1,
                                  0,
                                  123,
                                      Task(
                                          'Найти первые N простых чисел',
                                          123)))
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()


class TestStudent_On_Main_Site(unittest.TestCase):

    def setUp(self):
        self.browser = create_new_browser_window(SITELINK2, USERNAME, PASSWORD, "Программирование(Тестовый класс для Фич)")

    def test_postmoderation(self):
        result = postmoderation(self.browser, "Нахождение элемента в массиве, который больше своих соседей", "Student")
        self.assertTrue(result, "Тест не пройден")
# Задача "Из списка рёбер в список смежности" не находится по полному названию, так как содержит символы &nbsp; Использовать \u00a0
    def test_postmoderation_filters(self):
        filter1 = set_p_filter(self.browser, ['Поиск и сортировка (Модуль 2)', 'Алгоритмы поиска'], 'Нахождение элемента в массиве, который больше своих соседей')
        print()
        self.browser.refresh()
        filter2 = set_p_filter(self.browser, ['Графы (Модуль 4)', 'Графы основа'], 'Из списка\u00a0рёбер\u00a0в список смежности\u00a0')
        print()
        self.browser.refresh()
        filter3 = set_p_filter(self.browser, ['C# (mono 6.12)'], 'Из списка\u00a0рёбер\u00a0в список смежности\u00a0')
        print()
        self.browser.refresh()
        filter4 = set_p_filter(self.browser, ['Python3 (python 3.12)'], 'Нахождение элемента в массиве, который больше своих соседей')
        print()
        self.browser.refresh()
        self.assertTrue(filter1 and filter2 and filter3 and filter4, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()


class TestTeacher_On_Main_Site(unittest.TestCase):

    def setUp(self):
        self.browser = create_new_browser_window(SITELINK2, USERNAME2, PASSWORD, "Программирование(Тестовый класс для Фич)", False)

    def test_postmoderation_management(self):
        result = postmoderation_management(self.browser, "Принято")
        self.assertTrue(result, "Тест не пройден")

    def test_result(self):
        res = result(self.browser, User("Срибный Григорий Романович", "Студенты"),
                     TaskInRating('Основы программирования (Модуль 1) (модуль 1)', 'Присваивание и арифметика', 'Hello, world!'))
        self.assertTrue(res, "Тест не пройден")

    def test_private_comments(self):
        result = comments(self.browser, User("Срибный Григорий Романович", "Студенты"),
                     TaskInRating('Основы программирования (Модуль 1) (модуль 1)', 'Присваивание и арифметика', 'Hello, world!'),
                       "private", "Программирование(Тестовый класс для Фич)")
        self.assertTrue(result, "Тест не пройден")

    def test_public_comments(self):
        result = comments(self.browser, User("Срибный Григорий Романович", "Студенты"),
                     TaskInRating('Основы программирования (Модуль 1) (модуль 1)', 'Присваивание и арифметика', 'Hello, world!'),
                       "public", "Программирование(Тестовый класс для Фич)")
        self.assertTrue(result, "Тест не пройден")

    def tearDown(self):
        self.browser.quit()