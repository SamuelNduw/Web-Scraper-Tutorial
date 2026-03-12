import requests
from bs4 import BeautifulSoup
import csv
import argparse

url = "http://books.toscrape.com/"

parser = argparse.ArgumentParser(description='Process some files.')

parser.add_argument('filename', help='File to process')
args = parser.parse_args()

print("Fetching the page...")

with open(f"{args.filename}.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["Title", "Price (£)", "Availability", "Rating"])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    print("Books found:", len(books))

    for book in books:
        title = book.select_one("h3 a")["title"]
        price = book.select_one(".price_color").text
        price = price.replace("£", "").replace("Â", "")
        price = float(price)
        availability = book.select_one(".instock").text.strip()
        rating = book.select_one(".star-rating")["class"][1]

        writer.writerow([title, price, availability, rating])

print(f"Successfully scraped data. Books saved in {args.filename}.csv.")