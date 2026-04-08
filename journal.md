# Zap Onboarding AI — Project Journal

---

## 14:00 — Understanding the task

Received the hiring challenge from Zap. The role is GenAI Exploration Lead (junior/graduate). The task asks us to build or describe an AI-based automation for onboarding a new business client — specifically an AC technician in the Krayot area who just bought a 5-page website and a Dapei Zahav minisite from Zap.

The automation needs to:
1. Scan the client's existing digital assets
2. Extract contact details and service categories
3. Generate a "Client Card" for the Zap account manager
4. Generate a personalized onboarding call script, sent to the client and logged in the CRM

Deadline is tomorrow, April 9. Estimated ~3 hours of work. Submission via GitHub (public repo) with a short README.

---

## 14:10 — Deciding on the approach

The task doesn't give us a real client URL — we have to figure out what to scan. We considered three options:

- **Option 1:** Find a real AC technician in the Krayot area with an existing digital presence but no Dapei Zahav listing, and use them as the demo subject
- **Option 2:** Mock the data entirely — create a fake but realistic JSON representing what a scraper would return
- **Option 3:** Both — real scraper with a mock fallback

We chose **Option 1**. A real client makes the demo grounded and impressive. It shows initiative and proves the pipeline works on actual data, not just hypothetical inputs.

---

## 14:15 — First attempt at finding a demo client (Dapei Zahav)

Started by searching `d.co.il` for AC technicians in the Haifa/Krayot area (`טכנאי מזגנים קריות`). Found ~280 listings. Browsed individual profiles by extracting listing IDs from the page snapshot. Found "אלכסיי מיזוג אוויר" in Kiryat Bialik — correct area, phone number available, hours listed. Looked promising at first.

---

## 14:20 — Caught a logic problem with the first candidate

A client already listed on Dapei Zahav can't be a "new" client being onboarded onto Dapei Zahav. The whole point of the automation is to scan their *pre-existing* digital footprint before Zap builds anything for them. Aleksey was already a Zap/Dapei Zahav client — wrong direction entirely.

The digital assets we should be scanning are things like Google Maps, Facebook, or an existing personal website — not a Dapei Zahav listing that Zap hasn't built yet.

---

## 14:25 — Second attempt (Google search → found Yigal)

Searched Google for `טכנאי מזגנים קרית ביאליק` and found several small businesses with their own standalone websites. One immediately stood out: **יגאל מזגנים** at `imazganim.co.il`. Has a real multi-page website with services, brand listings, testimonials, and contact info.

Confirmed via `site:d.co.il` search for "יגאל מזגנים" and "imazganim" — no results for the Krayot area. Yigal has no Dapei Zahav listing and no Zap-built website. He is genuinely the "new client" scenario the task describes.

**Demo client confirmed: יגאל מזגנים**
- Website: https://www.imazganim.co.il
- Phone: 072-3977065
- Location: Krayot area (קריות)
- Services: AC installation, repair, cleaning, sales
- Brands: Electra, Tadiran, LG, Mitsubishi, Whirlpool, Tornado, Family, Elco
- Experience: 15+ years
- On Dapei Zahav: No — perfect new client scenario

The scenario: Yigal just called Zap and bought a package — a new 5-page website + Dapei Zahav minisite. Before the account manager picks up the phone, our automation scrapes `imazganim.co.il`, extracts everything, and delivers a ready Client Card + personalized call script.

---

## 14:30 — Project setup

Created project folder at `/Users/shaiaviv/Projects/zap-onboarding-ai/`. Started this journal to track decisions and thought process as we go.

---

## 14:40 — Verifying Yigal's digital footprint

Before committing to Yigal as our demo client, we ran a full check of his presence across all relevant platforms.

**Zap (zap.co.il):** Searched and found a result called "IMazgan" — but on closer inspection, that business links to `imazgan.co.il` (Tel Aviv), not our `imazganim.co.il`. Completely different business. Yigal is confirmed NOT on Zap. ✅

