from scraper import BonpreuScraper
import argparse

def main():
    """
    Main function to run the Bonpreu scraper.
    """
    # Set the base URL and available categories from BonpreuScraper
    base_url = "https://www.compraonline.bonpreuesclat.cat"
    all_categories = BonpreuScraper.categories()
    
    # Configure parser
    parser = argparse.ArgumentParser(description="Run the Bonpreu scraper.")
    parser.add_argument('--category', type=str, choices=all_categories + ["all"],
                        help='Specify the category to scrape or "all" for all categories.')
    parser.add_argument('--subcategories', type=str, nargs='*',
                        help='Specify subcategories to scrape (optional, only applies to single categories).')
    parser.add_argument('--list-subcategories', action='store_true',
                        help='List available subcategories for the selected category and exit.')
    args = parser.parse_args()
    
    # Check category selection
    if args.category == "all":
        print("Cannot list subcategories when 'all' is selected. Please specify a single category.")
        return
    
    # Create scraper instance for the specified category
    scraper = BonpreuScraper(base_url, args.category)
    
    # List subcategories if requested
    if args.list_subcategories:
        subcategories = scraper.get_subcategories_names()
        print("Available subcategories for '{}':".format(args.category))
        for sub in subcategories:
            print(f"- {sub}")
        return  # Exit after listing subcategories
    
    # Validate and filter subcategories
    if args.subcategories:
        # Get available subcategories for validation
        available_subcategories = scraper.get_subcategories_names()
        selected_subcategories = [sub for sub in args.subcategories if sub in available_subcategories]
        
        if not selected_subcategories:
            print("No valid subcategories selected.")
            return
        
        print(f"Scraping selected subcategories: {selected_subcategories}")
        scraper.get_product_info(selected_subcategories)
    else:
        # No subcategories specified, scrape all subcategories in the category
        print("No specific subcategories provided. Scraping all available subcategories.")
        all_subcategories = scraper.get_subcategories_names()
        scraper.get_product_info(all_subcategories)

if __name__ == "__main__":
    main()
