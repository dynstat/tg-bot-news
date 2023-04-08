import os
from dotenv import load_dotenv

load_dotenv()

# getting the APIKEY from .env
APIKEY = os.getenv("APIKEY")
TGAPI = os.getenv("TGAPI")


# https://api.telegram.org/bot<token>/METHOD_NAME
BASE_URL = f"https://api.telegram.org/bot{TGAPI}"
