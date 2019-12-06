# Flask SMS system

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4c0754ca2ccf4ae58c0fd20547a91043)](https://www.codacy.com/manual/dnorhoj/FlaskSMSSystem?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dnorhoj/FlaskSMSSystem&amp;utm_campaign=Badge_Grade)

## What is this

This is a project I made for fun to send text messages through the [messagebird](https://messagebird.com/en/).
It's a webserver made in [flask](https://palletsprojects.com/p/flask/) which is a python library.

It is currently set up to automatically convert the inserted phone number to a danish one.

## Setup

To set this script up you need [python3](https://www.python.org) and pip.
To install the requirements via pip, run `pip install -r requirements.txt`

You also need install redis server.

Then you need to create a `.env` which contains the secret information like API keys and the redis url. You can find these on your plivo dashboard. Example:

```env
AUTH_ID="id123"
MESSAGEBIRD="messagebird_api_key"
REDIS_URL="redis://redis123"
```
