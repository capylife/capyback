# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import os

from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

MONGO_HOST = os.getenv("MONGO_IP", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "capybara")

TWITTER_CLIENT_ID = os.environ["TWITTER_CLIENT_ID"]
TWITTER_CLIENT_SECRET = os.environ["TWITTER_CLIENT_SECRET"]

FRONTEND_PROXIED = os.getenv("FRONTEND_PROXIED", "http://localhost:3000")
BACKEND_PROXIED = os.getenv("BACKEND_PROXIED", "http://127.0.0.1:8000")

NANO_ID_LEN = int(os.getenv("NANO_ID_LEN", 21))

SAVE_PATH = os.getenv("SAVE_PATH", "./capybaras")

try:
    os.mkdir(SAVE_PATH)
except Exception:
    pass