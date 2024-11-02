from scraper import BonpreuScraper

# Run the scraper
if __name__ == "__main__":
    # Set the main url
    base_url = "https://www.compraonline.bonpreuesclat.cat"
    # Set the category to scrape
    category = "Frescos"
    # Create the scraper object
    scraper = BonpreuScraper(base_url, category)
    # Get the subcategories for the selected category
    subcategories = scraper.get_subcategories_names()
    # Get the products for the selected category
    scraper.get_product_info(subcategories[0])