# Python Web Scraper

A simple asynchronous web crawler written in Python.

The crawler extracts information from webpages and generates a JSON report containing the crawled pages.

## Requirements

* Python 3.14+
* [uv](https://docs.astral.sh/uv/)

## Installation

Clone the repository:

```bash
git clone https://github.com/rasyidbp/python-scraper.git
cd python-scraper
```

Create the virtual environment:

```bash
uv venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install the project dependencies:

```bash
uv sync
```

The project includes `uv.lock`, so `uv sync` will install the locked dependency versions.

## Usage

Run the crawler with:

```bash
uv run main.py <URL> <MAX_CONCURRENCY> <MAX_PAGES>
```

For example:

```bash
uv run main.py https://learnwebscraping.dev/practice/ecommerce/ 3 10
```

Arguments:

* `URL` — The website where the crawl starts.
* `MAX_CONCURRENCY` — Maximum number of pages being fetched concurrently.
* `MAX_PAGES` — Maximum number of pages to crawl.

After the crawl finishes, a `report.json` file will be generated containing the crawled page data.

## Example

```bash
uv run main.py https://learnwebscraping.dev/practice/ecommerce/ 5 20
```

This starts the crawler at the ecommerce page, allows up to 5 concurrent requests, and crawls a maximum of 20 pages.

## JSON Report

The crawler creates `report.json` containing the crawled pages sorted by URL.

Example:

```json
[
  {
    "url": "https://example.com/",
    "heading": "Example Domain",
    "first_paragraph": "This domain is for use in illustrative examples...",
    "outgoing_links": [],
    "image_urls": []
  }
]
```

## Running Tests

Run the test suite with:

```bash
uv run -m unittest -v
```

## Project Structure

```text
python-scraper/
├── crawl.py
├── json_report.py
├── main.py
├── test_crawl.py
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

