Atlys Scraping Tool
A web scraping API built with FastAPI that extracts product information (name, price, and image) from DentalStall and stores it in a local JSON database with caching and proxy support.

Features
- Scrapes product name, price, and image from multiple pages.
- Supports page limit and proxy settings.
- Stores data in a JSON file (extensible to other databases).
- Uses Redis caching to avoid unnecessary updates.
- Implements retry mechanism for failed requests.
- Includes authentication using a static token.
- Provides a health check API to monitor database status.

Project Structure
.
├── app.py                 # FastAPI entry point
├── module/dentalstall_module.py   # API Router for DentalStall scraper
├── crud/dentalstall_crud.py     # Core logic for scraping & updating DB
├── scraper.py             # Scraper class (BeautifulSoup)
├── db/database.py            # JSON-based storage handler
├── cache.py               # Redis caching logic
├── html_response_codes.py  # Response models for API responses
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
└── README.md              # Documentation

Installation & Setup
- Clone the Repository
- git clone https://github.com/yourusername/fastapi-scraper.git
- cd fastapi-scraper

Install Dependencies
- pip install -r requirements.txt

Set Up Environment Variables
- Create a .env file:
DATA_FILE=data/products.json
IMAGE_DIR=data/images
REDIS_HOST=localhost
REDIS_PORT=6379

Start Redis (if not running)
- redis-server

Run the Application
uvicorn app:app --reload
OR
python app.py

📡 API Endpoints
-- Scrape Products
POST /dentalstall/scrape

Parameter
- page	int	Number of pages to scrape
- proxy	str	(Optional) Proxy string


Example Request:
`curl -X 'POST' 'http://127.0.0.1:8080/dentalstall/scrape?page=5' \
  -H 'token: your_static_token'`

-- Check Database Health
GET /health
{"status": "ok", "message": "File is valid"}


How It Works
- FastAPI Router (dentalstall_module.py) receives the request.
- Calls scraper logic (dentalstall_crud.py).
- Uses Scraper class (scraper.py) to extract product details.
- Stores data in JSON database (database.py).
- Uses Redis (cache.py) to avoid redundant updates.
- Logs scraping results and prints status.

Future Improvements
- Support for PostgreSQL / MongoDB storage.
- Webhook/email notifications for scraping results.
- Headless browser integration for JavaScript-heavy pages.