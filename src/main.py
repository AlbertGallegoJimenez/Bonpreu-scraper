from scraper import BonpreuScraper

# Run the scraper
if __name__ == "__main__":
    # Set the main url
    base_url = "https://www.compraonline.bonpreuesclat.cat"
    # Create the scraper object
    scraper = BonpreuScraper(base_url)
    # Get the categories section url
    scraper.get_categories_url()
    # Get the categories
    scraper.get_categories()
    