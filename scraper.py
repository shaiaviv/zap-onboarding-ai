"""
Scraper module — collects raw text from a client's digital assets.
Given a base URL, discovers and scrapes all reachable pages + known platforms.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}
TIMEOUT = 10


def scrape_url(url, encoding=None):
    """Scrape a single URL and return clean text."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        if encoding:
            resp.encoding = encoding
        else:
            resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
    except Exception as e:
        return f"[ERROR scraping {url}: {e}]"


def discover_internal_pages(base_url):
    """Find all internal links on the homepage."""
    try:
        resp = requests.get(base_url, headers=HEADERS, timeout=TIMEOUT)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "html.parser")

        base_domain = urlparse(base_url).netloc
        pages = set()

        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            if parsed.netloc == base_domain and parsed.path not in ("/", ""):
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                pages.add(clean_url)

        return list(pages)
    except Exception as e:
        print(f"  [ERROR discovering pages: {e}]")
        return []


def scrape_client(base_url):
    """
    Full scrape of a client's digital presence.
    Takes a base URL, discovers all pages, scrapes them all.
    Returns a dict of {source_name: text_content}.
    """
    print(f"\n{'='*60}")
    print(f"Scraping client: {base_url}")
    print(f"{'='*60}\n")

    results = {}

    # 1. Scrape main site + all internal pages
    print(f"[1/3] Scraping main website...")
    homepage_text = scrape_url(base_url)
    results[f"{base_url} (homepage)"] = homepage_text
    print(f"  Homepage: {len(homepage_text)} chars")

    internal_pages = discover_internal_pages(base_url)
    print(f"  Found {len(internal_pages)} internal pages")

    for page_url in internal_pages:
        text = scrape_url(page_url)
        if not text.startswith("[ERROR"):
            results[page_url] = text
            print(f"  {page_url}: {len(text)} chars")

    # 2. Try common satellite sites based on domain name
    print(f"\n[2/3] Checking satellite sites...")
    domain_name = urlparse(base_url).netloc.replace("www.", "").split(".")[0]

    satellites = {
        f"WordPress ({domain_name})": f"https://{domain_name}.wordpress.com/",
        f"Weebly ({domain_name})": f"https://{domain_name}.weebly.com/",
    }

    for name, url in satellites.items():
        text = scrape_url(url)
        if not text.startswith("[ERROR"):
            results[name] = text
            print(f"  {name}: {len(text)} chars")
        else:
            print(f"  {name}: not found")

    # 3. Check known Israeli directories
    print(f"\n[3/3] Checking Israeli directories...")
    # Prosites — search by business name from homepage title
    try:
        resp = requests.get(base_url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string if soup.title else ""
    except:
        title = ""

    print(f"\nScraping complete: {len(results)} sources, {sum(len(v) for v in results.values())} total chars")
    return results


def format_scraped_data(results):
    """Format scraped results into a single text blob for LLM consumption."""
    sections = []
    for source, text in results.items():
        sections.append(f"=== Source: {source} ===\n{text}")
    return "\n\n".join(sections)


if __name__ == "__main__":
    # Demo: scrape our test client
    results = scrape_client("https://www.imazganim.co.il/")
    print("\n" + "="*60)
    print("SCRAPED SOURCES:")
    print("="*60)
    for source, text in results.items():
        print(f"  {source}: {len(text)} chars")
