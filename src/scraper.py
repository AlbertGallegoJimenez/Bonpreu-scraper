from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from itertools import chain
import numpy as np

class BonpreuScraper():
    """
    A web scraper for the Bonpreu website to gather product prices and other relevant information.
    
    Attributes:
        base_url (str): The main URL of the Bonpreu website.
    """
    # Default categories to scrape
    default_categories = [
        "Frescos", "Alimentació", "Begudes",
        "Làctics i ous", "Celler"
        ]
    
    def __init__(self, base_url, categories=None):
        self.base_url = base_url
              
    @classmethod
    def categories(cls):
        """Method to get the categories."""
        return cls.default_categories
    
    def _parse_html(self, url: str = None, dynamic_content = False) -> str:
        """
        Parses the HTML content of the page.
        
        Args:
            url (str): URL of the page to scrape. If None, uses the base URL.
            dynamic_content (bool): If True, uses Selenium to scrape the page.
            
        Returns:
            str: HTML content of the page.
        """
        try:
            if dynamic_content:
                # Sets the driver
                driver = webdriver.Chrome()
                # Opens the URL
                driver.get(url)
                # Scrolls to the bottom of the page to load all the content
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Waits for the page to load
                time.sleep(2)
                # Gets the page source
                page_source = driver.page_source
                # Closes the driver
                driver.quit()
            
                return page_source
            
            else:
            
                # Define the headers to avoid being blocked
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive"
                }
                
                # Use requests to get the page content
                response = requests.get(url, headers=headers)
                #time.sleep(2) # Wait for page to load
                
                return response.text
        
        except Exception as e:
            print(f"Error occurred while loading the page: {e}")
            
        return
        
    def _get_soup(self, html_page) -> BeautifulSoup:
        """
        Creates a BeautifulSoup object for the webpage passed.
        
        Args:
            html_page (str): HTML content of the page.
            
        Returns:
            BeautifulSoup: Parsed HTML content of the page.
        """
        try:
            # Create a BeautifulSoup object
            soup = BeautifulSoup(html_page, 'html.parser')
            
            return soup
        
        except Exception as e:
            print(f"Error occurred while parsing the HTML: {e}")
        
        return
    
    def _get_categories_section_url(self) -> str:
        """
        Retrieves the URL of the categories section from the navigation menu.
        The categories web page is accessed through the Supermercat section.
        
        Returns:
            str: URL of the categories page, if found. Otherwise, None.
        """
        try:
            # Get the main page content
            main_page = self._parse_html(self.base_url, dynamic_content=False)
            
            # Get the main page soup
            main_soup = self._get_soup(main_page)
            
            # Get the navigation menus from the main page where the Supermercat is located
            nav_menu = main_soup.find_all('ul', {
                'id': 'nav-menu',
                'aria-labelledby': 'nav-menu-button',
                'role': 'menu',
                'class': 'sc-1w5m3ly-0 aIFnR'
            })
            
            # As the previous find_all returns a list,
            # we need to get the element where "Supermercat" is located
            if isinstance(nav_menu, list):
                for ul in nav_menu:
                    if ul.find('li', string='Supermercat'):
                        # Get the url of the Supermercat page
                        categories_tag = ul.find('li', string='Supermercat')
                        categories_section_url = self.base_url + categories_tag.find('a')['href']
                        
                        return categories_section_url
                    
            else:
                print("Error occurred while getting the categories section URL: nav_menu is not a list.")
                return
        except Exception as e:
            print(f"Error occurred while getting the categories section URL: {e}")
            
            return
        
    def _iterate_nested_subcategories(self, subcat_name, subcat_url) -> dict:
        """
        Iterates through the nested subcategories to get the URLs of the products.
        
        Args:
            subcat_name (str): Name of the subcategory.
            subcat_url (str): URL of the subcategory.
            
        Returns:
            dict: Dictionary containing the subcategories and their URLs.
        """
        # Create a dictionary to store the subcategories and their URLs
        subcat_dict = {}
        # Get the html content of the subcategory page
        subcat_page = self._parse_html(subcat_url, dynamic_content=False)
        # Get the soup of the subcategory page
        subcat_soup = self._get_soup(subcat_page)
        # Get the div tag containing the subcategories menu
        subcat_menu = subcat_soup.find('div', {
        'class': 'sc-1wz1hmv-0 cmTtoc'
        })
        if subcat_menu: # Check if the subcategory page has a subcategory menu
            subsubcats = subcat_menu.find_all('a')
            for subsubcat in subsubcats:
                subsubcat_name = subsubcat.text.strip()
                subsubcat_url = self.base_url + subsubcat["href"]
                # Recursively iterate through the subcategories
                subcat_dict[subsubcat_name] = self._iterate_nested_subcategories(subsubcat_name, subsubcat_url)
        else:
            # Store the subcategory URL
            subcat_dict[subcat_name] = subcat_url

        return subcat_dict
    
    def _clean_output_subcategories(self, subcat_dict) -> dict:
        """
        Cleans the nested subcategories dictionary to remove duplicate entries.
        
        Args:
            subcat_dict (dict): Dictionary containing the nested subcategories.
            
        Returns:
            dict: Cleaned dictionary with the subcategories and their URLs.
        """
        # Create a dictionary to store the cleaned subcategories
        clean_dict = {}
        
        for key, value in subcat_dict.items():
            if isinstance(value, dict):
                # Recursively clean the nested subcategories
                cleaned_value = self._clean_output_subcategories(value)
                # Check if the cleaned subcategory is a single URL
                if len(cleaned_value) == 1 and key in cleaned_value:
                    clean_dict[key] = cleaned_value[key] # Assign the URL directly
                else:
                    clean_dict[key] = cleaned_value  # Assign the cleaned subcategory
            else:
                # Store the subcategory URL
                clean_dict[key] = value
        
        return clean_dict
    
    def get_categories_url(self, categories=None) -> str:
        """
        Extracts categories and their URLs from the categories menu.

        Returns:
            list: A list of tuples containing category names and their nested subcategories.
        """
        if not categories:
            raise ValueError("Categories must be provided. Use BonpreuScraper.categories() to get the default categories.")
        elif not isinstance(categories, list):
            categories = [categories]
            
        try:
            # Get the URL of the categories section
            self.categories_url = self._get_categories_section_url()
            # Get the page content of the categories section
            self.categories_page = self._parse_html(self.categories_url, dynamic_content=False)
            # Get the soup of the categories page
            self.categories_soup = self._get_soup(self.categories_page)
            # Get the div tag containing the categories menu
            self.categories_menu = self.categories_soup.find('div', {
                'class': 'sc-1wz1hmv-0 cmTtoc'
            })

            # Create a dict to store the categories and their URLs
            self.categories_dict = {}
            for category in self.categories_menu.find_all('a'):
                # Filter the categories to scrape
                if category.text not in categories:
                    continue
                # Get the category name and its URL
                category_name = category.text
                category_url = self.base_url + category["href"]
                
                # Call the function to get the nested subcategories
                nested_subcategories = self._iterate_nested_subcategories(category_name, category_url)
                
                # Clean the nested subcategories dictionary
                cleaned_subcategories = self._clean_output_subcategories(nested_subcategories)
                
                # Append the category name and its URL to the dict
                self.categories_dict[category_name] = cleaned_subcategories

            return self.categories_dict

        except Exception as e:
            print(f"Error occurred while getting the categories: {e}")
            return

    def extract_nested_values(self, d):
        """
        Extracts the nested values from a dictionary.
        Ref: https://www.geeksforgeeks.org/python-get-all-values-from-nested-dictionary/
        
        Args:
            d (dict): Dictionary to extract the values from.
            
        Returns:
            list: List of the extracted values.
        """
        return list(chain.from_iterable(
            [self.extract_nested_values(v) if isinstance(v, dict) else [v]
            if isinstance(v, str) else v for v in d.values()]
        ))
        
    def _convert_price(self, price_str):
        """
        Converts the price string to a float.
        
        Args:
            price_str (str): Price string to convert.
            
            Returns:
                float: Price as a float.
        """
        
        return float(price_str.replace('\xa0€', '').replace(',', '.'))

    def get_product_info(self, url):
        """
        Extracts product information from the given URL.

        Args:
            url (str): URL of the category page.

        Returns:
            tuple: Tuple of lists containing the names, prices, and URLs of the products.
        """
        # Get the parsed HTML content
        category_page = self._parse_html(url, dynamic_content=False)
        category_soup = self._get_soup(category_page)

        # Initialize lists for product details
        product_names, product_prices, product_urls = [], [], []

        # Extract product details from each product card
        for product in category_soup.find_all("div", {'class': 'product-card-container'}):
            
            # Extract product name
            product_name = product.find('a').get("aria-label", np.nan)

            # Extract product price
            product_price = product.find('span', {'class': '_text_16wi0_1 _text--m_16wi0_23 sc-1fkdssq-0 bwsVzh'})
            product_price = self._convert_price(product_price.text) if product_price else np.nan

            # Extract product URL
            product_url = product.find('a').get('href', None)
            product_url = self.base_url + product_url if product_url else np.nan

            # Append extracted details to lists
            product_names.append(product_name)
            product_prices.append(product_price)
            product_urls.append(product_url)

        return product_names, product_prices, product_urls