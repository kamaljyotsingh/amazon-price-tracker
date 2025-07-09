import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_amazon_product_details(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Request failed with status: {response.status_code}")
            return "Error fetching product", None

        soup = BeautifulSoup(response.content, "html.parser")

        # Product Title
        title_tag = soup.find(id="productTitle")
        title = title_tag.get_text(strip=True) if title_tag else "Title not found"

        # Price tags
        price_whole_tag = soup.find("span", class_="a-price-whole")
        price_fraction_tag = soup.find("span", class_="a-price-fraction")

        if price_whole_tag:
            price_whole = price_whole_tag.get_text(strip=True).replace(',', '').replace('.', '')
            price_fraction = price_fraction_tag.get_text(strip=True).replace('.', '') if price_fraction_tag else "00"
            price_str = f"{price_whole}.{price_fraction}"
            current_price = float(price_str)
            return title, current_price

        return title, None

    except Exception as e:
        print("Error fetching product:", e)
        return "Error fetching product", None
