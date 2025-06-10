import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.investopedia.com/bonds-4689778"  # Modify based on section
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_soup(url):
    """Fetch HTML content and parse with BeautifulSoup"""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    return None

def extract_articles(page_url):
    """Extract all article links from the news page"""
    soup = get_soup(page_url)
    if not soup:
        return [], None

    articles = []
    for link in soup.select("a[href*='/articles/']"):  # Extract only article links
        article_url = link.get("href")
        if article_url.startswith("/"):
            article_url = "https://www.investopedia.com" + article_url
        articles.append(article_url)

    # Find next page link (modify selector if needed)
    next_page = soup.select_one("a.next")  # Adjust selector based on site changes
    next_page_url = next_page["href"] if next_page else None
    if next_page_url and next_page_url.startswith("/"):
        next_page_url = "https://www.investopedia.com" + next_page_url

    return articles, next_page_url

def scrape_article(article_url):
    """Extract details from an article page"""
    soup = get_soup(article_url)
    if not soup:
        return None

    title = soup.select_one("h1").text.strip() if soup.select_one("h1") else "N/A"
    author = soup.select_one(".mntl-attribution__name a")
    author = author.text.strip() if author else "Unknown"
    date = soup.select_one("time")
    date = date["datetime"] if date else "Unknown"

    # Extract all paragraphs in the main content section
    content = " ".join([p.text.strip() for p in soup.select("div.mntl-sc-block p")])

    return {
        "title": title,
        "author": author,
        "published_date": date,
        "content": content,
        "url": article_url,
    }

def scrape_investopedia(pages=3):
    """Scrape multiple pages of Investopedia articles"""
    scraped_data = []
    url = BASE_URL

    for _ in range(pages):
        print(f"Scraping page: {url}")
        articles, next_page = extract_articles(url)
        for article_url in articles:
            print(f"Scraping article: {article_url}")
            data = scrape_article(article_url)
            if data:
                scraped_data.append(data)
            time.sleep(1)  # Avoid hitting server too fast

        if not next_page:
            break  # Stop if there's no next page
        url = next_page

    # Save data to JSON file
    with open("investopedia_articles.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4)

    print("Scraping completed! Data saved to investopedia_articles.json.")

# Run the scraper
scrape_investopedia(pages=3)
