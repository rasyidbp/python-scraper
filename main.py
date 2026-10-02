import sys, requests

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

    html = get_html(base_url)
    print(html)

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


if __name__ == "__main__":
    main()
