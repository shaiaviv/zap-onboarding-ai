"""
Zap Onboarding AI — Main Pipeline

Simulates an automated onboarding flow triggered when a new client
purchases a website + Dapei Zahav minisite package from Zap Group.

Usage:
    python main.py                          # Uses default demo client
    python main.py https://www.example.com  # Scrape a specific URL
"""

import os
import sys
import json

from scraper import scrape_client, format_scraped_data
from llm import (
    extract_client_card,
    generate_client_card_hebrew,
    generate_welcome_message,
    generate_draft_website,
    generate_draft_minisite,
)
from crm import log_to_crm

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
DEFAULT_URL = "https://www.imazganim.co.il/"


def ensure_output_dirs():
    """Create output directories if they don't exist."""
    os.makedirs(os.path.join(OUTPUT_DIR, "website"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "minisite"), exist_ok=True)


def save_file(path, content):
    """Save content to a file."""
    full_path = os.path.join(OUTPUT_DIR, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: output/{path}")


def run_pipeline(url):
    """Run the full onboarding pipeline for a given client URL."""

    print("\n" + "=" * 60)
    print("  ZAP ONBOARDING AI — Automated Client Onboarding")
    print("=" * 60)
    print(f"\n  Simulating CRM trigger: 'New client purchased package'")
    print(f"  Client URL: {url}")

    ensure_output_dirs()

    # Step 1: Scrape
    print(f"\n{'─' * 60}")
    print("STEP 1: Scanning digital assets")
    print(f"{'─' * 60}")
    scraped = scrape_client(url)
    raw_text = format_scraped_data(scraped)

    # Step 2: Extract Client Card
    print(f"\n{'─' * 60}")
    print("STEP 2: Extracting client data (AI)")
    print(f"{'─' * 60}")
    print("  Calling Claude API for structured extraction...")
    client_card_json = extract_client_card(raw_text)
    save_file("client_card.json", client_card_json)

    # Step 3: Generate readable Client Card in Hebrew
    print("  Generating Hebrew client card summary...")
    client_card_md = generate_client_card_hebrew(client_card_json)
    save_file("client_card.md", client_card_md)

    # Step 4: Generate welcome message
    print(f"\n{'─' * 60}")
    print("STEP 3: Generating onboarding welcome message (AI)")
    print(f"{'─' * 60}")
    print("  Generating personalized welcome message...")
    welcome_msg = generate_welcome_message(client_card_json)
    save_file("welcome_message.md", welcome_msg)

    # Step 5: Generate draft website
    print(f"\n{'─' * 60}")
    print("STEP 4: Generating draft website (AI)")
    print(f"{'─' * 60}")
    print("  Generating 5-page website draft...")
    website_pages = generate_draft_website(client_card_json)
    for filename, html in website_pages.items():
        save_file(f"website/{filename}", html)

    # Step 6: Generate draft Dapei Zahav minisite
    print(f"\n{'─' * 60}")
    print("STEP 5: Generating draft Dapei Zahav minisite (AI)")
    print(f"{'─' * 60}")
    print("  Generating minisite draft...")
    minisite_html = generate_draft_minisite(client_card_json)
    save_file("minisite/minisite.html", minisite_html)

    # Step 7: Log to CRM
    print(f"\n{'─' * 60}")
    print("STEP 6: Logging to CRM")
    print(f"{'─' * 60}")
    log_to_crm(client_card_json, welcome_msg, OUTPUT_DIR)

    # Done
    print(f"\n{'=' * 60}")
    print("  ONBOARDING COMPLETE")
    print(f"{'=' * 60}")
    print(f"\n  All outputs saved to: {OUTPUT_DIR}/")
    print(f"  Files generated:")
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR)
            print(f"    - {rel}")
    print()


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    run_pipeline(url)
