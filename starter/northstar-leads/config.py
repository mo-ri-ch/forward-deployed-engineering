"""Settings. Secrets come from environment variables, never from this file."""
import os

# Where the lead sheet lives. Point this at a copy when you experiment.
LEADS_FILE = os.environ.get("LEADS_FILE", "leads.csv")

# WhatsApp checks this token when it connects to /webhook.
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN", "")
