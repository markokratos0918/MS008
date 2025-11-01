import requests
from bs4 import BeautifulSoup
import re

def scrape_events():
    # URL of the website
    url = 'https://commeventshub.onrender.com/'
    
    try:
        # Send GET request to the website
        response = requests.get(url)
        response.raise_for_status()
        
        # Create BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all event links
        event_links = soup.find_all('a', href=re.compile(r'/events/\d+$'))
        
        # Print header
        print("\nUpcoming Events:")
        print("-" * 50)
        
        # Extract and print information from each event
        for link in event_links:
            text = link.text.strip()
            
            # Split the text into components using bullet point as separator
            parts = text.split('•')
            
            if len(parts) >= 2:
                # Extract date and time
                date_time = parts[0].strip()
                
                # Extract title and category
                event_info = parts[1].strip()
                # Split at the last occurrence of the category (MĀORI, PACIFIC, or GENERAL)
                category_match = re.search(r'(MĀORI|PACIFIC|GENERAL)$', event_info)
                if category_match:
                    category = category_match.group(1)
                    title = event_info[:category_match.start()].strip()
                else:
                    category = "Unknown"
                    title = event_info
                
                # Print event details
                print(f"Date & Time: {date_time}")
                print(f"Title: {title}")
                print(f"Category: {category}")
                print("-" * 50)
            
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_events()
