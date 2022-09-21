import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from argparse import ArgumentParser


HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

PARSER = "html.parser"


def get_essay_info(url, headers=HEADERS, parser=PARSER, sep="\n\n", **response_args):
    response = requests.get(url=url, headers=headers, **response_args)
    soup = BeautifulSoup(response.text, parser)

    topic = soup.find(class_="article__heading").text
    text_elements = soup.find(class_="article__content").findAll("p")
    text_parts = [text_element.text for text_element in text_elements]
    text = sep.join(text_parts)

    return {
        "url": url,
        "topic": topic,
        "text": text,
    }

def get_page_essays(url, headers=HEADERS, parser=PARSER, verbose=10, n_jobs=-1, **essay_args):
    print(f"Parsing '{url}'")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, parser)
    
    essays_blocks = soup.find_all(class_="article--list")

    essays = []

    iterator = tqdm(essays_blocks, total=len(essays_blocks))
    for essay_block in iterator:
        essay_url = essay_block.find(class_="article__heading-link").get("href")
        essay = get_essay_info(url=essay_url, headers=headers, parser=parser, **essay_args)
        essays.append(essay)

    return essays


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output_path", default="ivypanda_essays.csv", required=False)

    args = parser.parse_args()

    response = requests.get(url=args.url, headers=HEADERS)
    soup = BeautifulSoup(response.text, PARSER)

    pagination_block = soup.find(class_="wp-nav-links")
    pagination_elements = pagination_block.findAll("a")
    num_pagination_pages = int(pagination_elements[-1].text)
    
    pagination_page_format = "{url}/page/{page}"

    essays = []
    for page in range(1, num_pagination_pages + 1):    
        page_url = pagination_page_format.format(url=args.url, page=page)
        page_essays = get_page_essays(url=page_url)
        essays.extend(page_essays)
        print()

    num_essays = len(essays)
    print(f"Totally parsed {num_essays} essays")

    essays_data_frame = pd.DataFrame.from_dict(essays)
    essays_data_frame.to_csv(args.output_path, index=False)

    print(f"{num_essays} essays were saved to '{args.output_path}'")