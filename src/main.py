from browser import create_browser
from scraper import DoctorScraper

def main():
    try:
        # Get ZIP code from user
        zip_code = input("Enter ZIP code (or press Enter for default ZIP code - 10081): ").strip()
        if not zip_code:
            zip_code = "10081"
            
        print(f"Starting scraping for zip code: {zip_code}")
        print("This may take a few moments...")
        
        # Create browser instance
        driver = create_browser()
        
        # Create scraper instance and run scraping
        scraper = DoctorScraper(driver)
        doctors = scraper.scrape(zip_code)
        
        # Close browser
        driver.quit()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main() 