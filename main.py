import sys
import time

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from packages import xpaths
    from packages.utils import (
        chrome_options,
        get_input,
        _get_job_ids,
        dump_ids_into_file,
        render_jobs,
        select_past_24_hour_jobs,
    )
except ModuleNotFoundError as e:
    print(e)
    print("Install dependencies from requirements.txt")
    sys.exit()


def main():
    """Function that returns Job ids of a search query in the respective country"""

    query, location = get_input()
    url = "https://www.linkedin.com/login"
    options = chrome_options(silence=False)
    driver = webdriver.Chrome(
        service=(ChromeService(ChromeDriverManager().install())), options=options
    )
    driver.get(url)
    driver.implicitly_wait(10)
    job_btn = driver.find_element(By.XPATH, xpaths.JOBS_BTN_XPATH)
    job_btn.click()
    search_input = driver.find_element(By.XPATH, xpaths.SEARCH_XPATH)
    search_input.click()
    time.sleep(1)
    search_input.send_keys(query)
    country_input = driver.find_element(By.XPATH, xpaths.COUNTRY_XPATH)
    country_input.click()
    country_input.send_keys(location)
    search_btn = driver.find_element(By.XPATH, xpaths.SEARCH_BTN_XPATH)
    search_btn.click()
    driver.implicitly_wait(10)
    date_posted = driver.find_element(By.XPATH, xpaths.DATE_POSTED_XPATH)
    date_posted.click()
    past_24h_jobs = driver.find_element(By.XPATH, xpaths.P)
    driver.execute_script('argument[0].click();', )
    # query_element = driver.find_element(By.XPATH, xpaths.SEARCH_XPATH)
    # query_element.send_keys(query)
    # country_query = driver.find_element(By.XPATH, xpaths.COUNTRY_XPATH)
    # country_query.clear()
    # country_query.send_keys(location)
    # search_button = driver.find_element(By.XPATH, xpaths.SEARCH_BTN_XPATH)
    # search_button.click()
    # driver.implicitly_wait(10)
    # select_past_24_hour_jobs(driver)
    # html = render_jobs(driver)
    # ids = _get_job_ids(html)
    # file_path = dump_ids_into_file(ids, query)


def sd():
    with open('job_ids/game_developer_jobs.txt', 'r') as f:
        lines = f.read().splitlines()
    print(lines)
    print(len(lines))
    print(len(set(lines)))

if __name__ == "__main__":
    main()
    # sd()