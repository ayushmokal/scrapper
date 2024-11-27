from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

class DoctorScraper:
    def __init__(self, driver):
        self.driver = driver
        
    def extract_doctor_info(self, element):
        """Extract doctor information from a search result element."""
        try:
            # Get name from h2 tag
            name = element.find_element(By.TAG_NAME, 'h2').text.strip()
            
            # Get address from p tag with location icon
            try:
                address_element = element.find_element(By.XPATH, ".//p[contains(text(), 'miles from')]")
                address = address_element.text.split('\n')[0].strip()
            except:
                address = "N/A"
            
            return {
                'name': name,
                'address': address
            }
        except Exception as e:
            print(f"Error extracting doctor info: {str(e)}")
            return None

    def scrape(self, zip_code):
        """Scrape doctor information for the given zip code."""
        base_url = f"https://health.usnews.com/doctors/search?distance=250&location={zip_code}&np_pa=false&specialty=Urology&sort=distance"
        doctors = []
        page = 1
        max_pages = 7  # Site shows 7 pages maximum
        
        while page <= max_pages:
            url = f"{base_url}&page_num={page}" if page > 1 else base_url
            print(f"\nProcessing page {page}...")
            self.driver.get(url)
            
            try:
                # Wait for doctor listings to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h2"))
                )
                
                # Wait for dynamic content
                time.sleep(2)
                
                # Find all doctor elements
                doctor_elements = self.driver.find_elements(By.XPATH, "//div[.//h2]")
                
                if not doctor_elements:
                    break
                
                for element in doctor_elements:
                    doctor_info = self.extract_doctor_info(element)
                    if doctor_info:
                        doctors.append(doctor_info)
                        print(f"Found doctor: {doctor_info['name']} at {doctor_info['address']}")
                
                page += 1
                
            except TimeoutException:
                print(f"Timeout on page {page}")
                break
                
        # Save results to CSV
        if doctors:
            filename = f"urologists_{zip_code}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['name', 'address'])
                writer.writeheader()
                writer.writerows(doctors)
            print(f"\nSaved {len(doctors)} doctors to {filename}")
        else:
            print("\nNo doctors found")
            
        return doctors