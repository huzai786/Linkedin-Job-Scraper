import os, re, time, sys
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from .helper_functions import check_elm_if_exist
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from . import xpaths


UA = UserAgent()


def chrome_options(silence=False):
    options = webdriver.ChromeOptions()

    if silence:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

    options.add_argument(f"user-agent={UA.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("-incognito")
    options.add_argument("--disk-cache-")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    return options


def get_input():
    """Gets search query and location"""
    print("Enter job search query: ")
    job_query = input("> ")
    print("Enter Location: ")
    location = input("> ")
    return job_query, location



def scroll_down(driver):
    """Scroll down till the end of the page!"""
    try:
        page_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(1.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == page_height:
                check_elem = check_elm_if_exist(driver, xpaths.FIND_MORE_JOBS_XPATH)
                if check_elem:
                    see_more_jobs_button = driver.find_element(
                        By.XPATH, xpaths.FIND_MORE_JOBS_XPATH
                    )
                    if see_more_jobs_button.is_displayed():
                        time.sleep(2)
                        see_more_jobs_button.click()
                        time.sleep(1)
                        new_height = driver.execute_script(
                            "return document.body.scrollHeight"
                        )
                    else:
                        break
                else:
                    break
            page_height = new_height
            

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("error: ", e)
        print(
            "error type:",
            exc_type.__qualname__,
            "file:",
            fname,
            "Line no:",
            exc_tb.tb_lineno,
        )


def dump_ids_into_file(ids, file_name):
    file_name = re.sub("\s", "_", file_name)
    file_path = os.path.join(os.getcwd(), "job_ids", f"{file_name}_jobs.txt")

    if os.path.exists(file_path):
        with open(file_path, "a+") as f:
            id_lists = f.read().splitlines()
            new_items = []
            for i in ids:
                if i not in id_lists:
                    new_items.append(i + '\n')
            f.writelines(new_items)
            print(f"{file_name} updated!")

    else:
        with open(file_path, "w") as f:
            for i in ids:
                f.write(i + '\n')
            print(f"{file_name} created!")

    return file_path


def render_jobs(driver):
    """Function to render the page and return all the job ids"""

    try:
        driver.implicitly_wait(10)
        scroll_down(driver)
        html = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(html, "lxml")
        return soup

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def _get_job_ids(html_object):
    try:
        jobs = html_object.select("ul.jobs-search__results-list > li")
        ids = []
        for job in jobs:
            div = job.find("div")
            if "data-entity-urn" in div.attrs:
                job_id = div.attrs["data-entity-urn"]
                i = re.search(r"\d+", job_id)
                ids.append(str(i.group(0))) 

        return ids
    except (AttributeError, IndexError) as e:
        print(e)
        pass


def select_past_24_hour_jobs(driver):
    driver.implicitly_wait(10)
    past_job_btn = driver.find_element(By.XPATH, xpaths.PAST_24H_JOBS_BTN_XPATH)
    past_job_btn.click()
    past_24h_job_btn = driver.find_element(By.XPATH, '//*[@id="f_TPR-0"]')
    past_24h_job_done_btn = driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/div/button')
    driver.execute_script('arguments[0].click();', past_24h_job_btn)
    past_24h_job_done_btn.click()
    time.sleep(2)
    
    
