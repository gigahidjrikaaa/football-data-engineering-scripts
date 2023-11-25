from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import logging

logging.basicConfig(level=logging.INFO)

def scrape_premier_league_data():
    # Create a new instance of the Firefox driver
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    try:
        # Go to the webpage
        driver.get("https://understat.com/league/EPL/2023")

        # Find the div element that contains the Premier League data
        div = driver.find_element(By.ID, "league-chemp")

        # Get the HTML content of the div element
        html = div.get_attribute("innerHTML")

        # Log the success of web content scraping
        logging.info("Successfully scraped web content")

        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Extract table headers
        headers = [th.get_text(strip=True) for th in soup.select('table th')]

        # Extract table rows
        rows = []
        for row in soup.select('table tbody tr'):
            rows.append([td.get_text(strip=True) for td in row.select('td')])

        # Write to CSV
        csv_file = 'files/webscraped_table.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(headers)
            # Write rows
            writer.writerows(rows)

        logging.info(f'CSV file "{csv_file}" created successfully.')

    except Exception as e:
        logging.error(f"Error occurred while scraping data: {e}")

    finally:
        # Close the driver
        driver.quit()

# Call the function
if __name__ == "__main__":
    scrape_premier_league_data()