**Facebook:** Found two pages — a personal profile (`facebook.com/igalsem/`) belonging to someone who "worked at יגאל מזגנים", and a business page (`facebook.com/יגאל-מזגנים-466825966760517`). The business page is marked as an "Unofficial Page", has 0 followers, was created in 2013, and is essentially empty. Not useful for scraping.

**Dapei Zahav:** Already confirmed not listed. ✅

**Google Maps:** Not yet checked — worth doing before fully committing.

**Scrapeable assets so far:**
- `imazganim.co.il` — rich multi-page site, primary source ✅
- Facebook — empty, skip ✗
- Google Maps — TBD

The website alone has services, brands, phone number, location, and customer testimonials — enough to build a solid demo. Will check Google Maps next before starting the build.

---

## 14:45 — Launching parallel subagent searches across all platforms

Decided to find at least 3 scrapeable digital assets beyond the main website. Rather than checking each platform one by one, we launched 8 parallel subagents (AI agents working simultaneously), each searching a different platform:

**First batch (3 agents):**
1. Google Maps — search for Google Business Profile
2. Instagram — search for business account
3. Israeli directories (Midrag, pro.co.il, koneimot, homely) — anything outside Dapei Zahav and Zap

**Second batch (5 more agents, launched after deciding to cast a wider net):**
4. LinkedIn — company page or owner profile
5. Twitter/X — business account
6. Facebook — deeper dig beyond the empty unofficial page we already found
7. YouTube + TikTok — video content
8. Yad2, news, reviews, other Israeli platforms — classifieds and anything else

All 8 ran in parallel while we waited for results to come back.

---

## 14:50 — Results start coming in

**Google Maps agent returned first:**
- Found a Google Business Profile ✅
- Address: נעמי שמר 2/34, קריית ביאליק, 2751401
- Phone: 072-397-7065 (matches)
- Category: שירות תיקונים למזגנים
- Rating: 3.4 stars from 5 reviews (3× five-star, 2× one-star with no text)
- Also surfaced two bonus URLs: `mazganim.yolasite.com` and a listing on `www1.co.il`

**Twitter/X agent:**
- No Twitter/X account found ✗
- But discovered 3 additional web presences: `imazganim.wordpress.com`, `imazganim.weebly.com`, `mazganim.yolasite.com`
- These appear to be old SEO satellite sites Yigal built before his current website

**LinkedIn agent:**
- No LinkedIn found ✗
- But uncovered the owner's full name: **יגאל גימלברג (Yigal Gimelberg)**
- Found references to 35+ years in business (since ~1989)
- Also found listings on `pro.co.il`, `matkinim.co.il`, and `midrag.co.il`

**Instagram agent:**
- Found @yigal_mazganim ✅
- Confirmed it redirects to imazganim.co.il (same business)
- But Instagram blocks unauthenticated scrapers — bio/followers not accessible without login
- Later found it has only 1 post and 2 followers — essentially inactive

**YouTube/TikTok agent:**
- No accounts found on either platform ✗

**Facebook agent:**
- Hit a rate limit, returned nothing useful

**Israeli directories agent:**
- Massive report with 7 platforms found
- Key new find: **prosites.co.il** (ID 15630) — phone 072-3977065 matches, address: קרית חיים הגדוד העברי 14, email: Imazganim@walla.co.il
- Also found: www1.co.il, haifakrayot.co.il, bakrayot.co.il
- And a Dapei Zahav passive listing at d.co.il/80188498/26250 (Kiryat Yam, non-paying, 0 reviews)

**Yad2/other platforms agent:**
- Found Midrag listing with 106 reviews and 9.79/10 score — seemed amazing
- Also confirmed pro.co.il listing is a different person (Tel Aviv area)
- And a tovtoda.co.il listing (yet another different Yigal)

---

## 15:00 — Critical verification step: "Are we sure these are all the same business?"

