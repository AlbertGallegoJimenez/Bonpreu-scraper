import unittest
from unittest.mock import patch, MagicMock
import os
import sys
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scraper import BonpreuScraper

class TestBonpreuScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = BonpreuScraper(base_url="https://www.compraonline.bonpreuesclat.cat",
                                      category="Frescos")

    @patch('src.scraper.requests.get')
    def test_parse_html_static(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        html = self.scraper._parse_html(url="https://www.compraonline.bonpreuesclat.cat", dynamic_content=False)
        self.assertEqual(html, "<html></html>")

    @patch('src.scraper.webdriver.Chrome')
    def test_parse_html_dynamic(self, mock_chrome):
        mock_driver = MagicMock()
        mock_driver.page_source = "<html></html>"
        mock_chrome.return_value = mock_driver

        html = self.scraper._parse_html(url="https://www.compraonline.bonpreuesclat.cat", dynamic_content=True)
        self.assertEqual(html, "<html></html>")

    def test_get_soup(self):
        html = "<html><body><div>Test</div></body></html>"
        soup = self.scraper._get_soup(html)
        self.assertEqual(soup.find('div').text, "Test")

    @patch('src.scraper.BonpreuScraper._parse_html')
    @patch('src.scraper.BonpreuScraper._get_soup')
    def test_get_categories_section_url(self, mock_get_soup, mock_parse_html):
        mock_parse_html.return_value = "<html></html>"
        mock_soup = MagicMock()
        mock_soup.find_all.return_value = [MagicMock()]
        mock_get_soup.return_value = mock_soup

        url = self.scraper._get_categories_section_url()
        self.assertIsNotNone(url)

    @patch('src.scraper.BonpreuScraper._parse_html')
    @patch('src.scraper.BonpreuScraper._get_soup')
    def test_get_subcategories_names(self, mock_get_soup, mock_parse_html):
        mock_parse_html.return_value = "<html></html>"
        mock_soup = MagicMock()
        mock_soup.find.return_value = MagicMock()
        mock_soup.find_all.return_value = [MagicMock(text="Subcategory1"), MagicMock(text="Subcategory2")]
        mock_get_soup.return_value = mock_soup

        subcategories = self.scraper.get_subcategories_names()
        self.assertIsInstance(subcategories, list)

    def test_convert_price(self):
        price_str = "12,34\xa0€"
        price = self.scraper._convert_price(price_str)
        self.assertEqual(price, 12.34)

    def test_normalize_text(self):
        text = "Café"
        normalized_text = self.scraper._normalize_text(text)
        self.assertEqual(normalized_text, "Cafe")

if __name__ == '__main__':
    unittest.main()