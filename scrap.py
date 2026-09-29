from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag

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
