from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class BonpreuScraper():
    """
    A web scraper for the Bonpreu website to gather product prices and other relevant information.
    
    Attributes:
        base_url (str): The main URL of the Bonpreu website.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        
    def _get_soup(self, url: str = None) -> BeautifulSoup:
        """
        Sets up a Selenium WebDriver to retrieve and parse HTML content of the page.
        Uses a headless browser to minimize resource usage.
        
        Args:
            url (str): URL of the page to scrape. If None, uses the base URL.
            
        Returns:
            BeautifulSoup: Parsed HTML content of the page.
        """
        try:
            # Set up headless Chrome WebDriver options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            
            # Initialize WebDriver
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(2) # Wait for page to load
            
            # Parse page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            return soup
        
        except Exception as e:
            print(f"Error occurred while loading the page: {e}")
        finally:
            driver.quit()
            
        return
    
    def get_categories_section_url(self) -> str:
        """
        Retrieves the URL of the categories section from the navigation menu.
        The categories web page is accessed through the Supermercat section.
        
        Returns:
            str: URL of the categories page, if found. Otherwise, None.
        """
        try:
            # Get the main page soup
            self.main_soup = self._get_soup(self.base_url)
            
            # Get the navigation menus from the main page where the Supermercat is located
            nav_menu = self.main_soup.find_all('ul', {
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
                        self.categories_section_url = self.base_url + categories_tag.find('a')['href']
                        
                        return self.categories_section_url
                    
            else:
                print("Error occurred while getting the categories section URL: nav_menu is not a list.")
                return
        except Exception as e:
            print(f"Error occurred while getting the categories section URL: {e}")
            
            return
    
    def get_categories(self) -> str:
        """
        Retrieves the individual URLs of the categories of products available on the Supermercat page.
        """
        try:
            # Get the Supermercat page soup
            self.categories_soup = self._get_soup(self.categories_section_url)
            
            # Get the div tag containing the categories menu
            self.categories_menu = self.categories_soup .find('div', {
                'class': 'sc-1wz1hmv-0 cmTtoc'
            })
            
            # Create a dictionary to store the categories and their URLs
            self.categories_dict = {}
            for cat in self.categories_menu.find_all('a'):
                self.categories_dict[cat.text] = self.base_url + cat["href"]
                
            return self.categories_dict
                
        except Exception as e:
            print(f"Error occurred while getting the categories: {e}")
            
            return
    
    

