from urllib.parse import urlsplit

def normalize_url(url):
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/")
    return parsed.netloc + path
