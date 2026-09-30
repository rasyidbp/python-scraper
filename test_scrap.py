import unittest
from scrap import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data

class TestScrap(unittest.TestCase):

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual,  expected)

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual,  expected)

    def test_normalize_url(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual,  expected)

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual,  expected)

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual,  expected)

class TestGetHeadingFromHTML(unittest.TestCase):

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>No heading here.</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


class TestGetFirstParagraphFromHTML(unittest.TestCase):

    def test_get_first_paragraph_from_html_basic(self):
        input_body = """
        <html>
            <body>
                <p>First paragraph.</p>
                <p>Second paragraph.</p>
            </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """
        <html>
            <body>
                <p>Outside paragraph.</p>
                <main>
                    <p>Main paragraph.</p>
                </main>
            </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_body)

        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = """
        <html>
            <body>
                <h1>Test Title</h1>
            </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

class TestGetUrlsFromHTML(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'

        actual = get_urls_from_html(input_body, input_url)

        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)


    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
            </body>
        </html>
        """

        actual = get_urls_from_html(input_body, input_url)

        expected = [
            "https://crawler-test.com/about",
            "https://crawler-test.com/contact",
        ]
        self.assertEqual(actual, expected)


    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <a href="/one">One</a>
                <a href="https://example.com/two">Two</a>
                <a href="/three">Three</a>
            </body>
        </html>
        """

        actual = get_urls_from_html(input_body, input_url)

        expected = [
            "https://crawler-test.com/one",
            "https://example.com/two",
            "https://crawler-test.com/three",
        ]
        self.assertEqual(actual, expected)

class TestGetImagesFromHTML(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'

        actual = get_images_from_html(input_body, input_url)

        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)


    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://example.com/logo.png" alt="Logo"></body></html>'

        actual = get_images_from_html(input_body, input_url)

        expected = ["https://example.com/logo.png"]
        self.assertEqual(actual, expected)


    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html>
            <body>
                <img alt="No source">
                <img src="/logo.png" alt="Logo">
            </body>
        </html>
        """

        actual = get_images_from_html(input_body, input_url)

        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

class TestGetPageData(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }

        self.assertEqual(actual, expected)


    def test_extract_page_data_h2_fallback(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Fallback Heading</h2>
            <p>First paragraph.</p>
            <a href="/about">About</a>
        </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "Fallback Heading",
            "first_paragraph": "First paragraph.",
            "outgoing_links": ["https://crawler-test.com/about"],
            "image_urls": [],
        }

        self.assertEqual(actual, expected)


    def test_extract_page_data_empty_content(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <div>No useful content here.</div>
        </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
