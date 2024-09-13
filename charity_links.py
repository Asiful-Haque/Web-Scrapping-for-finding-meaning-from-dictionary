from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Function to scrape charity links and names from a single page with retries
def scrape_charity_links(page_url, driver, retries=3):
    for attempt in range(retries):
        try:
            driver.get(page_url)
            
            # Wait until the charity links are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'name'))
            )
            
            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract all charity links and names
            charity_elements = soup.find_all('a', class_='name')
            charities = []
            for element in charity_elements:
                name = element.text.strip()
                relative_link = element.get('href')
                full_link = f"https://www.acnc.gov.au{relative_link}"
                charities.append({"Charity Name": name, "Link": full_link})

            return charities

        except Exception as e:
            print(f"Failed to retrieve data for page: {page_url} on attempt {attempt + 1}\nError: {e}")
            if attempt < retries - 1:
                delay = random.uniform(5, 10)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"All retries failed for page: {page_url}")
                return []

# Setup Selenium WebDriver with custom options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')  # Suppress logs
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')

# Path to ChromeDriver for Windows (Ensure the path is correct)
service = Service(r'C:\Users\USER\Downloads\chromedriver_win32\chromedriver.exe')  # Use raw string to avoid escape character issues
driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://www.acnc.gov.au/charity/charities?page={}&f[]=countries%3A3411872625"
all_charities = []

# Loop through all the pages (e.g., 1791 pages)
total_pages = 1791
for page_number in range(1, total_pages + 1):
    page_url = base_url.format(page_number)
    print(f"Scraping page {page_number}/{total_pages}: {page_url}")
    
    # Scrape charity links from the page
    charities = scrape_charity_links(page_url, driver)
    all_charities.extend(charities)
    
    # Add a delay of 3 to 6 seconds between requests to avoid triggering server limits
    delay = random.uniform(3, 6)
    print(f"Waiting for {delay:.2f} seconds before the next request...")
    time.sleep(delay)  

driver.quit()

# Convert the list of charities to a DataFrame and save as CSV
if all_charities:
    df = pd.DataFrame(all_charities)
    df.to_csv(r'C:\Users\USER\Desktop\charity_links.csv', index=False)  # Use raw string for path
    print("Data successfully scraped and saved to 'charity_links.csv'")
else:
    print("No data was scraped, CSV file was not created.")
