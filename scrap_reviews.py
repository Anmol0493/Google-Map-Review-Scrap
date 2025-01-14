from helper_class import *
from selenium_driver import *
import dateparser


class SCRAP_REVIEWS():

    def __init__(self):

        self.helper = Helper()
        
        with open('Scraped_data/scraped_urls.json', 'r', encoding='utf-8') as input_file:
            self.urls = json.load(input_file)

        self.scraped_reviews = []

        if os.path.exists('Scraped_data/Reviews.json'):
            with open('Scraped_data/Reviews.json', 'r', encoding='utf-8') as output_file:
                self.scraped_reviews += json.load(output_file)

        self.done = []

        if os.path.exists('Scraped_data/done_scraped_urls.json'):
            with open('Scraped_data/done_scraped_urls.json', 'r', encoding='utf-8') as done:
                self.done += json.load(done)

        self.selenium_driver = selenium_with_proxy()


    def convert_relative_date(self, relative_date):
        parsed_date = dateparser.parse(relative_date, settings={'PREFER_DATES_FROM': 'past'})
        if parsed_date:
            return parsed_date.strftime('%Y-%m-%d')
    
        return relative_date
    

    def filter_and_update_json(self, raw_data):
        for item in raw_data:
            if "review" in item:
                for review in item["review"]:
                    if "text" in review:
                        # if len(review["text"]) > 99:
                        if item not in self.scraped_reviews:
                            self.scraped_reviews.append(item)
    
    
    def get_reviews(self, url):
        
        ratings = url['total_ratings']
        url = url['url']

        if url not in self.done:
            driver = self.selenium_driver.get_driver()
            driver.maximize_window()
            driver.get(url)
            print(f'{url} , ratings: {ratings}')

            raw_data = []

            try:
                accept_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
                if accept_button:
                    accept_button.click()
            except Exception:
                pass

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'LRkQ2')))

            review_btn = driver.find_elements(By.CSS_SELECTOR, "div.LRkQ2")

            for i in review_btn:
                if 'Reviews' in i.text:
                    i.click()
                    
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'jANrlb')))

            if int(ratings) > 1050:
                counter = 105
            else:
                result = driver.find_element(By.CLASS_NAME, 'jANrlb').find_element(By.CLASS_NAME, 'fontBodySmall').text
                result = result.replace(',', '')
                result = result.split(' ')
                result = result[0].split('\n')
                counter =  int(int(result[0])/10)+1

            scrollable_div = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf")

            print('scrolling started')

            for _ in range(counter+1):
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', scrollable_div)
                time.sleep(3)

            print('scrolling finished')
            
            place = driver.find_element(By.ID, 'searchbox').get_attribute('aria-label')
            avg_rating = self.helper.get_text_from_tag(driver.find_element(By.CSS_SELECTOR, 'div.fontDisplayLarge'))
            review_data = driver.find_elements(By.CSS_SELECTOR, 'div.m6QErb')[-1]
            all_review = review_data.find_elements(By.CSS_SELECTOR, 'div.jftiEf.fontBodyMedium')

            print('scraping reviews')
            
            try:
                for review in all_review:
                    scraped_data = {'place_url': url,'place': place, 'avg_rating': avg_rating, 'name': '', 'rating': '', 'date': '', 'review': [], 'url': ''}

                    try:
                        more_element = review.find_element(By.CSS_SELECTOR, 'button.w8nwRe.kyuRq')
                        more_element.click()
                        time.sleep(1)
                    except Exception:
                        pass

                    try:
                        scraped_data['name'] = self.helper.get_text_from_tag(review.find_element(By.CSS_SELECTOR, 'div.d4r55'))
                    except NoSuchElementException:
                        pass
                    try:
                        scraped_data['rating'] = review.find_element(By.CSS_SELECTOR, 'span.kvMYJc').get_attribute('aria-label')
                    except NoSuchElementException:
                        pass
                    try:
                        scraped_data['date'] = self.convert_relative_date(self.helper.get_text_from_tag(review.find_element(By.CSS_SELECTOR, 'span.rsqaWe')))
                    except NoSuchElementException:
                        pass

                    try:
                        scraped_data['review'] = [{'text': self.helper.get_text_from_tag(review.find_element(By.CSS_SELECTOR, 'span.wiI7pd'))}]
                    except NoSuchElementException:
                        scraped_data['review'] = [{'text': ''}]
                    
                    try:
                        for x in review.find_elements(By.CSS_SELECTOR, 'div.PBK6be'):
                            spans = x.find_elements(By.CSS_SELECTOR, 'span.RfDO5c')
                            if len(spans) == 2:
                                scraped_data['review'].append({self.helper.get_text_from_tag(spans[0]): self.helper.get_text_from_tag(spans[1])})
                            if len(spans) == 1:
                                details = self.helper.get_text_from_tag(spans[0]).split(':')
                                scraped_data['review'].append({details[0].strip(): details[1].strip()})
                    except:
                        pass

                    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.PP3Y3d.S1qRNe')))
                    share_btn = review.find_element(By.CSS_SELECTOR, 'button.PP3Y3d.S1qRNe')
                    time.sleep(0.2)
                    share_btn.click()
                    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.fxNQSd')))
                    share_review = driver.find_element(By.CSS_SELECTOR, 'div.fxNQSd')
                    share_review.click()
                    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.vrsrZe')))
                    scraped_data['url'] = driver.find_element(By.CSS_SELECTOR, 'input.vrsrZe').get_attribute('value')
                    time.sleep(0.2)
                    close_btn = driver.find_element(By.CSS_SELECTOR, 'span.AmPKde')
                    close_btn.click()

                    raw_data.append(scraped_data)
                    time.sleep(1)
                
                driver.quit()
                
                self.filter_and_update_json(raw_data)
                new_len = len(self.scraped_reviews)

                print('Writing Reviews.json')
                
                with open('Scraped_data/Reviews.json', 'w', encoding='utf-8') as output_file:
                    json.dump(self.scraped_reviews, output_file, indent=4)
                
                self.done.append(url)
                with open('Scraped_data/done_scraped_urls.json', 'w', encoding='utf-8') as done:
                    json.dump(self.done, done, indent=4)

                print("Total scraped reviews: ", new_len)
            except Exception:
                print(f'skipping {url}')
                driver.quit()


    def run(self, max_workers=1):
        print(len(self.scraped_reviews))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.get_reviews, self.urls)


if __name__ == '__main__':
    SCRAP_REVIEWS().run()