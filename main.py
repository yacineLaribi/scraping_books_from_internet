import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
url = "https://archive.org/details/booksbylanguage_arabic?page=2"

# Send a request to the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the div with id 'container' which holds the book information
container = soup.find('div', id='container')

# Find all article elements with class 'cell-container' inside the container
books = container.find_all('article', class_='cell-container')

# Open a CSV file to store the data
with open('books_arabic.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Author', 'Link', 'Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each book item and extract the details
    for book in books:
        # Get the book title from h4 with class 'truncated'
        title_tag = book.find('h4', class_='truncated')
        title = title_tag.text.strip() if title_tag else 'Unknown Title'

        # Get the author from span with class 'truncated'
        author_tag = book.find('span', class_='truncated')
        author = author_tag.text.strip() if author_tag else 'Unknown Author'

        # Get the book link
        link = book.find('a')['href']
        full_link = f"https://archive.org{link}"

        # Try to get a description if available
        description_div = book.find('div', class_='snippet-archive')
        description = description_div.text.strip() if description_div else 'No description available'

        # Write to the CSV
        writer.writerow({
            'Title': title,
            'Author': author,
            'Link': full_link,
            'Description': description
        })

print("Scraping complete, data saved to books_arabic.csv")
