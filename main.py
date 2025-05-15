import requests
from bs4 import BeautifulSoup
import time

def get_google_results(query, num_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36"
    }

    urls = []
    for page in range(num_pages):
        start = page * 10
        url = f"https://www.google.com/search?q={query}&start={start}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Error {response.status_code} on page {page + 1}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.select("div.g"):
            a_tag = g.find("a")
            if a_tag and a_tag['href'].startswith("http"):
                href = a_tag['href']
                if href not in urls:
                    urls.append(href)

        print(f"[+] Page {page + 1}: Found {len(urls)} total links so far.")
        time.sleep(2)  # polite delay to avoid blocking

    return urls

# --- Main Program ---

query_input = input("Enter your Google search query: ").strip()
pages_input = input("How many pages to scrape (each page = 10 results): ").strip()

try:
    num_pages = int(pages_input)
except ValueError:
    print("Invalid page number. Please enter a numeric value.")
    exit(1)

query = query_input.replace(" ", "+")
results = get_google_results(query, num_pages)

print(f"\nTotal {len(results)} URLs found:")
for i, url in enumerate(results, 1):
    print(f"{i}. {url}")
