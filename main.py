"""
Zap Onboarding AI — Main Pipeline

Simulates an automated onboarding flow triggered when a new client
purchases a website + Dapei Zahav minisite package from Zap Group.

Usage:
    # Discovery mode — start from business name (simulates a real CRM trigger)
    python main.py --name "יגאל מזגנים" --phone "072-3977065" --location "קריות"

    # Direct URL mode — skip discovery, scrape a known URL
    python main.py --url https://www.imazganim.co.il/

    # No args — runs demo with known URL (fast, for testing)
    python main.py
"""

import os
import sys
import json
import argparse

from scraper import scrape_client, scrape_multiple, discover_assets, format_scraped_data, collect_images
from llm import (
    extract_client_card,
    generate_client_card_hebrew,
    generate_welcome_message,
    generate_draft_website,
    generate_draft_minisite,
)
from crm import log_to_crm

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
DEMO_URL = "https://www.imazganim.co.il/"


def ensure_output_dirs():
    os.makedirs(os.path.join(OUTPUT_DIR, "website"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "minisite"), exist_ok=True)


def save_file(path, content):
    full_path = os.path.join(OUTPUT_DIR, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: output/{path}")


def run_pipeline(scraped_results, base_url=None):
    """
    Core pipeline: takes already-scraped results dict and runs
    extraction → generation → CRM logging.
    Called by both URL mode and discovery mode.
    """
    raw_text = format_scraped_data(scraped_results)

    # Collect real images from the client's site for use in galleries
    images = []
    if base_url:
        print("  Collecting images from client site...")
        images = collect_images(base_url)

    # Step 2: Extract structured Client Card
    print(f"\n{'─' * 60}")
    print("STEP 2: Extracting client data (AI)")
    print(f"{'─' * 60}")
    print("  Calling Claude API for structured extraction...")
    client_card_json = extract_client_card(raw_text)
    save_file("client_card.json", client_card_json)

    print("  Generating Hebrew client card summary...")
    client_card_md = generate_client_card_hebrew(client_card_json)
    save_file("client_card.md", client_card_md)

    # Step 3: Onboarding welcome message
    print(f"\n{'─' * 60}")
    print("STEP 3: Generating onboarding welcome message (AI)")
    print(f"{'─' * 60}")
    print("  Generating personalized welcome message...")
    welcome_msg = generate_welcome_message(client_card_json)
    save_file("welcome_message.md", welcome_msg)

    # Step 4: Draft 5-page website
    print(f"\n{'─' * 60}")
    print("STEP 4: Generating draft website (AI)")
    print(f"{'─' * 60}")
    print("  Generating 5-page website draft...")
    website_pages = generate_draft_website(client_card_json, images)
    for filename, html in website_pages.items():
        save_file(f"website/{filename}", html)

    # Step 5: Draft Dapei Zahav minisite
    print(f"\n{'─' * 60}")
    print("STEP 5: Generating draft Dapei Zahav minisite (AI)")
    print(f"{'─' * 60}")
    print("  Generating minisite draft...")
    minisite_html = generate_draft_minisite(client_card_json, images)
    save_file("minisite/index.html", minisite_html)

    # Step 6: CRM log
    print(f"\n{'─' * 60}")
    print("STEP 6: Logging to CRM")
    print(f"{'─' * 60}")
    log_to_crm(client_card_json, welcome_msg, OUTPUT_DIR)

    # Done
    print(f"\n{'=' * 60}")
    print("  ONBOARDING COMPLETE")
    print(f"{'=' * 60}")
    print(f"\n  All outputs saved to: {OUTPUT_DIR}/")
    print("  Files generated:")
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR)
            print(f"    - {rel}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Zap Onboarding AI Pipeline")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--url", help="Direct URL to scrape (skip discovery)")
    group.add_argument("--name", help="Business name (for discovery mode)")
    parser.add_argument("--phone", help="Business phone number (required with --name)")
    parser.add_argument("--location", help="Business location/city (required with --name)")

    # Also support positional URL for backwards compatibility
    parser.add_argument("positional_url", nargs="?", help=argparse.SUPPRESS)

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  ZAP ONBOARDING AI — Automated Client Onboarding")
    print("=" * 60)

    ensure_output_dirs()

    # ── Step 1: Scrape ────────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print("STEP 1: Scanning digital assets")
    print(f"{'─' * 60}")

    if args.name:
        # Discovery mode — simulates a real CRM trigger with just name+phone+location
        if not args.phone or not args.location:
            print("Error: --name requires --phone and --location")
            sys.exit(1)
        print(f"  Mode: DISCOVERY")
        print(f"  Simulating CRM trigger: 'New client purchased package'")
        print(f"  Client: {args.name} | {args.phone} | {args.location}")
        discovered_urls = discover_assets(args.name, args.phone, args.location)
        if not discovered_urls:
            print("\n  No verified assets found. Check business name / phone.")
            sys.exit(1)
        # Use the first verified URL (most likely the client's own site) for image collection
        base_url = discovered_urls[0]
        scraped = scrape_multiple(discovered_urls)

    else:
        # Direct URL mode
        base_url = args.url or args.positional_url or DEMO_URL
        print(f"  Mode: DIRECT URL")
        print(f"  Simulating CRM trigger: 'New client purchased package'")
        print(f"  Client URL: {base_url}")
        scraped = scrape_client(base_url)

    run_pipeline(scraped, base_url=base_url)


if __name__ == "__main__":
    main()