At this point we had a long list of assets — but a critical question was raised: how do we know all of these actually belong to the same Yigal from the Krayot area?

This turned out to be an essential step. We manually verified each asset by navigating to it and checking for matching identifiers:

**Verification method — cross-referencing these signals:**
- Phone number (072-3977065)
- Website URL (imazganim.co.il)
- Location (Krayot area / Kiryat Bialik)
- Owner name (יגאל גימלברג)

**Yolasite (mazganim.yolasite.com):**
Navigated directly. Found same phone (072-3977065) and links to imazganim.co.il throughout the page. Service areas list all Krayot cities. ✅ Confirmed same business.

**pro.co.il (business-id-9315):**
Navigated directly. Found the listing says "אינו פעיל יותר" (no longer active), location is **Tel Aviv** (not Krayot), and says "repair only — does not do installations" (contradicts imazganim.co.il which lists installation as a core service). ✗ Different person — a namesake in central Israel.

**Midrag (Sp/118444):**
Page returned 404 on direct access. Searched Midrag specifically — all results show this profile serving Rehovot-Yavne-Nes Ziona, Tel Aviv, Ramat Gan — all central Israel. Our Yigal is in the north. ✗ Different person entirely. Despite the agents reporting 106 reviews and 9.79/10 score, this data belongs to someone else.

**bakrayot.co.il:**
Initially thought it was confirmed (redirects to imazganim.co.il). But the directories agent found it shows a different phone (052-4132559) and different email (hubcoils@gmail.com). ⚠️ Uncertain — may be a different "Yigal" in the same area. Removed from verified list.

**prosites.co.il (ID 15630):**
Phone matches (072-3977065), email is Imazganim@walla.co.il, location is Kiryat Haim. ✅ Confirmed same business.

**Dapei Zahav correction:**
The Yad2 agent found a passive listing at d.co.il/80188498/26250 for "יגאל מיזוג אוויר" in Kiryat Yam. It's a non-paying listing with a proxy phone number and 0 reviews. Marked as "העסק שצפית אינו מפרסם באתר" (this business does not advertise on the site). This changes our earlier statement — Yigal IS technically on Dapei Zahav, but only as a passive/unpaid listing. This actually strengthens the demo scenario: he's already there as a ghost listing, and is now buying a real minisite.

**Lesson learned:** When multiple agents return results for a common name like "Yigal," cross-verification against known identifiers (phone, address, website) is critical. At least 3 of the results returned by our agents turned out to be different people entirely.

---

## 15:10 — Final verified asset list

After all 8 agents reported and manual verification was complete:

**✅ Confirmed same business (scrapeable):**

| # | Asset | Key Evidence |
|---|-------|-------------|
| 1 | `imazganim.co.il` | Primary website — services, brands, testimonials, phone |
| 2 | Google Maps | Same phone, links to site. Address: נעמי שמר 2/34, קריית ביאליק |
| 3 | `mazganim.yolasite.com` | Same phone (072-3977065), links to imazganim.co.il |
| 4 | `imazganim.wordpress.com` | Same phone, same domain pattern |
| 5 | `prosites.co.il` (ID 15630) | Same phone, email: Imazganim@walla.co.il, address: קרית חיים |
| 6 | Instagram @yigal_mazganim | Redirects to imazganim.co.il (but scraping limited without login) |

**✗ Not the same business (removed):**
- Midrag Sp/118444 — different Yigal in central Israel
- pro.co.il business-id-9315 — different Yigal, Tel Aviv, repairs only
- tovtoda.co.il — יגאל בוקובזה, Rishon LeZion, different person entirely
- bakrayot.co.il — uncertain, different phone number

**✗ Not found:**
- Twitter/X, LinkedIn, YouTube, TikTok, Yad2, Facebook (useful)

