# Google Maps Review Scraper

This Python script is designed for scraping reviews from Google Maps listings. It uses Selenium for web automation to extract review data, and you can use it to collect information about reviews from various businesses and locations.

## Prerequisites

Before using this script, ensure that you have the following prerequisites in place:

- **Python**: Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- **Required Libraries**: Install the necessary Python libraries by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory containing the script files.

3. Look for main.py in the directory

4. Edit the `url` variable according to your needs

5. Run the script by executing the following command:

    ```bash
    python main.py
    ```

6. The script will scrape reviews from the specified URLs and save them in the `Reviews.json` and `Reviews.csv` files in the same directory.


## Customization

- **URLs**: Edit the `url` in `main.py` file with the URLs of the Google Maps url you want to scrape.

- **filter_and_update_json**: You can modify the `filter_and_update_json` function in `scrap_reviews.py`. It's objective is to filter reviews according to requirements.

- **Script Behavior**: You can adjust the script to handle errors, logging, and other behaviors according to your specific use case.

- **Multithreading**: The script supports multithreading for faster review scraping. You can configure the number of threads in the `run` method within `scrap_reviews.py`.

## Data Output

- **Reviews.json**: Contains the scraped review data in JSON format.

- **Reviews.csv**: Contains the scraped review data in CSV format for easy analysis and sharing.