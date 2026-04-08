"""
LLM module — all Claude API calls for extraction and generation.
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-20250514"


def call_claude(system_prompt, user_prompt, max_tokens=4096):
    """Make a single Claude API call."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


def extract_client_card(scraped_text):
    """Extract structured client data from scraped text. Returns JSON string."""
    system = """You are a data extraction assistant for Zap Group, an Israeli digital services company.
Your job is to extract structured business information from raw scraped website text.
Return ONLY valid JSON — no markdown, no explanation."""

    prompt = f"""Extract all business information from the following scraped data and return a JSON object with these fields:

{{
  "business_name": "Hebrew business name",
  "business_name_english": "English transliteration",
  "owner_name": "if found",
  "phone": "main phone number",
  "email": "if found",
  "address": "full address if found",
  "city": "city name",
  "region": "region/area",
  "services": ["list of services offered"],
  "service_areas": ["list of cities/areas served"],
  "brands": ["brands they work with"],
  "years_experience": "number or description",
  "description": "2-3 sentence Hebrew description of the business",
  "website_url": "their current website",
  "social_media": {{"platform": "url"}},
  "google_rating": "if found",
  "google_reviews_count": "if found",
  "testimonials": ["key customer quotes"],
  "unique_selling_points": ["what makes them stand out"],
  "notes_for_producer": ["observations useful for the Zap producer, e.g. missing digital presence, content gaps"]
}}

SCRAPED DATA:
{scraped_text}"""

    result = call_claude(system, prompt, max_tokens=4096)
    # Clean any markdown wrapping
    if result.startswith("```"):
        result = result.split("\n", 1)[1].rsplit("```", 1)[0]
    return result


def generate_client_card_hebrew(client_card_json):
    """Generate a readable Hebrew Client Card summary from structured data."""
    system = """You are a content writer for Zap Group, an Israeli digital services company.
Write in professional Hebrew. The audience is a Zap producer (account manager) who needs to quickly understand a new client."""

    prompt = f"""Based on the following client data, write a professional Hebrew "כרטיס לקוח" (Client Card) document.

The card should include:
1. A header with the business name and key details
2. A summary section about the business
3. Services and brands
4. Service areas
5. Digital presence status (where they are online, where they're missing)
6. Customer reviews/reputation summary
7. Notes and recommendations for the producer

Format it nicely with Hebrew headers and bullet points.

CLIENT DATA:
{client_card_json}"""

    return call_claude(system, prompt, max_tokens=4096)


def generate_welcome_message(client_card_json):
    """Generate a personalized onboarding welcome message for the client."""
    system = """You are a friendly customer success representative at Zap Group.
Write a warm, professional welcome message in Hebrew.
The message will be sent to a new client who just purchased a website + Dapei Zahav minisite package."""

    prompt = f"""Write a personalized onboarding welcome message (email/WhatsApp) for this new client.

The message should:
1. Welcome them warmly by name/business name
2. Show that we already know about their business (reference specific services they offer)
3. Mention that we've prepared a draft website and Dapei Zahav minisite for them to review
4. Include placeholder links: [LINK_DRAFT_WEBSITE] and [LINK_DRAFT_MINISITE]
5. Explain what to expect in the onboarding process
6. Ask them to confirm key details (hours, phone, any services we might have missed)
7. Sign off from "צוות זאפ דפי זהב"

Keep it concise — no more than 15 lines. Warm but professional.

CLIENT DATA:
{client_card_json}"""

    return call_claude(system, prompt, max_tokens=2048)


DESIGN_SYSTEM_PROMPT = """You are an elite web designer at Zap Group creating a draft website for a new client.
You produce distinctive, production-grade HTML that avoids generic "AI slop" aesthetics.

DESIGN PRINCIPLES:
- Typography: Use Google Fonts — choose distinctive, characterful fonts. NEVER use generic fonts like Arial, Inter, Roboto, or system fonts. Pair a bold display font (e.g., Heebo Black for Hebrew headers) with a refined body font (e.g., Heebo Light/Regular for text). Import via <link> tag from fonts.google.com.
- Color: Commit to a cohesive palette using CSS variables. Use a dominant color with sharp accents — not timid, evenly-distributed colors. For an AC/cooling business, think: deep navy + electric cyan accent + clean whites. Define all colors as CSS custom properties in :root.
- Spatial Composition: Generous negative space. Asymmetric hero sections. Grid-breaking elements where they surprise. Avoid cookie-cutter layouts.
- Motion: Add CSS transitions on hover states. Subtle scroll animations via CSS only. One well-orchestrated page load with staggered reveals (animation-delay) creates delight.
- Backgrounds & Depth: Create atmosphere — gradient meshes, subtle geometric patterns, layered transparencies, or textured backgrounds. Never flat solid white.
- Details: Custom styled buttons (not default), smooth box-shadows with multiple layers, border-radius choices that feel intentional, micro-interactions on interactive elements.

CRITICAL RULES:
- Every page must be a COMPLETE standalone HTML file with all CSS inline in a <style> tag
- RTL direction (dir="rtl" lang="he") — all text in Hebrew
- Mobile responsive with proper media queries
- Navigation bar linking to: index.html, services.html, about.html, areas.html, contact.html
- Footer with business name and phone
- Use ACTUAL client data — never placeholder text like "Lorem ipsum"
- The design should feel like it was crafted by a human designer, not generated by AI"""