**New info discovered along the way:**
- Owner's full name: יגאל גימלברג (Yigal Gimelberg)
- Email: Imazganim@walla.co.il
- Second address: הגדוד העברי 14, קרית חיים (from prosites.co.il)
- Passive Dapei Zahav listing exists (non-paying, proxy phone, 0 reviews)
- Business has been active since ~1989 (35+ years)

---

## 15:15 — Ready to build

We now have enough verified, scrapeable assets to build a realistic pipeline. The plan is to scrape 3-4 of these sources, feed the content into an LLM, and generate the Client Card + onboarding script.

Next: set up Python project structure and start coding.

---

## 15:20 — Tooling decision: requests + BeautifulSoup over Playwright

The research phase used Playwright (browser automation) heavily for scraping — navigating pages, taking snapshots, reading them. This was extremely expensive in credits because:
- Each page navigation = 1 tool call
- Snapshots returned massive YAML (100K+ characters)
- Subagents used Playwright internally too (one agent made 61 tool calls alone)
- The navigate → snapshot → read cycle is very chatty

For the actual prototype scraper, we decided to use `requests` + `BeautifulSoup` instead:
- One `requests.get(url)` call replaces the entire Playwright cycle
- BeautifulSoup parses HTML directly — no browser rendering needed
- All of Yigal's assets are simple static HTML pages, no JavaScript rendering required

Rule of thumb going forward:
- **Playwright** = JavaScript-heavy SPAs, login walls
- **requests/BeautifulSoup** = everything else (90% of sites)

---

## 15:25 — Python project initialized

Set up virtual environment and installed core dependencies:
- `requests` — lightweight HTTP requests
- `beautifulsoup4` — HTML parsing
- `anthropic` — Claude API for LLM extraction + generation

Quick test confirmed scraping works: `requests.get('https://www.imazganim.co.il/')` returned 200 with 2,470 characters of text in a single call.

Project structure so far:
```
zap-onboarding-ai/
├── journal.md
├── requirements.txt
└── venv/
```

Next: start building the scraper and pipeline.

---

## 15:35 — Adding a draft website to the pipeline

Realized the automation shouldn't just prepare the account manager — it should also prepare something to SHOW the client. The task says the client bought a 5-page website. During the onboarding call, the Zap producer should be able to say: "here's a draft of what we're going to build for you."

So the pipeline now generates a draft 5-page website from the scraped data — auto-generated HTML pages that the producer can present to the client as a preview of their investment. This makes the onboarding call a sales moment, not just a data-gathering call.

The 5 pages:
1. Home — business intro, tagline, hero section
2. Services — installation, repair, cleaning, sales
3. About — 15+ years experience, brands, the story
4. Service Areas — all the Krayot cities + surrounding areas
5. Contact — phone, email, address, contact form placeholder

All content auto-generated from the scraped data using Claude. Output as simple HTML files the producer can open in a browser and show the client.

---

## 15:40 — Remembered the Dapei Zahav minisite

Almost missed this — the task says the client bought TWO products: a 5-page website AND a Dapei Zahav minisite. The automation should draft both. We already know the exact structure of a Dapei Zahav minisite from when we scraped Aleksey's listing earlier (d.co.il/80344605/26250):
- Business name, about section, services, service areas, hours, phone/WhatsApp, gallery, contact form, reviews section.

So the pipeline also generates a draft Dapei Zahav profile — pre-filled with the client's extracted data, ready for the Zap producer to review and publish.

---

## 15:45 — Caught a missing requirement: "sent automatically to the client"

Re-read the original Hebrew task word by word. The task says the onboarding script is "שנשלח אוטומטית ללקוח ומתועד במערכת ה-CRM" — sent automatically to the client AND logged in the CRM. We were only planning to log it.

Discussed what "sent to the client" actually means. The call script itself is internal — it has notes and observations the client shouldn't see. What gets sent to the client is a **separate client-facing welcome message** that includes links to the draft website and Dapei Zahav minisite previews: "here's what we're building for you."

