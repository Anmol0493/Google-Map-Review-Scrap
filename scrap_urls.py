from helper_class import *
from selenium_driver import *


class SCRAP_URLS():
    def __init__(self, url):

        self.url = url

        self.helper = Helper()
        self.selenium_driver = selenium_with_proxy()

        self.done = []

        if os.path.exists('done_listing.json'):
            with open('Scraped_data/done_listing.json', 'r', encoding='utf-8') as done:
                self.done += json.load(done)

        self.scraped_urls = []

        if os.path.exists('scraped_urls.json'):
            with open('Scraped_data/scraped_urls.json', 'r', encoding='utf-8') as listing:
                self.scraped_urls += json.load(listing)


    def scrap_urls(self):

        if self.url not in self.done:

            driver = self.selenium_driver.get_driver()
            driver.maximize_window()
            driver.get(self.url)
            print(self.url)
            try:
                accept_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
                if accept_button:
                    accept_button.click()
            except Exception:
                pass

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'id-content-container')))

            scrollable_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')

            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', scrollable_div)

                time.sleep(5)
                
                new_height = driver.execute_script("return arguments[0].scrollTop;", scrollable_div)
                
                if new_height == last_height:
                    break
                last_height = new_height

            # This class can very by keywords
            cards = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.tH5CWc.THOPZb') # Nv2PK.THOPZb.CpccDe & Nv2PK.tH5CWc.THOPZb & Nv2PK.Q2HXcd.THOPZb
            if not cards:
                cards = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb.CpccDe')
            if not cards:
                cards = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.Q2HXcd.THOPZb')

            for card in cards:
                details = {'url': '', 'total_ratings': ''}
                details['url'] = card.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
                try:
                    total_rating = card.find_element(By.CSS_SELECTOR, 'span.UY7F9')
                    if total_rating:
                        details['total_ratings'] = self.helper.get_text_from_tag(total_rating).replace('(', '').replace(')', '').replace(',', '')
                    else:
                        details['total_ratings'] = '0'
                except NoSuchElementException:
                    details['total_ratings'] = '0'

                if int(details['total_ratings']) > 0:
                    if details not in self.scraped_urls:
                        self.scraped_urls.append(details)
            print("Total scraped urls: ", len(self.scraped_urls))

            driver.quit()

            with open('Scraped_data/scraped_urls.json', 'w', encoding='utf-8') as listing:
                json.dump(self.scraped_urls, listing, indent=4)

            self.done.append(self.url)
            with open('Scraped_data/done_listing.json', 'w', encoding='utf-8') as done:
                json.dump(self.done, done, indent=4)


if __name__ == '__main__':
    SCRAP_URLS().scrap_urls()