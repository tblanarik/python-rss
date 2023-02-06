import feedparser
import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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


message = Mail(
    from_email=os.environ.get('SENDER_EMAIL_ADDRESS'),
    to_emails=os.environ.get('RECIPIENT_EMAIL_ADDRESS'),
    subject='Test Email',
    html_content=make_page(entries))
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)