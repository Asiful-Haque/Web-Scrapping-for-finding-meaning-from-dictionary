import pymysql  # or mysql.connector for MySQL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

# Database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='newdatabase'
)

# Function to get all words from the database
def get_words_from_db():
    cursor = connection.cursor()
    cursor.execute("SELECT word FROM v3_simple_list")
    words = cursor.fetchall()  # Returns list of tuples
    return [word[0] for word in words]

# Function to insert the word and meaning into the database
def save_word_meaning_to_db(word, meaning):
    cursor = connection.cursor()
    query = "INSERT INTO meanings (word, meaning) VALUES (%s, %s)"
    cursor.execute(query, (word, meaning))
    connection.commit()

# Function to scrape the meaning of the word
def scrape_word_meaning(word, driver, retries=3):
    base_url = f"https://www.dictionary.com/browse/{word}"
    for attempt in range(retries):
        try:
            driver.get(base_url)

            # Wait until the relevant section is loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ol.lpwbZIOD86qFKLHJ2ZfQ.E53FcpmOYsLLXxtj5omt'))
            )
            
            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find the first ol element with the class 'lpwbZIOD86qFKLHJ2ZfQ E53FcpmOYsLLXxtj5omt'
            first_ol = soup.find('ol', class_='lpwbZIOD86qFKLHJ2ZfQ E53FcpmOYsLLXxtj5omt')
            if first_ol:
                # Find the first li element within this ol
                first_li = first_ol.find('li')
                if first_li:
                    # Find the span element within the li
                    span = first_li.find('span', class_='HGU9YJqWX_GVHkeeJhSH')
                    if span:
                        # Find the div with class 'NZKOFkdkcvYgD3lqOIJw'
                        div_nzk = span.find_next('div', class_='NZKOFkdkcvYgD3lqOIJw')
                        if div_nzk:
                            # Find the innermost div and extract text
                            inner_div = div_nzk.find('div')
                            if inner_div:
                                text = inner_div.get_text(strip=True)
                                return text
                            else:
                                print(f"Innermost div not found under div with class 'NZKOFkdkcvYgD3lqOIJw' for {word}")
                                return None
                        else:
                            print(f"Div with class 'NZKOFkdkcvYgD3lqOIJw' not found for {word}")
                            return None
                    else:
                        print(f"Span with class 'HGU9YJqWX_GVHkeeJhSH' not found for {word}")
                        return None
                else:
                    print(f"First 'li' element not found for {word}")
                    return None
            else:
                print(f"Ordered list with class 'lpwbZIOD86qFKLHJ2ZfQ E53FcpmOYsLLXxtj5omt' not found for {word}")
                return None

        except Exception as e:
            print(f"Failed to retrieve data for word: {word} on attempt {attempt + 1}\nError: {e}")
            if attempt < retries - 1:
                delay = random.uniform(5, 10)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"All retries failed for word: {word}")
                return None


# Setup Selenium WebDriver with custom options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')  # Suppress logs
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')

# Path to ChromeDriver for Windows
service = Service(r'C:\Users\USER\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Adjust the path if needed
driver = webdriver.Chrome(service=service, options=chrome_options)

# Get all words from the database
words = get_words_from_db()

# Process each word
for word in words:
    print(f"Scraping meaning for word: {word}")
    meaning = scrape_word_meaning(word, driver)
    
    if meaning:
        # Save to database
        save_word_meaning_to_db(word, meaning)
        print(f"Saved: {word} - {meaning}")
    else:
        print(f"No meaning found for word: {word}")
    
    # Add a delay of 3 to 6 seconds between requests to avoid being blocked
    delay = random.uniform(3, 6)
    print(f"Waiting for {delay:.2f} seconds before the next request...")
    time.sleep(delay)

# Close the browser and database connection
driver.quit()
connection.close()
