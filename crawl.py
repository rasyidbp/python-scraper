from urllib.parse import urlsplit, urljoin, urlparse
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests

def normalize_url(url):
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/")
    return parsed.netloc + path

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    h_tag = soup.find("h1")
    if not isinstance(h_tag, Tag):
        h_tag = soup.find("h2")

    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main")
    if isinstance(main, Tag):
        p_tag = main.find("p")
    else:
        p_tag = soup.find("p")

    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    for a_tag in soup.find_all("a"):
        if not isinstance(a_tag, Tag):
            continue

        href = a_tag.get("href")
        if href:
            urls.append(urljoin(base_url, href))

    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    image_urls = []

    for img_tag in soup.find_all("img"):
        if not isinstance(img_tag, Tag):
            continue

        src = img_tag.get("src")
        if src:
            image_urls.append(urljoin(base_url, src))

    return image_urls

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }

def get_html(url):
    response = requests.get(
        url,
        headers={"User-Agent": "BootCrawler/1.0"},
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise Exception("response content type is not text/html")

    return response.text

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url

    if page_data is None:
        page_data = {}

    if urlparse(base_url).netloc != urlparse(current_url).netloc:
        return page_data

    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        return page_data

    try:
        print(f"crawling: {current_url}")
        html = get_html(current_url)
    except Exception as e:
        print(f"error crawling {current_url}: {e}")
        return page_data

    data = extract_page_data(html, current_url)
    page_data[normalized_url] = data

    for next_url in data["outgoing_links"]:
        crawl_page(base_url, next_url, page_data)

    return page_data
