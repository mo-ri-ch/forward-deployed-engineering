"""A simplified sign-in token, like the ones SSO systems send.

The client's login system writes a short note ("this is priya@meridian, valid until 10:15")
and signs it with a secret key. Your app checks the signature before trusting the note.
Real SSO (OIDC or SAML) uses the same idea with public-key signatures and a proper library.
"""
import base64
import hashlib
import hmac
import json

MERIDIAN_LOGIN_KEY = b"meridian-login-demo-key"   # demo only: real keys live in environment variables


def _b64(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def make_token(claims, key=MERIDIAN_LOGIN_KEY):
    """What the client's login system does. You never write this part in real life."""
    body = _b64(json.dumps(claims, sort_keys=True).encode())
    sig = _b64(hmac.new(key, body.encode(), hashlib.sha256).digest())
    return f"{body}.{sig}"


def read_token(token):
    """Split a token into its claims and signature, without checking anything."""
    body, sig = token.split(".")
    claims = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    return body, sig, claims
