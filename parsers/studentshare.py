import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from argparse import ArgumentParser
from IPython.display import display
from typing import Dict, Any, Optional, List
from tqdm import tqdm
import pandas as pd
import warnings
import re
import time

from constants import PARSER, HEADERS


warnings.simplefilter("ignore")


def get_essay_info(
    url: str, 
    parser: str = PARSER, 
    headers: Dict[str, Any] = HEADERS, 
    sep: str = "\n\n",
) -> Dict[str, Any]:
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, parser)
    
    if response.status_code != 404:
        element = soup.find(class_="extract_sample_bl")

        topic = element.find("h2").text
        topic_pattern = r'"(.*?)"'
        topic = re.findall(topic_pattern, topic)[0]
        
        text_element = element.find(class_="content")
        text_parts_elements = text_element.findAll("p")
        text_parts = [text_art_element.text for text_art_element in text_parts_elements]
        text = sep.join(text_parts)
        
        essay_info_element = soup.find(class_="info_document")
        essay_info_elements = essay_info_element.findAll("a")
        essay_info_texts = [essay_info_element.text for essay_info_element in essay_info_elements]
        subject, type_, level, *_ = essay_info_texts
        
        return {
            "url": url,
            "topic": topic,
            "text": text,
            "subject": subject,
            "type": type_,
            "level": level,
        }

    return None


def set_filter_inputs(
    driver, 
    xpath: str, 
    values: List[str] = [], 
    value_delay: float = 3.0,
    menu_delay: float = 5.0, 
    menu_xpath: str = '//*[@id="ui-id-1"]',
) -> None:
    input_element = driver.find_element(by=By.XPATH, value=xpath)
    for value in values:
        driver.implicitly_wait(value_delay)
        input_element.send_keys(value)
        time.sleep(menu_delay)
        
        menu_element = driver.find_element(by=By.XPATH, value=menu_xpath)
        menu_options = menu_element.find_elements(by=By.TAG_NAME, value="li")

        for menu_option in menu_options:
            if menu_option.text == value:
                menu_option.click()
                driver.implicitly_wait(value_delay)

def set_filter_choices(
    driver, 
    class_name: str, 
    values: List[str] = [], 
    value_delay: float = 2.0,
) -> None:
    choices_element = driver.find_element(by=By.CLASS_NAME, value=class_name)
    buttons = choices_element.find_elements(by=By.TAG_NAME, value="button")
    for value in values:
        for button in buttons:
            if button.text == value:
                driver.execute_script("arguments[0].click();", button)
                driver.implicitly_wait(value_delay)


def set_filter_interval_inputs(
    driver, 
    min_xpath: str, 
    max_xpath: str, 
    min_value: Optional[int] = None, 
    max_value: Optional[int] = None, 
    delay: float = 3.0,
) -> None:
    if min_value is not None:
        min_value_input = driver.find_element(by=By.XPATH, value=min_xpath)
        min_value_input.send_keys(str(min_value))
        driver.implicitly_wait(delay)

    if max_value is not None:
        max_value_input = driver.find_element(by=By.XPATH, value=max_xpath)
        max_value_input.send_keys(str(max_value))
        driver.implicitly_wait(delay)


def filter_results(
    driver, 
    document_types:Optional[List[str]] = None, 
    min_pages: Optional[int] = None, 
    max_pages: Optional[int] = None, 
    subjects: Optional[int] = None, 
    downloads: Optional[List[str]] = None, 
    min_amount_of_words: Optional[int] = None, 
    max_amount_of_words: Optional[int] = None, 
    levels: Optional[List[str]] = None, 
) -> None:  

    # openning all settings
    filter_element = driver.find_element(by=By.CLASS_NAME, value="filtr_container")
    unwrap_elements = filter_element.find_elements(by=By.CLASS_NAME, value="section_filtr_bl")
    unwrap_elements = [
        unwrap_element.find_element(by=By.CLASS_NAME, value="title") for unwrap_element in unwrap_elements
    ]

    for unwrap_element in unwrap_elements:
        driver.execute_script("arguments[0].click();", unwrap_element)
        time.sleep(2)

    time.sleep(3)

    if document_types is not None:
        set_filter_inputs(
            driver=driver, 
            xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[3]/input', 
            values=document_types,
        )
    
    if subjects is not None:
        set_filter_inputs(
            driver=driver, 
            xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[4]/input', 
            values=subjects,
        )
    
    if min_pages is not None or max_pages is not None:
        set_filter_interval_inputs(
            driver=driver, 
            min_xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[5]/div[2]/div/input[1]', 
            max_xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[5]/div[2]/div/input[2]', 
            min_value=min_pages, 
            max_value=max_pages,
        )

    if downloads is not None:
        set_filter_choices(
            driver=driver, 
            class_name="download-filter", 
            values=downloads,
        )

    if min_amount_of_words is not None or max_amount_of_words is not None:
        set_filter_interval_inputs(
            driver=driver, 
            min_xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[7]/div[2]/div/div[1]/input',
            max_xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[7]/div[2]/div/div[2]/input',
            min_value=min_amount_of_words,
            max_value=max_amount_of_words,
        )

    if levels is not None:
        set_filter_choices(
            driver=driver, 
            class_name="level-filter", 
            values=levels,
        )

    apply_button_element = driver.find_element(by=By.XPATH, value='//*[@id="filters-form"]/button[1]')
    driver.execute_script("arguments[0].click();", apply_button_element)


