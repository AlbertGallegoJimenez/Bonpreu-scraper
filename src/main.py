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
    parser.add_argument('--category', type=str, nargs='+', choices=all_categories + ["all"],
                        help='Specify one or more categories to scrape or "all" for all categories.')
    parser.add_argument('--subcategories', type=str, nargs='*',
                        help='Specify subcategories to scrape (optional, only applies to single categories).')
    parser.add_argument('--list-categories', action='store_true',
                            help='List available categories and exit.')
    parser.add_argument('--list-subcategories', action='store_true',
                        help='List available subcategories for the selected category and exit.')
    args = parser.parse_args()
    
    # List categories if requested
    if args.list_categories:
        print("Available categories:")
        for category in all_categories:
            print(f"- {category}")
        return  # Exit after listing categories
       
    # If "all" is selected, replace args.category with all categories
    if "all" in args.category:
        selected_categories = all_categories
    else:
        selected_categories = args.category
    
    # Check if multiple categories and subcategories were specified
    if len(selected_categories) > 1 and args.subcategories:
        print("Error: Subcategories cannot be specified when multiple categories are selected.")
        return  # Exit if invalid combination is provided
    
    # Check if multiple categories are selected with list-subcategories
    if len(selected_categories) > 1 and args.list_subcategories:
        print("Error: Cannot list subcategories for multiple categories. Please specify a single category.")
        return  # Exit if invalid combination is provided
    
    # Iterate over each selected category
    for category in selected_categories:
        # Create scraper instance for the specified category
        scraper = BonpreuScraper(base_url, category)
    
        # List subcategories if requested
        if args.list_subcategories:
            subcategories = scraper.get_subcategories_names()
            print(f"Available subcategories for '{category}':")
            for sub in subcategories:
                print(f"- {sub}")
            continue  # Continue to next category after listing subcategories
    
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
            if len(selected_categories) == 1:
                # No subcategories specified, scrape all subcategories in the category
                print("No specific subcategories provided. Scraping all available subcategories.")
            all_subcategories = scraper.get_subcategories_names()
            scraper.get_product_info(all_subcategories)

if __name__ == "__main__":
    main()
