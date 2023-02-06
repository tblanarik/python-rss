import feedparser
import datetime
import os
import sendgrid

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


sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
print("secret check ", os.getenv('TEST_SECRET'))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": os.getenv('RECIPIENT_EMAIL_ADDRESS')
        }
      ],
      "subject": "Test subject"
    }
  ],
  "from": {
    "email": os.getenv('SENDER_EMAIL_ADDRESS')
  },
  "content": [
    {
      "type": "text/plain",
      "value": "Test content"
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)