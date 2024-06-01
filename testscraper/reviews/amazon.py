import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import uuid

custom_headers = {
    "authority": "www.amazon.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}


def get_soup(url):
    response = requests.get(url, headers=custom_headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        print(response.status_code)
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_reviews(soup):
    review_elements = soup.select("div.review")

    scraped_reviews = []

    for review in review_elements:
        r_author_element = review.select_one("span.a-profile-name")
        r_author = r_author_element.text if r_author_element else None

        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text[:1] if r_rating_element else None

        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one(
            "span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None

        r_date_element = review.select_one("span.review-date")
        r_date = r_date_element.text if r_date_element else None

        r_verified_element = review.select_one("span.a-size-mini")
        r_verified = r_verified_element.text if r_verified_element else None

        r_image_element = review.select_one("img.review-image-tile")
        r_image = r_image_element.attrs["src"] if r_image_element else None

        r = {
            "id": uuid.uuid5(uuid.NAMESPACE_DNS, r_author),
            "author": r_author,
            "score": r_rating,
            "title": r_title,
            "content": r_content,
            "date": r_date,
            "verified": r_verified,
            "image_url": r_image
        }

        scraped_reviews.append(r)

    return scraped_reviews


def main():

    csv_file = "amz.csv"
    counter = 0
    stars = ["one_star", "two_star", "three_star", "four_star", "five_star"]

    for star in stars:

        for i in range(1, 3):
            search_url = f"https://www.amazon.com/product-reviews/B08D67D5WB/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&filterByStar={star}&reviewerType=all_reviews&pageNumber={i}#reviews-filter-bar"
            soup = get_soup(search_url)

            if (soup is None):
                counter += 1

            data = get_reviews(soup)
            df = pd.DataFrame(data=data)

            # Prüfen, ob die Datei bereits existiert, um zu entscheiden, ob Header geschrieben werden soll
            if not os.path.isfile(csv_file):
                df.to_csv(csv_file, index=False, mode='w', encoding='utf-8-sig')
            else:
                df.to_csv(csv_file, index=False, mode='a',
                        header=True, encoding='utf-8-sig')

        print(f"Anzahl an Fehlern: {counter}")


if __name__ == '__main__':
    main()
