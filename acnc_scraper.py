from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Function to scrape data using Selenium and BeautifulSoup
def scrape_charity_data(url, driver):
    retries = 5  # Number of retries
    for i in range(retries):
        try:
            driver.get(url)

            # Wait until the desired element is loaded
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'title.text-uppercase'))
            )
            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract organization name from the specific div and h1 tag
            organization_name = soup.find('h1', class_='title text-uppercase').text.strip() if soup.find('h1', class_='title text-uppercase') else None
            abn = soup.find('a', href=lambda x: x and 'http://www.abr.business.gov.au/SearchByAbn.aspx?SearchText=' in x).text.strip() if soup.find('a', href=lambda x: x and 'http://www.abr.business.gov.au/SearchByAbn.aspx?SearchText=' in x) else None
            address = soup.find('address', class_='m-0').text.strip().replace('<br>', ', ') if soup.find('address', class_='m-0') else None
            email = soup.find('a', href=lambda x: x and x.startswith('mailto:')).text.strip() if soup.find('a', href=lambda x: x and x.startswith('mailto:')) else None
            website = None

            return {
                "Organization Name": organization_name,
                "ABN": abn,
                "Address": address,
                "Email": email,
                "Website": website
            }

        except Exception as e:
            print(f"Attempt {i+1}/{retries} failed for URL: {url}\nError: {e}")
            if i < retries - 1:  # If not the last retry
                backoff_time = 5 * (2 ** i)  # Exponential backoff
                print(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                print(f"Failed to retrieve data after {retries} attempts.")
                return None

# Setup Selenium WebDriver
service = Service('/Users/ahnafsayed/Downloads/chromedriver_mac_arm64/chromedriver')  # Update this path
driver = webdriver.Chrome(service=service)

# List of charity profile URLs
charity_urls = [
     "https://www.acnc.gov.au/charity/charities/0af726e3-2daf-e811-a963-000d3ad24077/profile",
    "https://www.acnc.gov.au/charity/charities/b7ea26e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/8af926e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/3fef26e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/07f726e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/004126dd-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/d6d8f517-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/d1e626e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/fb6fee1d-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/c8f726e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/22f326e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/7cfa26e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/69d6f517-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/0cd7f517-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/ebf526e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/2ff126e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/73742ce9-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/5af626e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/c4732ce9-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/82f626e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/ebd8f517-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/b9d7f517-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/6d1b7b09-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/d95578d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/725478d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/b5d31e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/5a5178d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/175278d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/14d31e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/3d3426dd-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/0fd01e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/5a5678d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/b3902710-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/96c41e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/fb4f78d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/adcd1e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/709b2710-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/4b5778d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/aad41e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/b09a2710-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/065178d6-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/9bcf1e16-2caf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/25f926e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/bdf826e3-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/63d6f517-38af-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/de4326dd-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/ff3c26dd-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/594026dd-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/534426dd-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/93732ce9-2daf-e811-a963-000d3ad24077/profile",
"https://www.acnc.gov.au/charity/charities/51e826e3-2daf-e811-a963-000d3ad24077/profile",
    # Add charity profile URLs here...
]

all_charity_data = []

for url in charity_urls:
    print(f"Scraping data for: {url}")
    data = scrape_charity_data(url, driver)
    if data:
        all_charity_data.append(data)
    
    # Random delay between requests to avoid getting blocked
    delay = random.uniform(5, 10)
    print(f"Waiting for {delay:.2f} seconds before the next request...")
    time.sleep(delay)

driver.quit()

# Convert to DataFrame and save as CSV
if all_charity_data:
    df = pd.DataFrame(all_charity_data)
    df.to_csv('/Users/saifulislam/Desktop/all_charities_info.csv', index=False)
    print("Data successfully scraped and saved to 'all_charities_info.csv'")
else:
    print("No data was scraped, CSV file was not created.")