def login(
    driver, 
    email: str, 
    password: str, 
    url: str = "https://studentshare.org/login", 
    loading_page_delay: float = 5.0, 
    input_delay: float = 3.0,
) -> None:
    driver.get(url)
    time.sleep(loading_page_delay)
    
    # email
    email_input_element = driver.find_element(by=By.XPATH, value='//*[@id="loginform-email"]')
    email_input_element.send_keys(email)
    time.sleep(input_delay)    

    # password
    password_input_element = driver.find_element(by=By.XPATH, value='//*[@id="loginform-password_hash"]')
    password_input_element.send_keys(password)
    time.sleep(input_delay)    

    # checkboxes
    checkboxes_element = driver.find_element(by=By.XPATH, value='//*[@id="sign_in"]/div/div/div/div[1]/div[1]/p/label')
    checkboxes_element.click()
    time.sleep(input_delay)

    # login button
    login_button_element = driver.find_element(by=By.XPATH, value='//*[@id="sign_in"]/div/div/div/div[1]/input')
    login_button_element.click()
    time.sleep(input_delay)


def get_essays(driver) -> List[Dict[str, Any]]:
    essays = []
    essays_blocks = driver.find_elements(by=By.CLASS_NAME, value="c_p")
    for essay_block in tqdm(essays_blocks, total=len(essays_blocks)):
        essay_content = essay_block.find_element(by=By.CLASS_NAME, value="product_content")
        essay_url_element = essay_content.find_element(by=By.TAG_NAME, value="a")
        essay_url = essay_url_element.get_attribute("href")
        essay = get_essay_info(url=essay_url)

        if essay is not None:
            essays.append(essay)
        
    return essays

def parse(
    chrome_driver_path: str, 
    url: str, 
    window_width: int = 1980,
    window_height: int = 1280,
    email: Optional[str] = None, 
    password: Optional[str] = None,
    output_path: str = "studentshare_essays.csv",
    loading_page_delay: float = 10.0, 
    loading_results_delay: float = 10.0,
    **filter_args,
) -> None:
    driver = webdriver.Chrome(chrome_driver_path)
    driver.set_window_size(window_width, window_height)    

    # login
    if email is not None and password is not None:
        login(driver, email=email, password=password)


    driver.get(url)
    time.sleep(loading_page_delay)

    # filtering
    filter_results(driver, **filter_args)
    time.sleep(loading_results_delay)

    # found essays
    found_essays_text = driver.find_element(by=By.CLASS_NAME, value="result_item").text
    result = re.search("results of (.*) items", found_essays_text)
    found_essays = int(result.group(1))
    print(f"Found {found_essays} essays")

    # num pagination pages
    pagination_block = driver.find_element(by=By.CLASS_NAME, value="pagination")
    pagination_elements = pagination_block.find_elements(by=By.TAG_NAME, value="a")
    num_pagination_pages = int(pagination_elements[-2].text)
    print(f"Num pages: {num_pagination_pages}")
    
    # parsing
    essays = []
    stop = False
    page = 1
    while not stop:
        print(f"Parsing {page} page")
        pagination_essays = get_essays(driver)
        essays.extend(pagination_essays)
        
        pagination_block = driver.find_element(by=By.CLASS_NAME, value="pagination")
        pagination_elements = pagination_block.find_elements(by=By.TAG_NAME, value="li")
        next_page_button_element = pagination_elements[-1]

        if next_page_button_element.get_attribute("class") != "next disabled":
            next_page_button = next_page_button_element.find_element(by=By.TAG_NAME, value="a")
            driver.execute_script("arguments[0].click();", next_page_button)
        else:
            stop = True

        page += 1

        time.sleep(loading_page_delay)

    driver.close()

    essays_data_frame = pd.DataFrame.from_dict(essays)
    essays_data_frame.to_csv(args.output_path, index=False)
    display(essays_data_frame)

    num_essays = len(essays)
    print(f"{num_essays} essays were saved to '{output_path}'")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--chrome_driver_path", required=True)
    parser.add_argument("--email",  required=True)
    parser.add_argument("--password",  required=True)
    parser.add_argument("--output_path", default="studentshare_essays.csv", required=False)
    parser.add_argument("--document_types", nargs="+", default=None, required=False)
    parser.add_argument("--subjects", nargs="+", default=None, required=False)
    parser.add_argument("--levels", nargs="+", default=None, required=False)
    parser.add_argument("--min_pages", default=None, required=False)
    parser.add_argument("--max_pages", default=None, required=False)
    parser.add_argument("--min_amount_of_words", default=None, required=False)
    parser.add_argument("--max_amount_of_words", default=None, required=False)
    parser.add_argument("--downloads", nargs="+", default=None, required=False)
    parser.add_argument("--loading_page_delay", default=10, required=False)
    parser.add_argument("--loading_results_delay", default=10, required=False)
    parser.add_argument("--window_width", default=1980, required=False)
    parser.add_argument("--window_height", default=1280, required=False)
    
    args = parser.parse_args()

    parse(
        url=args.url,
        chrome_driver_path=args.chrome_driver_path, 
        email=args.email,
        password=args.password,
        output_path=args.output_path, 
        document_types=args.document_types, 
        subjects=args.subjects, 
        levels=args.levels, 
        min_pages=args.min_pages, 
        max_pages=args.max_pages, 
        min_amount_of_words=args.min_amount_of_words, 
        max_amount_of_words=args.max_amount_of_words,
        loading_page_delay=args.loading_page_delay,
        downloads=args.downloads,
        loading_results_delay=args.loading_results_delay,
        window_width=args.window_width,
        window_height=args.window_height,
    )