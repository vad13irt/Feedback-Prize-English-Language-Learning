from argparse import ArgumentParser
from ctypes import Union
from typing import Any, Dict, List, Optional, Tuple, Union
from selenium import webdriver
import pandas as pd


def get_num_pagination_pages(
    driver, 
    url: Optional[str] = None, 
    return_current_page: bool = False,
    ) -> Union[int, Tuple[int, int]]:

    if url is not None:
        driver.get(url) 
  
    pagination_pages_block = driver.find_element_by_class_name("wp-nav-links")
    pagination_pages_elements = pagination_pages_block.find_elements_by_class_name("page-numbers")
    max_pagination_pages = int(pagination_pages_elements[-1].text)
    
    if return_current_page:
        pagination_pages_tags = [pagination_pages_element.tag for pagination_pages_element in pagination_pages_elements]
        current_page = int(pagination_pages_tags.index("span")) + 1
        
        return current_page, max_pagination_pages

    return max_pagination_pages


def parse_essay_page(driver, url: Optional[str] = None, text_part_sep: str = "\n\n") -> Dict[str, Any]:
    if url is not None:
        driver.get(url)

    # topic
    topic_element = driver.find_element_by_class_name("article__heading")
    topic = str(topic_element.text)

    # text
    text_block = driver.find_element_by_class_name("article__content")
    text_elements = text_block.find_elements_by_tag_name("p")
    text_parts = [text_element.text for text_element in text_elements]
    text = text_part_sep.join(text_parts)

    # paper details
    table_element = driver.find_element_by_class_name("paper-details-table__tbody")
    names_elements = table_element.find_elements_by_class_name("paper-details-table__th")
    info_elements = table_element.find_elements_by_class_name("paper-details-table__td")

    type_, subjects = None, None
    for name_element, info_element in zip(names_elements, info_elements):
        name_element = name_element.text
        info_element = info_element.text

        if "Type" in name_element:
            type_ = info_element
        elif "Subjects" in name_element:
            subjects = info_element

    return {
        "topic": topic,
        "text": text,
        "type": type_,
        "subjects": subjects,
    }


def get_essays_urls_from_page(driver, url: Optional[str] = None) -> List[str]:
    if url is not None:
        driver.get(url)
    
    elements = driver.find_elements_by_class_name("article--list")

    urls = []
    for element in elements:
        link_element = element.find_element_by_class_name("article__heading-link")
        url = link_element.get_attribute("href")
        urls.append(url)

    return urls


def parse_page(driver, url: Optional[str] = None, num_essays: Optional[int] = None) -> List[Dict[str, Any]]:
    essays_urls = get_essays_urls_from_page(driver, url=url)

    if num_essays is not None:
        essays_urls = essays_urls[:num_essays]

    essays = []
    for essay_url in essays_urls:
        essay = parse_essay_page(driver, url=essay_url)
        essays.append(essay)
    
    return essays


def parse(
    driver, 
    url: str, 
    pagination_page_url_format: str = "{url}/page/{page}", 
    num_pages: Optional[int] = None, 
    num_essays_per_page: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
    
    num_pagination_pages = get_num_pagination_pages(driver, url=url)

    if num_pages is not None:
        num_pagination_pages = min(num_pages, num_pagination_pages)

    essays = []
    for page in range(1, num_pagination_pages + 1):
        page_url = pagination_page_url_format.format(url=url, page=page)
        page_essays = parse_page(driver, url=page_url, num_essays=num_essays_per_page)
        essays.extend(page_essays)

    return essays

    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--urls", nargs="+", required=True)
    parser.add_argument("--chrome_driver_path", default=None, required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--num_pages", type=int, required=False, default=None)
    parser.add_argument("--num_essays_per_page", type=int,  required=False, default=None)

    args = parser.parse_args()

    driver = webdriver.Chrome(args.chrome_driver_path)

    essays = []
    for url in args.urls:
        url_essays = parse(
            driver=driver, 
            url=url, 
            num_pages=args.num_pages, 
            num_essays_per_page=args.num_essays_per_page,
        )
        essays.extend(url_essays)

    driver.close()

    essays_data_frame = pd.DataFrame.from_dict(essays)
    essays_data_frame.to_csv(args.output_path, index=False)