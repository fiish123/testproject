"""Outbound HTTP and diagnostic clients."""


import requests

from .ops import shell_ping


def fetch_webhook(target_url):
    """Deliver an event to the customer-configured webhook."""
    resp = requests.get(target_url, timeout=5)
    return resp.status_code, resp.text


def run_diagnostic(host):
    """Run a connectivity diagnostic against an operator-chosen host."""
    return shell_ping(host)


def fetch_logo():
    """Fetch the console logo from the internal CDN."""
    return requests.get("https://cdn.internal.local/logo.png", verify=True).content
