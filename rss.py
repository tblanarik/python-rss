import sys
from datetime import datetime, timezone
import feedparser
import sendgrid


def time_filter(date_string, days=7):
    parsed_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    delta = datetime.now(timezone.utc) - parsed_date
    return delta.days <= days

def make_html_link(entry):
    return f'<a href="{entry.link}">{entry.title}</a>'

def make_page(entries):
    html = []
    html.append('<html><body><h1>r/Olympia</h1><br><ul>')
    html.extend([f'<li>{make_html_link(entry)}</li>' for entry in entries])
    html.append(f'</ul></body></html>')
    return ''.join(html)

def generate_email_data(RECIPIENT_EMAIL_ADDRESS, SENDER_EMAIL_ADDRESS, content):
  return {
    "personalizations": [
      {
        "to": [
          {
            "email": RECIPIENT_EMAIL_ADDRESS
          }
        ],
        "subject": f'Weekly r/Olympia Digest - {datetime.now(timezone.utc).strftime("%Y-%m-%d")}'
      }
    ],
    "from": {
      "email": SENDER_EMAIL_ADDRESS
    },
    "content": [
      {
        "type": "text/html",
        "value": content
      }
    ]
  }

if __name__ == "__main__":
  SENDGRID_API_KEY = sys.argv[1]
  SENDER_EMAIL_ADDRESS = sys.argv[2]
  RECIPIENT_EMAIL_ADDRESS = sys.argv[3]

  NewsFeed = feedparser.parse("https://reddit.com/r/olympia/hot/.rss?limit=100")
  entries = [entry for entry in NewsFeed.entries if time_filter(entry.published)]
  sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
  response = sg.client.mail.send.post(request_body=generate_email_data(RECIPIENT_EMAIL_ADDRESS, SENDER_EMAIL_ADDRESS, make_page(entries)))
  print("Sendgrid status code:", response.status_code)