from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def scrape_url_content(url):
    try:
        logging.debug("Setting up Selenium WebDriver")
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        logging.debug(f"Navigating to URL: {url}")
        # Navigate to the URL
        driver.get(url)
        
        logging.debug("Extracting text content from the body tag")
        # Extract text content (customize the selector as needed)
        content = driver.find_element(By.TAG_NAME, "body").text
        
        logging.debug("Saving the fetched content into a file for debugging")
        # Save the fetched content into a file for debugging
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(content)

        logging.debug("Quitting the Selenium WebDriver")
        driver.quit()
        
        return content
    except Exception as e:
        logging.error(f"An error occurred while fetching the URL content: {e}")
        return f"An error occurred while fetching the URL content: {e}"
