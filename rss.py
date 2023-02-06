import sys
import os
import datetime
import feedparser
import sendgrid

SENDGRID_API_KEY = sys.argv[1]
SENDER_EMAIL_ADDRESS = sys.argv[2]
RECIPIENT_EMAIL_ADDRESS = sys.argv[3]

DATE_STRING = datetime.datetime.now().strftime("%Y-%m-%d")

NewsFeed = feedparser.parse("https://reddit.com/r/olympia/hot/.rss?limit=100")

def time_filter(entry, days=7):
    date_only = entry.published.split('T')[0]
    delta = datetime.datetime.now() - datetime.datetime.strptime(date_only, '%Y-%m-%d')
    return delta.days <= days

def make_html_link(entry):
    txt = '<a href="{url}">{title}</a>'
    return txt.format(url=entry.link, title=entry.title)

def make_page(entries):
    txt = """<html><body>
    <h1>r/Olympia</h1>
    <br>
    <ul>
    """
    for entry in entries:
        txt += "<li>"
        txt += make_html_link(entry)
        txt += "</li>"
    txt += "</ul></body></html>"
    return txt
entries = [entry for entry in NewsFeed.entries if time_filter(entry)]

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": RECIPIENT_EMAIL_ADDRESS
        }
      ],
      "subject": f'Weekly r/Olympia Digest - {DATE_STRING}'
    }
  ],
  "from": {
    "email": SENDER_EMAIL_ADDRESS
  },
  "content": [
    {
      "type": "text/html",
      "value": make_page(entries)
    }
  ]
}

response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)