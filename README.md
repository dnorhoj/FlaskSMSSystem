# Flask SMS system

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4c0754ca2ccf4ae58c0fd20547a91043)](https://www.codacy.com/manual/dnorhoj/FlaskSMSSystem?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dnorhoj/FlaskSMSSystem&amp;utm_campaign=Badge_Grade)

## What is this

This is a project I made for fun to send text messages through the [Messagebird](https://messagebird.com/en/).
It's a webserver made in Python [Flask](https://palletsprojects.com/p/flask/).

I did not make this app for other people to use. This is just for some code examples or whatever you want it to be. You're welcome to contribute but I don't ask for it, or expect it.

## Setup

To set this script up you need python3, pip and pipenv.
To install the requirements with pipenv, run `pipenv install`

You also need install redis server.

Then you need to create a `.env` which contains the secret information like API keys and the redis url.

```sh
MESSAGEBIRD="API_Key" # Messagebird API key
ADMIN_PASS="Password for admin user" # Basic Auth pass for /admin/*
REDIS_URL="redis://redis123" # Redis url for data storage
```
