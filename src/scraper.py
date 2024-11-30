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
        max_retries = 3
        
        while True:
            current_url = f"{base_url}&page_num={page}" if page > 1 else base_url
            print(f"\nProcessing page {page}...")
            
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    # Add longer random delay between page loads
                    time.sleep(random.uniform(4, 7))
                    self.driver.get(current_url)
                    
                    # Wait for initial page load
                    try:
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                    except TimeoutException:
                        print(f"Page load timeout for page {page}")
                        retry_count += 1
                        continue
                    
                    # Wait for doctor listings with increased timeout
                    try:
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.hvUhyf"))
                        )
                    except TimeoutException:
                        print(f"Doctor listings not found on page {page}")
                        retry_count += 1
                        continue
                    
                    # Find all doctor profile links that contain doctor names
                    doctor_links = self.driver.find_elements(
                        By.XPATH, 
                        "//a[contains(@href, '/doctors/') and .//h2[contains(@class, 'hvUhyf')]]"
                    )
                    
                    if not doctor_links:
                        print(f"No doctor links found on page {page}")
                        return urls
                    
                    for link in doctor_links:
                        try:
                            href = link.get_attribute('href')
                            name = link.find_element(By.TAG_NAME, 'h2').text.strip()
                            if href and '/doctors/' in href and 'search' not in href:
                                urls.append((href, name))
                        except Exception as e:
                            print(f"Error extracting link details: {str(e)}")
                            continue
                    
                    # Check if there are more pages
                    try:
                        next_button = self.driver.find_elements(
                            By.XPATH, 
                            "//button[contains(@aria-label, 'Next page')]"
                        )
                        if not next_button or 'disabled' in next_button[0].get_attribute('class'):
                            print("Reached last page")
                            return urls
                    except Exception as e:
                        print(f"Error checking next page button: {str(e)}")
                        return urls
                    
                    success = True
                    page += 1
                    
                except Exception as e:
                    print(f"Error on page {page} (attempt {retry_count + 1}): {str(e)}")
                    retry_count += 1
                    time.sleep(random.uniform(5, 8))
                    
            if not success:
                print(f"Failed to process page {page} after {max_retries} attempts")
                return urls
                
        return urls

    def extract_doctor_details(self, url_info):
        """Extract detailed doctor information from profile page."""
        url, name = url_info
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Add longer random delays between requests
                time.sleep(random.uniform(4, 7))
                self.driver.get(url)
                
                # Add an initial wait for any element to ensure page loads
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                except TimeoutException:
                    print(f"Page load timeout for {url}")
                    retry_count += 1
                    continue
                
                # Wait for the address container with increased timeout
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "fBaaRL"))
                    )
                except TimeoutException:
                    print(f"Address container not found for {url}")
                    retry_count += 1
                    continue
                
                # Get address with multiple fallback strategies
                address = "N/A"
                address_selectors = [
                    "div.Box-w0dun1-0 p:not(.fOMSOj)",
                    ".fBaaRL",
                    "//div[contains(@class, 'Box-w0dun1-0')]//p[contains(text(), ',')]"
                ]
                
                for selector in address_selectors:
                    try:
                        if selector.startswith("//"):
                            address_element = self.driver.find_element(By.XPATH, selector)
                        else:
                            address_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if address_element and address_element.text.strip():
                            address = address_element.text.strip()
                            break
                    except:
                        continue
                
                # Get phone with increased reliability
                phone = "N/A"
                phone_selectors = [
                    "a[href^='tel:']",
                    "//a[starts-with(@href, 'tel:')]",
                    ".//a[contains(@href, 'tel:')]"
                ]
                
                for selector in phone_selectors:
                    try:
                        if selector.startswith("//") or selector.startswith(".//"):
                            phone_element = self.driver.find_element(By.XPATH, selector)
                        else:
                            phone_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if phone_element and phone_element.text.strip():
                            phone = phone_element.text.strip()
                            break
                    except:
                        continue
                
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
                time.sleep(random.uniform(5, 8))  # Increased delay between retries
                
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