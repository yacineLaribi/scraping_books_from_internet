import asyncio
import aiohttp
import csv

async def fetch_collection_items(session, collection, start=0, rows=1000):
    url = f"https://archive.org/advancedsearch.php?q=collection:{collection}+AND+mediatype:texts+AND+language:Arabic&fl[]=identifier,title,creator,description,date,cover,subject&rows={rows}&start={start}&output=json"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error: {response.status} - {await response.text()}")
            return None

async def fetch_all_items(collection, batch_size=1000):
    all_items = []
    start = 0
    tasks = []

    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Fetching items starting from {start}...")
            tasks.append(fetch_collection_items(session, collection, start=start, rows=batch_size))

            if len(tasks) == 10:  # Limit the number of concurrent requests
                responses = await asyncio.gather(*tasks)
                for data in responses:
                    if data:
                        items = data.get('response', {}).get('docs', [])
                        all_items.extend(items)
                tasks = []

            start += batch_size
            if len(all_items) >= 100000:  # Limit to a reasonable number
                break

    return all_items

def save_to_csv(items, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Title', 'Identifier', 'Creator', 'Description', 'Published', 'Link', 'Cover Image', 'Categories'])

        for item in items:
            title = item.get('title', 'No title available')
            identifier = item.get('identifier')
            creator = item.get('creator', 'Unknown creator')
            description = item.get('description', 'No description available')
            date = item.get('date', 'No date available')
            link = f"https://archive.org/details/{identifier}"
            cover_image = f"https://archive.org/services/img/{identifier}"  # Using the identifier for the cover image
            categories =  item.get('subject', ['No categories available'])

            # Write row to CSV
            writer.writerow([title, identifier, creator, description, date, link, cover_image, categories])

if __name__ == "__main__":
    collection_name = "booksbylanguage_arabic"
    all_items = asyncio.run(fetch_all_items(collection_name))

    if all_items:
        print(f"Found {len(all_items)} items in the collection '{collection_name}'.")
        save_to_csv(all_items, 'books_info_with_images.csv')
        print("Book information has been saved to 'books_info_with_images.csv'.")
