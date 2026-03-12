import requests
from bs4 import BeautifulSoup
import csv
import argparse

parser = argparse.ArgumentParser('Scrape website')

parser.add_argument('date', help='Date of news')
parser.add_argument('filename', help='File name to be exported')
args = parser.parse_args()

# url = "https://news.ycombinator.com/front?day=2026-03-08&p=1"
base_url = "https://news.ycombinator.com/front?day={}&p={}"

with open(f"{args.filename}.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Title", "Link", "Points", "Author", "Age", "Comments"])

    for page in range(1, 3):
        print("Scraping page", page)
        url = base_url.format(args.date, page)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        
        soup = BeautifulSoup(response.text, "html.parser")

        posts = soup.select("tr.athing")
        print("Posts found: ", len(posts))

        for post in posts:
            rank = post.select_one(".rank").text.strip()
            title = post.select_one(".titleline a").text.strip()
            link = post.select_one(".titleline a")["href"]

            subtext = post.find_next_sibling("tr")

            score_tag = subtext.select_one(".score")
            points = score_tag.text if score_tag else "0 points"

            author_tag = subtext.select_one(".hnuser")
            author = author_tag.text if author_tag else "unknown"

            age = subtext.select_one(".age").text

            comments = subtext.select("a")[-1].text

            writer.writerow([rank, title, link, points, author, age, comments])

print(f"CSV file createed: {args.filename}.csv")