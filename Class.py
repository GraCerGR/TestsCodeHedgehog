from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_class(browser, classname):

    classButton = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//p[contains(@class, 'Paragraph_paragraph__vZceR') and contains(@class, 'Paragraph_paragraph_weight_bold__uSpls') and text()='{classname}']"))
    )
    classButton.click()