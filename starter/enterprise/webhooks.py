"""Webhooks from Meridian's CRM: it calls your web address when something happens to a lead."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WEBHOOK_SECRET = b"meridian-webhook-demo-secret"   # demo only: the real one is an environment variable


def load():
    with open(os.path.join(HERE, "data", "webhooks.json"), encoding="utf-8") as f:
        return json.load(f)
