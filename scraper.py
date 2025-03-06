import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
import wget

load_dotenv()
IMAGE_DIR = os.getenv('IMAGE_DIR')

class Scraper:
    def __init__(self, page_limit=None, proxy=None):
        self.base_url = "https://dentalstall.com/shop/page/{}/"
        self.page_limit = page_limit
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        os.makedirs(IMAGE_DIR, exist_ok=True)

    # fetching page html data retrying fetching mechanism
    def fetch_page(self, url, max_retries=3, timeout=10):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, proxies=self.proxy, timeout=timeout)
                return response.text
            except requests.exceptions.RequestException:
                time.sleep(2)
        return None

    # Download and save product image using img_url
    def download_image(self, img_url, filename):
        img_path = os.path.join(IMAGE_DIR, filename)
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(img_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        return img_path
    
    # scraping product data
    def scrape(self):
        products = []
        page = 1

        while self.page_limit is None or page <= self.page_limit:
            url = self.base_url.format(page)
            html = self.fetch_page(url)
            if not html:
                raise Exception(f"Failed to fetch page {page}")

            soup = BeautifulSoup(html, "html.parser")
            product_elements = soup.find_all("div", class_="product-inner")

            if not product_elements:
                raise Exception(f"No products found on page {page}")

            for product in product_elements:
                name = product.find("h2", class_='woo-loop-product__title').text.strip()

                price_tag = product.find("span", class_="woocommerce-Price-amount")
                if price_tag:
                    price = float(price_tag.text.strip().replace("₹", "").replace(",", ""))
                else:
                    price = 0.0

                img_tag = product.find("img", class_="attachment-woocommerce_thumbnail")
                if img_tag:
                    img_url = img_tag['data-lazy-src']
                else:
                    img_url = None    

                img_path = self.download_image(img_url, f"{name}.jpg") if img_url else "No image"
                
                products.append({"product_title": name, "product_price": price, "path_to_image": img_path})

            page += 1

        return products
