import requests

def get_book_info(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    book_identifier = input("Enter the book identifier (e.g., 'surahalmulkpdf'): ")
    book_info = get_book_info(book_identifier)

    if book_info:
        print("Book Information (Full JSON Response):")
        print(book_info)  # Print the full response to inspect it

        # Example of accessing common fields
        title = book_info.get('metadata', {}).get('title')
        creator = book_info.get('metadata', {}).get('creator')
        description = book_info.get('metadata', {}).get('description')
        published = book_info.get('metadata', {}).get('date')
        identifiers = book_info.get('identifiers', {})

        print("\nExtracted Information:")
        print(f"Title: {title}")
        print(f"Creator: {creator}")
        print(f"Description: {description}")
        print(f"Published: {published}")
        print(f"Identifiers: {identifiers}")
