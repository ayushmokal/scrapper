from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import random

class DoctorScraper:
    def __init__(self, driver):
        self.driver = driver
        self.unique_doctors = set()
        
    def extract_doctor_urls(self, zip_code):
        """Extract doctor profile URLs from search page."""
        base_url = f"https://health.usnews.com/doctors/search?distance=250&location={zip_code}&np_pa=false&specialty=Urology&sort=distance"
        urls = []
        page = 1
        
        while True:
            current_url = f"{base_url}&page_num={page}" if page > 1 else base_url
            print(f"\nProcessing page {page}...")
            
            try:
                self.driver.get(current_url)
                time.sleep(random.uniform(2, 4))  # Random delay between requests
                
                # Wait for doctor listings to load
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h2.hvUhyf"))
                )
                
                # Find all doctor profile links that contain doctor names
                doctor_links = self.driver.find_elements(
                    By.XPATH, 
                    "//a[contains(@href, '/doctors/') and .//h2[contains(@class, 'hvUhyf')]]"
                )
                
                if not doctor_links:
                    break
                    
                for link in doctor_links:
                    try:
                        href = link.get_attribute('href')
                        name = link.find_element(By.TAG_NAME, 'h2').text.strip()
                        if href and '/doctors/' in href and 'search' not in href:
                            urls.append((href, name))
                    except:
                        continue
                
                # Check if there are more pages
                next_button = self.driver.find_elements(
                    By.XPATH, 
                    "//button[contains(@aria-label, 'Next page')]"
                )
                if not next_button or 'disabled' in next_button[0].get_attribute('class'):
                    break
                    
                page += 1
                time.sleep(random.uniform(1, 2))  # Random delay between pages
                
            except Exception as e:
                print(f"Error on page {page}: {str(e)}")
                time.sleep(5)  # Longer delay on error
                continue
                
        return urls

    def extract_doctor_details(self, url_info):
        """Extract detailed doctor information from profile page."""
        url, name = url_info
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.driver.get(url)
                time.sleep(random.uniform(2, 3))  # Random delay between profile visits
                
                # Wait for the address container to load
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "fBaaRL"))
                )
                
                # Get address
                address = "N/A"
                try:
                    address_element = self.driver.find_element(
                        By.CLASS_NAME, "fBaaRL"
                    )
                    if address_element:
                        address = address_element.text.strip()
                except:
                    pass
                
                # Get phone
                phone = "N/A"
                try:
                    phone_element = self.driver.find_element(
                        By.CSS_SELECTOR, "a[href^='tel:']"
                    )
                    if phone_element:
                        phone = phone_element.text.strip()
                except:
                    pass
                
                doctor_key = f"{name}-{address}"
                if doctor_key not in self.unique_doctors:
                    self.unique_doctors.add(doctor_key)
                    return {
                        'name': name,
                        'address': address,
                        'phone': phone,
                        'profileUrl': url
                    }
                return None
                
            except (TimeoutException, WebDriverException) as e:
                print(f"Attempt {retry_count + 1} failed for {url}: {str(e)}")
                retry_count += 1
                time.sleep(5)  # Longer delay between retries
                
        print(f"Failed to extract details after {max_retries} attempts for {url}")
        return None

    def scrape(self, zip_code):
        """Scrape doctor information for the given zip code."""
        doctors = []
        urls = self.extract_doctor_urls(zip_code)
        print(f"\nFound {len(urls)} doctor profiles")
        
        for url_info in urls:
            doctor_info = self.extract_doctor_details(url_info)
            if doctor_info:
                doctors.append(doctor_info)
                print(f"Found doctor: {doctor_info['name']} at {doctor_info['address']}")
            time.sleep(random.uniform(1, 2))  # Random delay between processing doctors
            
        return doctors