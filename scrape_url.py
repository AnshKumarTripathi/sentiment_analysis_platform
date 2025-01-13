import requests
from bs4 import BeautifulSoup

def scrape_url_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the main content based on common HTML structures
        text = soup.get_text(separator=' ', strip=True)
        
        # Save the fetched text content into a file for debugging
        with open('scraped_content.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        return text
    except Exception as e:
        return f"An error occurred while fetching the URL content: {e}"
