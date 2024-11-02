from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import unicodedata
import numpy as np
import pandas as pd
from pathlib import Path

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
    
    def __init__(self, base_url, category):
        self.base_url = base_url
        if not category or category not in self.default_categories:
            raise ValueError("Category not found. Use BonpreuScraper.categories() to get the available categories.")
        else:
            self.category = category
              
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

    def get_subcategories_names(self) -> list:
        """
        Gets the names of subcategories of the selected category.
        
        Returns:
            list: List containing the subcategories.
        """
        # Get the URL of the categories section
        categories_url = self._get_categories_section_url()
        # Get the page content of the categories section
        categories_page = self._parse_html(categories_url, dynamic_content=False)
        # Get the soup of the categories page
        categories_soup = self._get_soup(categories_page)
        # Get the div tag containing the categories menu
        categories_menu = categories_soup.find('div', {
            'class': 'sc-1wz1hmv-0 cmTtoc'
        })
        # Filter the categories menu to get the desired category
        category = [cat for cat in categories_menu.find_all('a') if cat.text == self.category][0]
        # Get the html content of the subcategory page
        subcat_page = self._parse_html(self.base_url + category["href"], dynamic_content=False)
        # Get the soup of the subcategory page
        subcat_soup = self._get_soup(subcat_page)
        # Get the div tag containing the subcategories menu
        self.subcat_menu = subcat_soup.find('div', {
        'class': 'sc-1wz1hmv-0 cmTtoc'
        })
        
        return [subcat.text for subcat in self.subcat_menu.find_all('a')]

    def _extract_subcategory_links(self, url):
        """
        Helper function to extract subcategory links at the given URL.
        If subcategories exist, returns a list of (text, full_url) tuples; otherwise, returns None.
        """
        # Get the html content of the subcategory page
        subcat_page = self._parse_html(url, dynamic_content=False)
        # Get the soup of the subcategory page
        subcat_soup = self._get_soup(subcat_page)
        # Get the div tag containing the subcategories menu
        subcat_menu = subcat_soup.find('div', {
        'class': 'sc-1wz1hmv-0 cmTtoc'
        })
        
        return [(a.text, self.base_url + a['href']) for a in subcat_menu.find_all('a')] if subcat_menu else None
    
    def _extract_subcat_structure(self, subcategory) -> list:
        """
        Extracts the hierarchical structure of the subcategories and their URLs.
        The structure of the returned list is as follows:
            [
                category, subcategory_1, subcategory_2, subcategory_3, subcategory_4, url, 
                ...
            ]
        When a subcategory does not have subcategories, the list will contain None until the URL.
        
        Args:
            subcategory (str): Name of the subcategory.
        
        Returns:
            list: List of URLs of the subcategories.
        """
        # Set the first two levels of the hierarchy
        # Level 0 and level 1 are the category and subcategory, respectively defined by the user
        level_0_text = self.category
        level_1_text = subcategory

        # Get the level_1 subcategory object
        level_1_subcat = [subcat for subcat in self.subcat_menu() if subcat.text == level_1_text][0]
        level_1_url = self.base_url + level_1_subcat.find('a')['href']

        # Initialize the list to store the subcategories
        subcat_list = []

        # Extract the subcategories of level 2
        level_2_subcats = self._extract_subcategory_links(level_1_url)

        for level_2_text, url_2 in level_2_subcats:
            # Extract the subcategories of level 3
            level_3_subcats = self._extract_subcategory_links(url_2)

            if level_3_subcats: # If there are subcategories of level 3
                
                for level_3_text, url_3 in level_3_subcats:
                    # Extract the subcategories of level 4
                    level_4_subcats = self._extract_subcategory_links(url_3)

                    if level_4_subcats: # If there are subcategories of level 4
                        
                        for level_4_text, url_4 in level_4_subcats:
                            subcat_list.append([level_0_text, level_1_text, level_2_text, level_3_text, level_4_text, url_4])
                    
                    else: # Without level 4
                        subcat_list.append([level_0_text, level_1_text, level_2_text, level_3_text, None, url_3])
            
            else: # Without level 3
                subcat_list.append([level_0_text, level_1_text, level_2_text, None, None, url_2])
        
        return subcat_list
        
    def _convert_price(self, price_str) -> float:
        """
        Converts the price string to a float.
        
        Args:
            price_str (str): Price string to convert.
            
            Returns:
                float: Price as a float.
        """
        return float(price_str.replace('\xa0€', '').replace(',', '.'))

    def get_product_info(self, subcategory) -> tuple:
        """
        Extracts all products and their information from the given subcategory.

        Args:
            subcategory (str): Name of the subcategory.

        """
        if isinstance(subcategory, list):
            raise ValueError("Please, select a single subcategory to avoid saturating the server.")
                
        # First, get the list of URLs
        subcat_structure_list = self._extract_subcat_structure(subcategory)
        url_list = [subcat_structure[-1] for subcat_structure in subcat_structure_list]
        
        # Initialize lists for product details we want to save
        cat, subcat_1, subcat_2, subcat_3, subcat_4, product_names, product_prices, product_urls = [], [], [], [], [], [], [], []
        
        # Iterate through the URLs to get the product details
        for i, url in enumerate(url_list):
                        
            # Get the parsed HTML content
            subcategory_page = self._parse_html(url, dynamic_content=False)
            subcategory_soup = self._get_soup(subcategory_page)         

            # Extract product details from each product card
            for product in subcategory_soup.find_all("div", {'class': 'product-card-container'}):
                
                # Extract product name
                product_name = product.find('a').get("aria-label", None)

                # Extract product price
                product_price = product.find('span', {'class': '_text_16wi0_1 _text--m_16wi0_23 sc-1fkdssq-0 bwsVzh'})
                product_price = self._convert_price(product_price.text) if product_price else np.nan

                # Extract product URL
                product_url = product.find('a').get('href', None)
                product_url = self.base_url + product_url if product_url else None

                # Append extracted details to lists
                cat = subcat_structure_list[i][0]
                subcat_1 = subcat_structure_list[i][1]
                subcat_2 = subcat_structure_list[i][2]
                subcat_3 = subcat_structure_list[i][3]
                subcat_4 = subcat_structure_list[i][4]
                product_names.append(product_name)
                product_prices.append(product_price)
                product_urls.append(product_url)
        
        # Save the product information to a CSV file
        print(f"Extracted {len(product_names)} products from the {self.category}>{subcategory} subcategory.")
        return self._save_csv((cat, subcat_1, subcat_2, subcat_3, subcat_4, product_names, product_prices, product_urls))
            
    def _save_csv(self, product_info):
        """
        Saves the product information to a CSV file.
        
        Args:
            product_info (tuple): Tuple containing the product information.
        """
        
        # Create a DataFrame from the product information
        product_df = pd.DataFrame({
            'Category': product_info[0],
            'Subcategory_1': product_info[1],
            'Subcategory_2': product_info[2],
            'Subcategory_3': product_info[3],
            'Subcategory_4': product_info[4],
            'Product Name': product_info[5],
            'Price': product_info[6],
            'URL': product_info[7]
        })
        
        # Create the filename based on the category + subcategory_1 + timestamp
        # Example: Frescos_Carns_20210901_120000.csv
        
        # First, check that category and subcategory_1 do not contain spaces and special characters
        category = product_info[0].replace(' ', '_').replace('/', '_')
        subcategory_1 = product_info[1].replace(' ', '_').replace('/', '_')
        # Remove special characters
        category = unicodedata.normalize('NFKD', category).encode('ascii', 'ignore').decode('utf-8')
        subcategory_1 = unicodedata.normalize('NFKD', subcategory_1).encode('ascii', 'ignore').decode('utf-8')
        
        # Get the current timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Create the filename
        filename = Path(__file__).parent.parent / "data" / f"{category}_{subcategory_1}_{timestamp}.csv"
        
        # Save the DataFrame to a CSV file
        product_df.to_csv(filename, index=False)
        
        print(f"Product information saved to {filename}.")
        
        return product_df