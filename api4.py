import requests
import csv

def get_collection_items(collection, rows=1000000000):  # Requesting all items at once
    url = f"https://archive.org/advancedsearch.php?q=collection:{collection}+AND+mediatype:texts+AND+language:Arabic&fl[]=identifier,title,creator,description,date,cover,subject&rows={rows}&output=json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def save_to_csv(items, filename):
    # Writing CSV with utf-8 encoding to properly handle Arabic characters
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Title', 'Identifier', 'Creator', 'Description', 'Published', 'Link', 'Cover Image', 'Categories'])

        for item in items:
            title = item.get('title', 'No title available')
            identifier = item.get('identifier')
            creator = item.get('creator', 'Unknown creator')
            description = item.get('description', 'No description available')
            date = item.get('date', 'No date available')
            link = f"https://archive.org/details/{identifier}"
            cover_image = f"https://archive.org/services/img/{identifier}"
            categories = item.get('subject', [])  # Combine all categories/subjects into a single string

            # Write the row with UTF-8 encoding
            writer.writerow([title, identifier, creator, description, date, link, cover_image, categories])

if __name__ == "__main__":
    collection_name = "booksbylanguage_arabic"

    print(f"Fetching all items from the collection '{collection_name}'...")
    data = get_collection_items(collection_name)

    if data:
        items = data.get('response', {}).get('docs', [])
        print(f"Found {len(items)} items in the collection '{collection_name}'.")

        # Save all items to a CSV file
        save_to_csv(items, 'books_info_with_categories_utf8.csv')
        print("Book information has been saved to 'books_info_with_categories_utf8.csv'.")
