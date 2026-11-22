# northstar-leads

Saves WhatsApp enquiries to the lead sheet.

Written by Kevin (IT, Northstar Skills). Northstar is a fictional client from the
[Forward Deployed Engineering](https://gradlabs.in/learn/fde/) course: every name, number and message here is made up.

## How it works

WhatsApp sends each new message to `/webhook`. The code pulls out the phone number,
name and text, checks whether that phone number is already in the lead sheet, and
either updates the existing lead or adds a new row.

| File | What it does |
| --- | --- |
| `app.py` | Starts the web server |
| `webhook.py` | Receives messages from WhatsApp |
| `leads.py` | Tidies the data and decides if a lead is new |
| `sheets.py` | Reads and writes the lead sheet |
| `config.py` | Settings, read from environment variables |
| `leads.csv` | A copy of the lead sheet |

In production the lead sheet is a Google Sheet. Here it's `leads.csv`, with the same columns,
so you can run everything on your own computer or in Colab.

## Run it

```
pip install flask pytest
python -m pytest -q      # run the tests
python app.py            # start the server on port 8000
```
