import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from typing import Dict, Any, List
from IPython.display import display

from constants import HEADERS, PARSER


def get_essay_info(
    url: str, 
    headers: Dict[str, Any] = HEADERS, 
    parser: str = PARSER, 
    sep: str = "\n\n", 
    **response_args,
) -> Dict[str, Any]:

    response = requests.get(url=url, headers=headers, **response_args)
    soup = BeautifulSoup(response.text, parser)

    topic = soup.find(class_="article__heading").text
    
    text_elements = soup.find(class_="article__content").findChildren(recursive=False)
    text_parts = [
        text_element.text for text_element in text_elements if "div" not in text_element.name
    ]

    text = sep.join(text_parts)

    details_element = soup.find(class_="paper-details-table__tbody")
    names = details_element.findAll("th")
    description_elements = details_element.findAll("td")
    
    subject, type_ = None, None
    for name, description_element in zip(names, description_elements):
        name = name.text.strip()
        if name == "Type":
            type_ = description_element.text.strip().replace("\n", ", ")
        elif name == "Subjects":
            subjects_elements = description_element.findAll("a")
            subject = [
                subject_element.text.strip() for subject_element in subjects_elements
            ]

    return {
        "url": url,
        "topic": topic,
        "text": text, 
        "subject": subject,
        "type": type_,
    }


def get_page_essays(
    url: str, 
    headers: Dict[str, Any] = HEADERS, 
    parser: str = PARSER, 
    **essay_args,
) -> List[Dict[str, Any]]:
    print(f"Parsing '{url}'")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, parser)
    
    essays_blocks = soup.find_all(class_="article--list")

    essays = []
    for essay_block in tqdm(essays_blocks, total=len(essays_blocks)):
        essay_heading_element = essay_block.find(class_="article__heading-link")
        essay_url = essay_heading_element.get("href")
        essay = get_essay_info(url=essay_url, headers=headers, parser=parser, **essay_args)
        essays.append(essay)

    return essays

def parse(
    url: str, 
    output_path: str="ivypanda_essays.csv", 
    headers: Dict[str, Any] = HEADERS, 
    parser: str = PARSER, 
    pagination_page_format: str = "{url}/page/{page}",
) ->  None:
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, parser)

    pagination_block = soup.find(class_="wp-nav-links")
    pagination_elements = pagination_block.findAll("a")
    num_pagination_pages = int(pagination_elements[-1].text)
    

    essays = []
    for page in range(1, num_pagination_pages + 1):    
        page_url = pagination_page_format.format(url=url, page=page)
        page_essays = get_page_essays(url=page_url)
        essays.extend(page_essays)
        print()

    num_essays = len(essays)
    print(f"Totally parsed {num_essays} essays")

    essays_data_frame = pd.DataFrame.from_dict(essays)
    essays_data_frame.to_csv(output_path, index=False)
    display(essays_data_frame)
    print(f"{num_essays} essays were saved to '{output_path}'")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output_path", default="ivypanda_essays.csv", required=False)
    parser.add_argument("--pagination_page_format", default="{url}/page/{page}", required=False)

    args = parser.parse_args()

    parse(
        url=args.url, 
        output_path=args.output_path, 
        pagination_page_format=args.pagination_page_format,
    )