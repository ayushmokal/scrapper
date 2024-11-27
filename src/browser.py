from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os
import sys
import platform

def create_browser():
    """Create and configure Chrome browser instance."""
    try:
        # Print system information for debugging
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.platform()}")
        print(f"Architecture: {platform.architecture()}")
        
        chrome_options = Options()
        # Temporarily disable headless mode for debugging
        # chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--window-size=1920,1080')
        
        print("Installing Chrome WebDriver...")
        # Get the latest version of ChromeDriver
        driver_path = ChromeDriverManager().install()
        
        # Verify the driver path exists and points to the executable
        if not driver_path.endswith('.exe'):
            # Try to find the actual executable
            driver_dir = os.path.dirname(driver_path)
            possible_paths = [
                os.path.join(driver_dir, 'chromedriver.exe'),
                os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe'),
                os.path.join(driver_dir, 'chromedriver-win32', 'chromedriver.exe')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    driver_path = path
                    break
        
        print(f"WebDriver path: {driver_path}")
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver executable not found at {driver_path}")
            
        service = Service(executable_path=driver_path)
        
        # Create the Chrome WebDriver instance
        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        print("Chrome WebDriver created successfully")
        return driver
        
    except Exception as e:
        print("\nDetailed error information:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Google Chrome is installed on your system")
        print("2. Try running the script without the --headless mode")
        print("3. Check if your Chrome browser version matches the WebDriver version")
        print("4. Make sure you have administrative privileges")
        
        if isinstance(e, WebDriverException):
            print("\nAdditional WebDriver troubleshooting:")
            print("5. Try clearing the Chrome WebDriver cache:")
            print("   - Delete the .wdm folder in your user directory")
            print("6. Make sure your Chrome browser is up to date")
        
        if isinstance(e, FileNotFoundError):
            print("\nChrome WebDriver path troubleshooting:")
            print("7. Manual installation steps:")
            print("   - Download ChromeDriver from: https://chromedriver.chromium.org/downloads")
            print("   - Extract the executable to a known location")
            print("   - Add the location to your system PATH")
        raise