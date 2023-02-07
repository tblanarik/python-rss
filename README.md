# python-rss

[![RSS Retrieve and Send Email](https://github.com/tblanarik/python-rss/actions/workflows/build-deploy.yml/badge.svg?branch=main)](https://github.com/tblanarik/python-rss/actions/workflows/build-deploy.yml)

A simple python script to retrieve the last 100 posts on [r/Olympia](https://www.reddit.com/r/olympia) and send them as an email. Driven weekly by a GitHub Action.

The GitHub Action requires 3 [repository secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository):
- `${{ secrets.SENDGRID_API_KEY }}` = an API key from your [SendGrid](https://sendgrid.com/) account
- `${{ secrets.SENDER_EMAIL_ADDRESS }}` = a sender email address, verified by SendGrid
- `${{ secrets.RECIPIENT_EMAIL_ADDRESS }}` = your recipient email address

The email addresses are secrets for privacy purposes.

### Dependencies
- [feedparser](https://github.com/kurtmckee/feedparser)
- [sendgrid](https://github.com/sendgrid/sendgrid-python#readme)