def _format_images(images):
    """Format image list into a prompt-friendly block."""
    if not images:
        return ""
    lines = ["REAL IMAGES FROM CLIENT'S SITE (use these URLs directly in <img> tags):"]
    for i, img in enumerate(images, 1):
        lines.append(f'  {i}. <img src="{img["url"]}" alt="{img["alt"]}">')
    return "\n".join(lines)


def generate_draft_website(client_card_json, images=None):
    """Generate a 5-page draft website as HTML files. Returns dict of filename: html_content."""
    pages = {}
    images_block = _format_images(images or [])

    page_specs = {
        "index.html": """Homepage — the most important page. Include:
- A dramatic hero section with the business name, a compelling Hebrew tagline, and a large call-to-action button with the phone number
- A brief "why choose us" section with 3-4 key selling points as icon-style cards
- A testimonial highlight
- If real images are provided, use 1-2 of them in the hero or as background
- The overall feel should be: trustworthy, professional, modern — this is a premium AC service""",

        "services.html": """Services page — showcase all services with visual impact:
- Each service (installation, repair, cleaning, sales, VRF systems) gets its own card/section
- Brief compelling description for each
- If real images are provided, use relevant ones (repair image on repair card, etc.)
- Make it scannable — a client should understand all services in 5 seconds""",

        "about.html": """About page — tell the business story:
- Years of experience prominently displayed (large number)
- The brand story in a compelling layout
- All brands they work with displayed as a logo-style grid (text-based since we don't have images)
- What makes them unique — authorized dealer, original parts only, warranty""",

        "areas.html": """Service areas page — geographic coverage:
- List all cities and areas served
- Organize visually — perhaps as a grid of location cards or a clean list with regional grouping
- Make the coverage area feel impressive and comprehensive""",

        "contact.html": """Contact page — make it easy to reach out:
- Phone number displayed LARGE and prominent
- Address with a placeholder for a map
- Business hours in a clean table/grid
- A styled contact form (non-functional placeholder) with fields: name, phone, email, message
- WhatsApp contact button""",
    }

    for filename, description in page_specs.items():
        prompt = f"""Create this page for a business website:

{description}

Use the client data below for ALL content — real business info only.
{images_block}
Output ONLY the complete HTML file, no explanation.

CLIENT DATA:
{client_card_json}"""

        html = call_claude(DESIGN_SYSTEM_PROMPT, prompt, max_tokens=8192)
        if html.startswith("```"):
            html = html.split("\n", 1)[1].rsplit("```", 1)[0]
        pages[filename] = html
        print(f"  Generated {filename}")

    return pages


def generate_draft_minisite(client_card_json, images=None):
    """Generate a draft Dapei Zahav minisite profile as HTML."""
    images_block = _format_images(images or [])
    system = """You are an elite web designer creating a Dapei Zahav (דפי זהב) minisite listing.
The design should closely match the real d.co.il business listing style — structured, directory-style,
but polished and professional.

DESIGN PRINCIPLES:
- Match Dapei Zahav's visual identity: yellow/gold (#FFD700, #FFC107) accent color with white backgrounds and dark text
- Use Google Fonts — Heebo for Hebrew text (import via <link> tag)
- Clean card-based layout with subtle shadows
- Structured sections with clear visual hierarchy
- Contact buttons should be prominent and styled (green for WhatsApp, blue for phone)
- Mobile responsive
- RTL direction (dir="rtl" lang="he")
- Include a "דפי זהב" branded header bar at the top
- The page should look like it belongs on d.co.il — professional directory aesthetic"""

    prompt = f"""Create an HTML page simulating a Dapei Zahav (דפי זהב) business listing/minisite.

Sections to include (matching real d.co.il format):
1. Header bar with דפי זהב branding (yellow/gold)
2. Business hero: name, category badge, location, availability status
3. Contact bar: phone button, WhatsApp button, "יצירת קשר" button — all prominent
4. "אודות" (About) — business description paragraph
5. "חוות דעת גולשים" (Reviews) — empty state with star rating display and "היה הראשון לדרג!" prompt
6. "גלריה" (Gallery) — use the real client images provided below as <img> tags with object-fit:cover, hover zoom effect, and a caption overlay. Do NOT use placeholder boxes.
7. "על השירות" (Service Details) — service categories and service areas displayed cleanly
8. "שעות פעילות" (Business Hours) — clean schedule display
9. "יצירת קשר" (Contact Form) — styled form with fields: name, email, phone, message + submit button
10. Footer with דפי זהב branding and copyright

Use ACTUAL client data from below — no placeholder text.
{images_block}
Output ONLY the complete HTML file.

CLIENT DATA:
{client_card_json}"""

    html = call_claude(system, prompt, max_tokens=8192)
    if html.startswith("```"):
        html = html.split("\n", 1)[1].rsplit("```", 1)[0]
    return html


if __name__ == "__main__":
    # Quick test — just verify API connection works
    result = call_claude(
        "You are a helpful assistant.",
        "Say 'API connection successful!' in exactly those words.",
        max_tokens=50,
    )
    print(f"API test: {result}")
