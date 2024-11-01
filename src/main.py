from scraper import BonpreuScraper

# Run the scraper
if __name__ == "__main__":
    # Set the main url
    base_url = "https://www.compraonline.bonpreuesclat.cat"
    # Create the scraper object
    scraper = BonpreuScraper(base_url)
    # Get the categories url dictionary
    categories = scraper.get_categories_url('Frescos')
    categories_urls = scraper.extract_nested_values(categories)
    # Get the products info lists
    products = scraper.get_product_info(categories_urls[0])
    
    