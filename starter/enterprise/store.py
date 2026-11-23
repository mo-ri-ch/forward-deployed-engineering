"""The lead store behind the staff dashboard. One store now holds leads for every client."""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


class LeadStore:
    def __init__(self, path=os.path.join(HERE, "data", "leads.csv")):
        with open(path, encoding="utf-8") as f:
            self.rows = list(csv.DictReader(f))

    def search(self, user, text):
        """Leads whose name contains `text`, for the signed-in user's screen."""
        return [r for r in self.rows if text.lower() in r["name"].lower()]
