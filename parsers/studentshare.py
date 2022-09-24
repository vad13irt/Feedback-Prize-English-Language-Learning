import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from argparse import ArgumentParser
from IPython.display import display
from tqdm import tqdm
import pandas as pd
import re
import time

from constants import PARSER, HEADERS


def get_essay_info(url, parser=PARSER, headers=HEADERS, sep="\n\n"):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, parser)
    
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


def set_filter_inputs(
    driver, 
    xpath, 
    values=[], 
    value_delay=3,
    menu_delay=5, 
    menu_xpath='//*[@id="ui-id-1"]',
):
    input_element = driver.find_element_by_xpath(xpath)
    for value in values:
        time.sleep(value_delay)
        input_element.send_keys(value)
        time.sleep(menu_delay)
        
        menu_element = driver.find_element_by_xpath(menu_xpath)
        menu_options = menu_element.find_elements_by_tag_name("li")

        for menu_option in menu_options:
            if menu_option.text == value:
                menu_option.click()
                time.sleep(value_delay)

def set_filter_choices(driver, class_name, values=[], value_delay=2):
    choices_element = driver.find_element_by_class_name(class_name)
    buttons = choices_element.find_elements_by_tag_name("button")
    for value in values:
        for button in buttons:
            if button.text == value:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(value_delay)


def set_filter_interval_inputs(driver, min_xpath, max_xpath, min_value=None, max_value=None, delay=3):
    if min_value is not None:
        min_value_input = driver.find_element_by_xpath(min_xpath)
        min_value_input.send_keys(str(min_value))
        time.sleep(delay)

    if max_value is not None:
        max_value_input = driver.find_element_by_xpath(max_xpath)
        max_value_input.send_keys(str(max_value))
        time.sleep(delay)


def filter_results(
    driver, 
    document_types=None, 
    min_pages=None, 
    max_pages=None, 
    subjects=None, 
    downloads=None, 
    min_amount_of_words=None, 
    max_amount_of_words=None, 
    levels=None, 
):  

    # openning all settings
    filter_element = driver.find_element_by_class_name("filtr_container")
    unwrap_elements = filter_element.find_elements_by_class_name("section_filtr_bl")

    for unwrap_element in unwrap_elements:
        unwrap_element.click()
        time.sleep(2)

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

    apply_button_element = driver.find_element_by_xpath('//*[@id="filters-form"]/button[1]')
    driver.execute_script("arguments[0].click();", apply_button_element)


def login(driver, email, password, url="https://studentshare.org/login", loading_page_delay=5, input_delay=3):
    driver.get(url)
    time.sleep(loading_page_delay)
    
    # email
    email_input_element = driver.find_element_by_xpath('//*[@id="loginform-email"]')
    email_input_element.send_keys(email)
    time.sleep(input_delay)    

    # password
    password_input_element = driver.find_element_by_xpath('//*[@id="loginform-password_hash"]')
    password_input_element.send_keys(password)
    time.sleep(input_delay)    

    # checkboxes
    checkboxes_element = driver.find_element_by_xpath('//*[@id="sign_in"]/div/div/div/div[1]/div[1]/p/label')
    checkboxes_element.click()
    time.sleep(input_delay)

    # login button
    login_button_element = driver.find_element_by_xpath('//*[@id="sign_in"]/div/div/div/div[1]/input')
    login_button_element.click()
    time.sleep(input_delay)


def parse(
    chrome_driver_path, 
    url, 
    window_width=1980,
    window_height=1280,
    email=None, 
    password=None,
    output_path="studentshare_essays.csv",
    loading_page_delay=10, 
    loading_results_delay=10,
    **filter_args,
):
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
    found_essays_text = driver.find_element_by_class_name("result_item").text
    pattern = "results of (.*) items"
    result = re.search(pattern, found_essays_text)
    found_essays = int(result.group(1))
    print(f"Found {found_essays} essays")

    # num pagination pages
    pagination_block = driver.find_element_by_class_name("pagination")
    pagination_elements = pagination_block.find_elements_by_tag_name("a")
    num_pagination_pages = int(pagination_elements[-2].text)
    print(f"Num pages: {num_pagination_pages}")
    
    # parsing
    essays = []
    for page in range(num_pagination_pages):
        print(f"Parsing {page} page")
        essays_blocks = driver.find_elements_by_class_name("c_p")

        pagination_essays = []
        for essay_block in tqdm(essays_blocks, total=len(essays_blocks)):
            essay_content = essay_block.find_element_by_class_name("product_content")
            essay_url_element = essay_content.find_element_by_tag_name("a")
            essay_url = essay_url_element.get_attribute("href")
            essay = get_essay_info(url=essay_url)
            pagination_essays.append(essay)
        
        essays.extend(pagination_essays)
        
        next_page_button_element = pagination_elements[-1]
        if next_page_button_element.get_attribute("class") != "next disabled":
            driver.refresh()
            next_page_button_element.click()

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