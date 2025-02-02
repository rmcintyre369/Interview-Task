import requests
import csv
from requests.exceptions import RequestException

# Variables for testing
# URL = "https://raw.githubusercontent.com/dk-books/tech-interview/refs/heads/main/ae/books.json"
# CATEGORIES = {}
# YEAR = 2020
# PRICE_INCREASE_FACTOR = 1.2
# OUTPUT_FILE = 'test2.csv'

def json_reader(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return []

def book_category_filter(books, categories):
    changed_books = []
    if not categories:
        return books
    try:
        for book in books:
                if any(category in book['categories'] for category in categories):
                    changed_books.append(book)
    except (KeyError, ValueError) as e:
        print(f"Error processing book data: {e}")
        return []
    return changed_books

def book_year_filter(books, year):
    if not year:
        return books
    changed_books = []
    for book in books:
        publicationYear = int(book['publication_date'].split('-')[0])
        if publicationYear >= year:
            changed_books.append(book)
    return changed_books

def price_changer(books, price_increase_factor):
    for book in books:
        book['price'] = round(book['price'] * price_increase_factor, 2)
    return books

def csv_writer(books, output_file):
    if not books:
        print("No books to write to CSV")
        return     
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = books[0].keys()
            writer.writerow(header)
            for book in books:
                writer.writerow(book.values())
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_user_input():
    url = input("Enter the URL for the JSON file: ")
    categories_input = input("Enter book categories (comma-separated) or leave empty for all categories: ")
    categories = [cat.strip() for cat in categories_input.split(',')] if categories_input else []
    while True:
        try:
            year_input = input("Enter minimum publication year or leave empty for all years: ")
            year = int(year_input) if year_input else None
            break
        except ValueError:
            print("Please enter a valid year")
    while True:
        try:
            price_factor = float(input("Enter price increase factor (e.g. 1.2 for 20% increase) or enter 1 to keep the original price: "))
            if price_factor <= 0:
                print("Price factor must be positive")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    output_file = input("Enter output CSV filename (e.g. books.csv): ")
    return url, categories, year, price_factor, output_file


if __name__ == "__main__":
    url, categories, year, price_factor, output_file = get_user_input()
    books = json_reader(url)
    filtered_category_books = book_category_filter(books, categories)
    filtered_year_books = book_year_filter(filtered_category_books, year)
    changed_books = price_changer(filtered_year_books, price_factor)
    csv_writer(changed_books, output_file)

