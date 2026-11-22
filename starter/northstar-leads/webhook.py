"""WhatsApp sends each new message here."""
from flask import Blueprint, jsonify, request

import config
import leads

bp = Blueprint("webhook", __name__)


def parse(payload):
    """Pull the phone number, name and text out of WhatsApp's message format."""
    value = payload["entry"][0]["changes"][0]["value"]
    message = value["messages"][0]
    contact = (value.get("contacts") or [{}])[0]
    return {
        "phone": message["from"],
        "name": contact.get("profile", {}).get("name", ""),
        "text": message.get("text", {}).get("body", ""),
    }


@bp.get("/webhook")
def verify():
    """WhatsApp calls this once, to check the web address is really ours."""
    if request.args.get("hub.verify_token") == config.VERIFY_TOKEN and config.VERIFY_TOKEN:
        return request.args.get("hub.challenge", "")
    return "Forbidden", 403


@bp.post("/webhook")
def receive():
    msg = parse(request.get_json())
    result = leads.save_lead(msg)
    return jsonify({"result": result})
