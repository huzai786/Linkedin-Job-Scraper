from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def check_elm_if_exist(driver, selector, method='xpath'):
    if method == 'xpath':
        Select_with = By.XPATH
    try:
        element = driver.find_element(Select_with,f'{selector}')
        return True
    
    except NoSuchElementException as e:
        return False





