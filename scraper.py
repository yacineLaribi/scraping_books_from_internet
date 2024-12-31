import requests
from bs4 import BeautifulSoup
import csv
import time

# URL to scrape
url = "https://archive.org/details/booksbylanguage_arabic?and%5B%5D=mediatype%3A%22texts%22"

# Send a GET request to the website
response = requests.get(url)

# Parse the content with Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the container with the books using the ID
container = soup.find_all('.cell-container')
print(container)
if container:
    # Find all the books
    books = container.select('.desktop')
    print(f"Found {len(books)} books")

    # Open a CSV file to store the data
    with open('books_arabic.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Author', 'Link', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for book in books:
            title_tag = book.select_one('.title')  # Adjust the selector as needed
            title = title_tag.text.strip() if title_tag else 'Unknown Title'

            author_tag = book.select_one('.creator')  # Adjust the selector as needed
            author = author_tag.text.strip() if author_tag else 'Unknown Author'

            link = book.find('a')['href']
            full_link = f"https://archive.org{link}"

            description_div = book.select_one('.description-class')  # Adjust the selector as needed
            description = description_div.text.strip() if description_div else 'No description available'

            writer.writerow({
                'Title': title,
                'Author': author,
                'Link': full_link,
                'Description': description
            })

    print("Scraping complete, data saved to books_arabic.csv")
else:
    print("No container found. Please check the page structure or selectors.")
