import feedparser
import datetime
import os
import sendgrid
from sendgrid.helpers.mail import *

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

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(os.environ.get('SENDER_EMAIL_ADDRESS'))
to_email = To(os.environ.get('RECIPIENT_EMAIL_ADDRESS'))
subject = "Test Email"
content = Content("text/plain", "Test content")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)