This splits the outputs into two audiences:

**Account manager (internal):**
- Client Card — all extracted data, digital presence map, observations
- Onboarding call script — talking points, what to highlight, what to ask

**Client (auto-sent before the call):**
- Personalized welcome message
- Links to draft website + Dapei Zahav minisite previews
- What to expect on the onboarding call

**Final pipeline:**
1. Scrape digital assets → raw text
2. Client Card (internal) → structured JSON + Hebrew summary for the producer
3. Draft Website → 5-page HTML
4. Draft Dapei Zahav Minisite → structured profile matching d.co.il format
5. Onboarding Script (internal) → talking points + call script for the account manager
6. Client Welcome Message (client-facing) → auto-sent with links to drafts
7. CRM Log → save everything

---

## 15:50 — Full scrape completed → clientinfo.md

Scraped all verified digital assets using `requests` + `BeautifulSoup` and compiled into `clientinfo.md` (30,855 chars, 13 sections):

1. imazganim.co.il — Home
2. imazganim.co.il — Repair page
3. imazganim.co.il — Installation page
4. imazganim.co.il — Cleaning page
5. imazganim.co.il — Sales page
6. imazganim.co.il — Testimonials page
7. imazganim.co.il — Contact page
8. imazganim.co.il — Blog page
9. WordPress (imazganim.wordpress.com)
10. Prosites.co.il (encoding fixed from windows-1255)
11. Google Maps (data extracted during research phase — can't scrape directly with requests)
12. Yolasite (data from research phase — Cloudflare blocked direct scrape)
13. Additional info from research (owner name, email, Instagram, Facebook, Dapei Zahav passive listing)

Two assets required manual data entry from our earlier Playwright research:
- Google Maps: can't scrape with simple requests (requires JS rendering)
- Yolasite: Cloudflare protection returned 403

This is the raw data that will feed into the Claude API for Client Card generation.

Next: build the pipeline scripts.

---

## 16:00 — Revisiting the architecture after cross-referencing with Gemini

Used Gemini to sanity-check our understanding of the task. Its breakdown aligned with ours but highlighted one thing we missed: **the trigger**. The automation should simulate starting from a CRM event ("new client purchased a package"), not just a URL we manually provide. The pipeline should be a repeatable script, not a one-time manual demo.

Also simplified the output split. Gemini interpreted the "onboarding script" as the client-facing welcome message (not an internal call script). Re-reading the Hebrew, this makes more sense — "תסריט שיחת Onboarding מותאם אישית שנשלח אוטומטית ללקוח" is something sent TO the client. Dropped the internal call script — the Client Card already gives the producer everything they need.

**Final pipeline (v3):**

```
Input: client name / URL (simulating a CRM trigger)
  → Scrape their digital assets
  → LLM extracts structured Client Card (internal, for the Zap producer)
  → LLM generates onboarding welcome message (client-facing, auto-sent)
  → LLM drafts 5-page website (to show client what Zap will build)
  → LLM drafts Dapei Zahav minisite (to show client their new listing)
  → Everything logged to simulated CRM
Output: Client Card, welcome message, draft website, draft minisite, CRM entry
```

This is the version we're building. Python script, repeatable for any new client.

---

## 16:10 — Building the pipeline

Built 4 files:

**scraper.py** — Takes a URL, auto-discovers all internal pages, scrapes them all, also checks for satellite sites (WordPress, Weebly) automatically. Tested on imazganim.co.il: found 14 sources, 40K chars. No AI needed for this step.

**llm.py** — All Claude API calls in one place. 5 functions:
- `extract_client_card()` — raw text → structured JSON
- `generate_client_card_hebrew()` — JSON → readable Hebrew summary
- `generate_welcome_message()` — JSON → client-facing onboarding message
- `generate_draft_website()` — JSON → 5 HTML pages
- `generate_draft_minisite()` — JSON → Dapei Zahav profile HTML

**crm.py** — Simulates CRM logging. Creates a JSON entry with all actions taken, timestamps, and links to deliverables.

**main.py** — The orchestrator. Runs the full pipeline in 6 steps:
1. Scrape → 2. Extract Client Card → 3. Generate welcome message → 4. Draft website → 5. Draft minisite → 6. CRM log

Can be run with `python main.py` (uses demo client) or `python main.py https://any-url.com` (any client).

API key set up via .env file, verified working.

---

## 16:30 — Full pipeline ran successfully end-to-end

Ran `python main.py` with `imazganim.co.il` as input. Full pipeline completed in ~3 minutes:
- 14 sources scraped, 40,340 chars
- Claude extracted structured `client_card.json` with all fields populated
- Hebrew `client_card.md` generated for the producer
- Personalized welcome message generated in Hebrew
- 5-page draft website generated (index, services, about, areas, contact)
- Dapei Zahav minisite generated
- CRM entry logged as `ZAP-20260408131050`

All outputs saved to `output/`. The automation works end-to-end with zero manual steps after running the script.

---

## 16:40 — Added asset discovery mode (Step 2 gap fix)

Realized the pipeline required a URL as input — but a real CRM trigger would only have the client's name, phone, and category. The task says "סורקת את הנכסים הדיגיטליים השונים של הלקוח" (scans the various digital assets) — implying the system should find them, not receive them.

Added `discover_assets(name, phone, location)` to `scraper.py`:
- Searches DuckDuckGo with 4 targeted queries (phone-first works best for Israeli sites)
- Collects candidate URLs from search results
- **Cross-verifies each URL** by scraping it and checking the phone number appears on the page
- Returns only verified URLs belonging to the right business

Cross-verification is essential — there are multiple "Yigal" AC technicians in Israel. The phone number is the unique identifier. In a test run, the system correctly found `imazganim.co.il` and `prosites.co.il`, and correctly rejected `bakrayot.co.il` (different Yigal, different phone) automatically.

Now two run modes:
```
python main.py --name "יגאל מזגנים" --phone "072-3977065" --location "קריות"  # discovery
python main.py --url https://www.imazganim.co.il/                               # direct
```

Added `ddgs` (DuckDuckGo search library) to dependencies.

---

## 16:50 — Deployed live demos to Vercel

Deployed the generated HTML output to Vercel so interviewers can click and see real results:

- **Draft website:** https://yigal-mazganim.vercel.app
- **Dapei Zahav minisite:** https://yigal-dapei-zahav.vercel.app

These are the actual AI-generated outputs from running the pipeline against Yigal's real website. The interviewer can navigate the full 5-page site and see the minisite listing.

Fix applied: Vercel serves `index.html` by default — renamed `minisite.html` to `index.html` in the minisite deployment folder.

---

## 16:20 — Embedding frontend design principles into LLM prompts

First pipeline run produced functional but generic-looking HTML. Asked whether we could use Claude Code's `/frontend-design` skill to improve the output. The skill is a Claude Code feature (injected into the system prompt) — it can't be used directly via the API.

**Solution:** Read the skill's actual design principles and embedded them directly into the system prompt for `generate_draft_website()` and `generate_draft_minisite()` in `llm.py`.

Key principles embedded:
- Typography: Google Fonts (Heebo for Hebrew), no generic fonts
- Color: Dominant color + sharp accents via CSS variables, not timid palettes
- Spatial composition: Generous negative space, asymmetric layouts, grid-breaking elements
- Motion: CSS transitions, staggered reveal animations
- Backgrounds: Atmosphere and depth, not flat white
- Details: Custom buttons, layered shadows, intentional border-radius

Also enhanced the page-specific prompts — each page now has detailed instructions about layout, visual hierarchy, and what information to emphasize.

Increased max_tokens from 4096 to 8192 for website generation to give the model room for richer HTML.

Regenerating all HTML files to compare quality.
