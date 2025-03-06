from scraper import Scraper
from cache import CacheManager
from db.database import JSONDatabase
from html_response_codes import *

db = JSONDatabase()
cache = CacheManager()

# scrape data takes care of all the logic:
# 1. Scaping products' data from dentalstall using scraper class
# 2. saving data cache
# 3. updating db if cache product price mismatches with recently scraped scraped
async def scrape_data(
    page: int,
    proxy: str,
):
    scraper = Scraper(page_limit=page, proxy=proxy)
    try:
        new_products = scraper.scrape()
    except Exception as e:
        print(e)
        return ErrorResponseModel(500, e)
    
    updated_products = []
    for product in new_products:
        cached_price = cache.get_cached_price(product["product_title"])
        if cached_price is None or float(cached_price) != product["product_price"]:
            cache.cache_price(product["product_title"], product["product_price"])
            updated_products.append(product)

    updated_count = db.update_products(updated_products)

    # Notification (console output for now)
    print(f"Products Scraped : {len(new_products)} \nUpdated in DB: {updated_count}")

    return ResponseModel(data = {"total_scraped": len(new_products), "updated_in_db": updated_count},message = "Successfully Scraped!")
