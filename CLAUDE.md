# CLAUDE.md — Project Instructions

## What is this project?

This is a prototype for a Zap hiring challenge (GenAI Exploration Lead — junior/graduate role). It demonstrates an AI-powered automation that onboards a new business client by scraping their existing digital assets, extracting structured data, and generating a Client Card + onboarding call script.

**Demo client:** יגאל מזגנים (Yigal Air Conditioning) — a real AC technician in the Krayot area of Israel with an existing website at `imazganim.co.il` but no Dapei Zahav minisite or Zap-built website. He represents a new client who just bought a Zap package.

## The Journal

`journal.md` is the decision log for this project. It is a running, timestamped record of every major decision, thought process, and discovery made during development.

**Rules for the journal:**
- Every meaningful decision gets its own timestamped entry (by time, not by date — this is a single-session project)
- Write in narrative form — capture what we considered, what we tried, what went wrong, and what we landed on
- Include verification steps and lessons learned, not just outcomes
- Update the journal BEFORE moving on to the next step — it should always reflect the current state of the project

## Verified Digital Assets

These are the confirmed assets belonging to our demo client. Every asset was manually verified by cross-referencing phone number (072-3977065), website URL (imazganim.co.il), and location (Krayot area).

| # | Asset | URL |
|---|-------|-----|
| 1 | Main website | https://www.imazganim.co.il |
| 2 | Google Maps | Search: "יגאל מזגנים קריות" — Address: נעמי שמר 2/34, קריית ביאליק |
| 3 | Yolasite | https://mazganim.yolasite.com |
| 4 | WordPress | https://imazganim.wordpress.com |
| 5 | Prosites.co.il | https://prosites.co.il/UniqueBusiness.asp?ID=15630 |
| 6 | Instagram | https://instagram.com/yigal_mazganim (limited — login required to scrape) |

**Do NOT use these — they belong to different people:**
- Midrag Sp/118444 — different Yigal in central Israel
- pro.co.il business-id-9315 — different Yigal in Tel Aviv
- tovtoda.co.il b=6036 — יגאל בוקובזה in Rishon LeZion
- bakrayot.co.il "יגאל מיזוג אוויר" — different phone number (052-4132559)

## Tech Stack

- **Python 3.10** with virtualenv at `./venv`
- **requests + BeautifulSoup4** — for scraping (NOT Playwright — these are all static HTML pages)
- **anthropic SDK** — for Claude API calls (extraction + generation)
- Activate the venv before running: `source venv/bin/activate`

## Scraping Rules

- Use `requests.get()` + `BeautifulSoup` for all scraping — it's cheap and fast
- Do NOT use Playwright/browser automation unless the page requires JavaScript rendering
- Do NOT use `WebFetch` or Playwright MCP tools for scraping during development — they burn credits unnecessarily
- Run scraping code via `python3` in the Bash tool instead
- Always set a timeout on requests: `requests.get(url, timeout=10)`
- Set a User-Agent header to avoid being blocked

## Code Style

- Keep it simple — this is a ~3 hour prototype, not production code
- Prefer one clear script over multiple abstracted modules
- Comments where the logic isn't obvious, but don't over-document
- Output should be in Hebrew where it makes sense (Client Card, onboarding script) since the end users are Israeli

## Project Structure (target)

```
zap-onboarding-ai/
├── CLAUDE.md              # This file
├── journal.md             # Decision log
├── requirements.txt       # Python dependencies
├── main.py                # Main pipeline script
├── scraper.py             # Scrapes digital assets
├── client_card.py         # Generates structured Client Card via LLM
├── onboarding_script.py   # Generates personalized call script via LLM
├── crm_logger.py          # Simulates CRM logging
├── output/                # Generated output files
│   ├── client_card.json
│   ├── client_card.md
│   └── onboarding_script.md
└── README.md              # Required for submission
```

This structure is a guideline — consolidate into fewer files if it makes more sense during implementation.

## Submission

- Deadline: Thursday, April 9, 2026
- Deliver: GitHub repo (public) + README explaining approach
- The README should explain the thinking, not just the code
