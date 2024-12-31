import requests
import csv

def get_collection_items(collection):
    url = f"https://archive.org/advancedsearch.php?q=collection:{collection}&fl[]=identifier,title,creator,description,date&rows=1000&start=0&output=json"
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
        writer.writerow(['Title', 'Identifier', 'Creator', 'Description', 'Published', 'Link'])
        
        for item in items:
            title = item.get('title', 'No title available')
            identifier = item.get('identifier')
            creator = item.get('creator', 'Unknown creator')
            description = item.get('description', 'No description available')
            date = item.get('date', 'No date available')
            link = f"https://archive.org/details/{identifier}"
            
            writer.writerow([title, identifier, creator, description, date, link])

if __name__ == "__main__":
    collection_name = "booksbylanguage_arabic"
    collection_info = get_collection_items(collection_name)

    if collection_info:
        items = collection_info.get('response', {}).get('docs', [])
        
        print(f"Found {len(items)} items in the collection '{collection_name}'.")
        
        # Save the items to a CSV file
        save_to_csv(items, 'books_info.csv')
        print("Book information has been saved to 'books_info.csv'.")
