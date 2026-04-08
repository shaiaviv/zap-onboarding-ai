"""
CRM module — simulates logging the onboarding data to a CRM system.
In production this would connect to Salesforce/HubSpot/etc via API.
"""

import json
import os
from datetime import datetime


def log_to_crm(client_card, welcome_message, output_dir):
    """
    Simulate logging everything to a CRM.
    Saves a JSON file representing what would be a CRM entry.
    """
    crm_entry = {
        "crm_id": f"ZAP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "status": "onboarding_initiated",
        "client_data": json.loads(client_card) if isinstance(client_card, str) else client_card,
        "actions_taken": [
            {
                "action": "digital_assets_scanned",
                "timestamp": datetime.now().isoformat(),
                "details": "Automated scan of client's digital presence completed",
            },
            {
                "action": "client_card_generated",
                "timestamp": datetime.now().isoformat(),
                "details": "AI-generated client card created for producer",
            },
            {
                "action": "welcome_message_sent",
                "timestamp": datetime.now().isoformat(),
                "details": "Personalized onboarding message auto-sent to client",
                "channel": "email",
            },
            {
                "action": "draft_website_generated",
                "timestamp": datetime.now().isoformat(),
                "details": "5-page draft website generated for client review",
            },
            {
                "action": "draft_minisite_generated",
                "timestamp": datetime.now().isoformat(),
                "details": "Dapei Zahav minisite draft generated for client review",
            },
        ],
        "welcome_message_preview": welcome_message[:500] + "..." if len(welcome_message) > 500 else welcome_message,
        "deliverables": {
            "client_card": "client_card.json",
            "client_card_readable": "client_card.md",
            "welcome_message": "welcome_message.md",
            "draft_website": "website/",
            "draft_minisite": "minisite/index.html",
        },
    }

    path = os.path.join(output_dir, "crm_log.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(crm_entry, f, ensure_ascii=False, indent=2)

    print(f"\n  CRM entry logged: {crm_entry['crm_id']}")
    print(f"  Status: {crm_entry['status']}")
    print(f"  Actions: {len(crm_entry['actions_taken'])} recorded")
    return crm_entry
