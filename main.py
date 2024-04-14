from scrap_urls import SCRAP_URLS
from scrap_reviews import SCRAP_REVIEWS
import json, os
import pandas as pd

class MAIN():

    def __init__(self, url):
        self.url_scraper = SCRAP_URLS(url)

        if not os.path.exists("Scraped_data"):
            os.makedirs("Scraped_data")


    def write_csv(self):
        with open('Scraped_data/Reviews.json', 'r', encoding='utf-8') as json_data:
            data = json.load(json_data)

        df = pd.DataFrame(data)

        def extract_optional_fields(review):
            optional_fields = []
            for item in review:
                key, value = list(item.items())[0]
                optional_fields.append(f"{key}: {value}")
            return ", ".join(optional_fields)
        
        df['Review Text'] = df['review'].apply(lambda review: review[0].get("text", ""))
        df['Optional Fields'] = df['review'].apply(lambda review: extract_optional_fields(review[1:]))
        df['Review Text'] += "  " + df['Optional Fields']

        df.drop(columns=['review', 'Optional Fields'], inplace=True)
        df.rename(columns={'rating': 'Rating', 'date': 'Review Date', 'name': 'Reviewer Name', 'place': 'Place Name',
                        'place_url': 'Place URL', 'url': 'Review URL'}, inplace=True)

        # Write DataFrame to CSV
        df.to_csv('Reviews.csv', index=False, encoding='utf-8')

        print(f"CSV data has been written to Reviews.csv")


    def main(self):
        self.url_scraper.scrap_urls()
        self.review_scraper = SCRAP_REVIEWS()
        self.review_scraper.run()
        
        print('Writing Reviews.csv')
        self.write_csv()


if __name__ == '__main__':

    url="https://www.google.com/maps/search/restaurants/@21.1689004,72.83731,17z/data=!3m1!4b1?entry=ttu"

    MAIN(url).main()