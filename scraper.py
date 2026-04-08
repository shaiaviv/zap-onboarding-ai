"""
Scraper module — collects raw text from a client's digital assets.

Two modes:
  1. Direct URL: scrape_client(url) — crawls a known URL + its internal pages
  2. Discovery:  discover_assets(name, phone, location) → scrape_multiple(urls)
                 Searches the web for the client's digital footprint, cross-verifies
                 each result by checking the phone number actually appears on the page.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ddgs import DDGS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}
TIMEOUT = 10

# Domains to skip — not useful content sources
SKIP_DOMAINS = {
    "google.com", "google.co.il", "facebook.com", "instagram.com",
    "twitter.com", "x.com", "linkedin.com", "youtube.com",
    "wikipedia.org", "waze.com", "apple.com",
}


# ─── Core scraping ───────────────────────────────────────────────────────────

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


# ─── Discovery mode ──────────────────────────────────────────────────────────

def _phone_variants(phone):
    """Return several normalised forms of a phone number for matching."""
    digits_only = re.sub(r"\D", "", phone)
    # e.g. 0723977065 → also try 072-3977065, 072 3977065
    with_dash = re.sub(r"(\d{3})(\d+)", r"\1-\2", digits_only)
    return {phone, digits_only, with_dash, digits_only[1:]}  # strip leading 0 too


def discover_assets(business_name, phone, location):
    """
    Given a business name, phone number, and location, search DuckDuckGo
    for URLs that belong to this client.

    Each candidate URL is cross-verified: we scrape it and confirm the
    phone number actually appears in the page text. This prevents false
    positives (e.g., a different person with the same first name).

    Returns a list of verified URLs.
    """
    print(f"\n{'='*60}")
    print(f"Discovering assets for: {business_name} | {phone} | {location}")
    print(f"{'='*60}\n")

    variants = _phone_variants(phone)

    # Phone-first query works best for Israeli businesses — DuckDuckGo indexes Hebrew
    # sites well when the phone number anchors the search.
    # Avoid quoting the phone number alone — it confuses non-Israeli number lookup engines.
    queries = [
        f"{phone} מזגנים",                            # phone + category (most reliable)
        f"{phone} {business_name}",                    # phone + name
        f"{business_name} {location}",                 # name + location (no phone)
        f"{business_name} site:d.co.il OR site:b144.co.il OR site:facebook.com",
    ]

    candidate_urls = set()
    print("[1/2] Searching the web...")
    with DDGS() as ddgs:
        for query in queries:
            try:
                results = ddgs.text(query, max_results=6)
                for r in results:
                    url = r.get("href", "")
                    domain = urlparse(url).netloc.replace("www.", "")
                    # Skip social networks and other non-scrapeable domains
                    if not any(skip in domain for skip in SKIP_DOMAINS):
                        candidate_urls.add(url)
                        print(f"  Found candidate: {url}")
            except Exception as e:
                print(f"  [Search error for '{query}': {e}]")

    print(f"\n[2/2] Cross-verifying {len(candidate_urls)} candidates (checking phone: {phone})...")
    verified = []
    for url in candidate_urls:
        text = scrape_url(url)
        if text.startswith("[ERROR"):
            print(f"  ✗ Unreachable: {url}")
            continue
        # Check if any phone variant appears in the page
        if any(v in text for v in variants):
            verified.append(url)
            print(f"  ✓ Verified: {url}")
        else:
            print(f"  ✗ Phone not found — skipped: {url}")

    print(f"\nDiscovery complete: {len(verified)} verified assets found")
    return verified


# ─── Scraping orchestration ──────────────────────────────────────────────────

def scrape_client(base_url):
    """
    Full scrape of a client's digital presence given a known URL.
    Discovers and scrapes all internal pages + satellite sites.
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

    # 3. Placeholder for Israeli directory lookups
    print(f"\n[3/3] Checking Israeli directories...")

    print(f"\nScraping complete: {len(results)} sources, {sum(len(v) for v in results.values())} total chars")
    return results


def scrape_multiple(urls):
    """
    Scrape a list of URLs (used after discovery mode).
    For each URL, also crawls its internal pages.
    Returns a dict of {source_name: text_content}.
    """
    print(f"\n{'='*60}")
    print(f"Scraping {len(urls)} discovered assets")
    print(f"{'='*60}\n")

    results = {}

    for base_url in urls:
        print(f"\n── {base_url}")
        homepage_text = scrape_url(base_url)
        if homepage_text.startswith("[ERROR"):
            print(f"  Skipped (error)")
            continue

        results[f"{base_url} (homepage)"] = homepage_text
        print(f"  Homepage: {len(homepage_text)} chars")

        # Crawl internal pages only for the client's own domain
        # (not for directory listings which have thousands of links)
        domain = urlparse(base_url).netloc
        if not any(d in domain for d in ["d.co.il", "b144", "yad2", "facebook"]):
            internal = discover_internal_pages(base_url)
            for page_url in internal:
                text = scrape_url(page_url)
                if not text.startswith("[ERROR"):
                    results[page_url] = text
                    print(f"  {page_url}: {len(text)} chars")

    total_chars = sum(len(v) for v in results.values())
    print(f"\nScraping complete: {len(results)} sources, {total_chars} total chars")
    return results


def format_scraped_data(results):
    """Format scraped results into a single text blob for LLM consumption."""
    sections = []
    for source, text in results.items():
        sections.append(f"=== Source: {source} ===\n{text}")
    return "\n\n".join(sections)


# ─── CLI demo ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Demo: discovery mode
    urls = discover_assets(
        business_name="יגאל מזגנים",
        phone="072-3977065",
        location="קריות",
    )
    print("\nVerified URLs:")
    for u in urls:
        print(f"  {u}")
