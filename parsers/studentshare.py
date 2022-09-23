from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import pandas as pd
import re
from argparse import ArgumentParser
from IPython.display import display
import time


# def get_essay_info(url, parser=PARSER, headers=HEADERS, sep="\n\n"):
#     element = soup.find(class_="extract_sample_bl")

#     topic = element.find("h2").text
#     topic_pattern = r'"(.*?)"'
#     topic = re.findall(topic_pattern, topic)[0]

#     text_element = element.find(class_="content")
#     text_parts_elements = text_element.findAll("p")
#     text_parts = [text_art_element.text for text_art_element in text_parts_elements]
#     text = sep.join(text_parts)

#     essay_info_element = soup.find(class_="info_document")
#     essay_info_elements = essay_info_element.findAll("a")
#     essay_info_texts = [essay_info_element.text for essay_info_element in essay_info_elements]
#     subject, type_, level, *_ = essay_info_texts

#     return {
#         "url": url,
#         "text": text,
#         "topic": topic,
#         "subject": subject,
#         "type": type_,
#         "level": level,
#     }


# def get_page_essays(url, parser=PARSER, headers=HEADERS, essay_url_format="{url}{essay_url}"):
#     essays_blocks = soup.findAll(class_="product_description")
    
#     essays = []
#     for essay_block in tqdm(essays_blocks, total=len(essays_blocks)):
#         essay_url_element = essay_block.find(class_="doc_title")
#         essay_url = essay_url_element.get("href")
#         essay_url = essay_url_format.format(url=url, essay_url=essay_url)
#         essay = get_essay_info(url=essay_url, parser=parser, headers=headers)
#         essays.append(essay)

#     return essays

def set_filter_inputs(
    driver, 
    xpath, 
    values=[], 
    value_wise_delay=5, 
    menu_wait_delay=3, 
    menu_xpath='//*[@id="ui-id-1"]',
):
    input_element = driver.find_element_by_xpath(xpath)
    for value in values:
        time.sleep(value_wise_delay)
        input_element.send_keys(value)
        time.sleep(menu_wait_delay)
        
        menu_element = driver.find_element_by_xpath(menu_xpath)
        menu_options = menu_element.find_elements_by_tag_name("li")

        for menu_option in menu_options:
            if menu_option.text == value:
                menu_option.click()
                break

def set_filter_choices(driver, class_name, values=[], button_delay=1):
    choices_element = driver.find_element_by_class_name(class_name)
    buttons = choices_element.find_elements_by_tag_name("button")
        
    for value in values:
        for button in buttons:
            if button.text == value:
                button.click()
                time.sleep(button_delay)


def set_filter_interval_inputs(driver, xpath, values=(None, None)):
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--chrome_driver_path", required=True)
    parser.add_argument("--output_path", default="studentshare_essays.csv", required=False)
    parser.add_argument("--document_types", nargs="+", default=None, required=False)
    parser.add_argument("--subjects", nargs="+", default=None, required=False)
    parser.add_argument("--levels", nargs="+", default=None, required=False)
    parser.add_argument("--pages", nargs="+", default=None, required=False)
    parser.add_argument("--amount_of_words", nargs="+", default=None, required=False)
    parser.add_argument("--downloads", nargs="+", default=None, required=False)
    
    args = parser.parse_args()

    driver = webdriver.Chrome(args.chrome_driver_path)
    driver.get(args.url)

    if args.document_types is not None:
        set_filter_inputs(
            driver=driver, 
            xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[3]/input', 
            values=args.document_types,
        )
    
    if args.subjects is not None:
        set_filter_inputs(
            driver=driver, 
            xpath='//*[@id="3"]/div[2]/div[2]/div[1]/div/div/div[4]/input', 
            values=args.subjects,
        )
    
    if args.pages is not None:
        pass

    if args.downloads is not None:
        set_filter_choices(driver=driver, class_name="download-filter", values=args.downloads)

    if args.amount_of_words is not None:
        pass

    if args.levels is not None:
        set_filter_choices(driver=driver, class_name="level-filter", values=args.levels)




    time.sleep(10)
    driver.close()

    # essays = get_page_essays(args.url)

    # essays_data_frame = pd.DataFrame.from_dict(essays)
    # essays_data_frame.to_csv(args.output_path, index=False)
    # display(essays_data_frame)