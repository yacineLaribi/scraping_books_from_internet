import requests
import csv

def get_collection_items(collection, start=0, rows=1000):
    url = f"https://archive.org/advancedsearch.php?q=collection:{collection}+AND+mediatype:texts+AND+language:Arabic&fl[]=identifier,title,creator,description,date,cover&rows={rows}&start={start}&output=json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def save_to_csv(items, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Title', 'Identifier', 'Creator', 'Description', 'Published', 'Link', 'Cover Image'])

        for item in items:
            title = item.get('title', 'No title available')
            identifier = item.get('identifier')
            creator = item.get('creator', 'Unknown creator')
            description = item.get('description', 'No description available')
            date = item.get('date', 'No date available')
            link = f"https://archive.org/details/{identifier}"
            cover_image = f"https://archive.org/services/img/{identifier}"  # Using the identifier for the cover image

            writer.writerow([title, identifier, creator, description, date, link, cover_image])

def fetch_all_items(collection):
    all_items = []
    start = 0
    rows = 1000  # Number of results per page

    while True:
        print(f"Fetching items starting from {start}...")
        data = get_collection_items(collection, start=start, rows=rows)

        if not data:
            break

        items = data.get('response', {}).get('docs', [])
        if not items:
            break

        all_items.extend(items)
        start += rows  # Move to the next batch of results

    return all_items

if __name__ == "__main__":
    collection_name = "booksbylanguage_arabic"
    all_items = fetch_all_items(collection_name)

    if all_items:
        print(f"Found {len(all_items)} items in the collection '{collection_name}'.")

        # Save all items to a CSV file
        save_to_csv(all_items, 'books_info_with_images.csv')
        print("Book information has been saved to 'books_info_with_images.csv'.")
