import unittest

from scrap import get_heading_from_html, get_first_paragraph_from_html


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


if __name__ == "__main__":
    unittest.main()
