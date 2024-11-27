import sys
from src import create_browser, DoctorScraper, save_to_csv, DEFAULT_ZIP_CODE

def get_zip_code():
    while True:
        zip_code = input("Enter ZIP code (or press Enter for default ZIP code - {}): ".format(DEFAULT_ZIP_CODE)).strip()
        if not zip_code:
            return DEFAULT_ZIP_CODE
        if zip_code.isdigit() and len(zip_code) == 5:
            return zip_code
        print("Invalid ZIP code. Please enter a 5-digit number.")

def main():
    # Get ZIP code from command line argument or prompt user
    zip_code = sys.argv[1] if len(sys.argv) > 1 else get_zip_code()
    driver = None
    
    try:
        print(f"Starting scraping for zip code: {zip_code}")
        print("This may take a few moments...")
        
        driver = create_browser()
        scraper = DoctorScraper(driver)
        doctors = scraper.scrape(zip_code)
        
        if not doctors:
            print("No doctors found for the specified location.")
            return
        
        filename = save_to_csv(doctors, zip_code)
        
        print("✓ Scraping completed successfully")
        print(f"✓ Found {len(doctors)} doctors")
        print(f"✓ Data saved to {filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()