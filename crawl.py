from urllib.parse import urlsplit, urljoin, urlparse
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import aiohttp, asyncio

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

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=1, max_pages=100):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False

            if normalized_url in self.visited:
                return False

            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False

            self.visited.add(normalized_url)
            return True

    async def get_html(self, url):
        async with self.session.get(
            url,
            headers={"User-Agent": "BootCrawler/1.0"},
        ) as response:
            if response.status >= 400:
                raise Exception(f"HTTP error: {response.status}")

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                raise Exception("response content type is not text/html")

            return await response.text()

    async def crawl_page(self, current_url):
        if self.should_stop:
            return

        if urlparse(current_url).netloc != self.base_domain:
            return

        normalized_url = normalize_url(current_url)

        if not await self.add_page_visit(normalized_url):
            return

        try:
            async with self.semaphore:
                print(f"crawling: {current_url}")
                html = await self.get_html(current_url)

            data = extract_page_data(html, current_url)

            async with self.lock:
                self.page_data[normalized_url] = data

            tasks = []

            for next_url in data["outgoing_links"]:
                if self.should_stop:
                    break

                task = asyncio.create_task(
                    self.crawl_page(next_url)
                )
                self.all_tasks.add(task)
                tasks.append(task)

            if tasks:
                try:
                    await asyncio.gather(*tasks)
                finally:
                    for task in tasks:
                        self.all_tasks.discard(task)

        except Exception as e:
            print(f"error crawling {current_url}: {e}")

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(
        base_url,
        max_concurrency=max_concurrency,
        max_pages=max_pages,
    ) as crawler:
        return await crawler.crawl()
