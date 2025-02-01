# ToDo refactoring, add aditional features and tests

import requests
import csv

url = "https://raw.githubusercontent.com/dk-books/tech-interview/refs/heads/main/ae/books.json"

def price_changer(url):
    response=requests.get(url)
    books=response.json()
    changed_books=[]
    for book in books:
        if ('Nonfiction' in book['categories']) or ('Hobbies' in book['categories']):
            publicationYear = int(book['publication_date'].split('-')[0])
            if publicationYear >= 2020:
                book['price'] = round(book['price'] * 1.2,2)
                changed_books.append(book)

    return changed_books


def csv_writer(books):
    with open('test.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        header = books[0].keys()
        writer.writerow(header)
        for book in books:
            writer.writerow(book.values())     

if __name__ == "__main__":
    changed_books = price_changer(url)
    csv_writer(changed_books)

    



