from dotenv import load_dotenv

load_dotenv()
from tg_const import *
import requests
import json


def get_all_updates():
    while True:
        print(f"{BASE_URL}/getUpdates")
        resp = requests.get(f"{BASE_URL}/getUpdates")
        print(resp)
        resp_dict = json.loads(resp.text)
        resp_list = resp_dict["result"]
        for itm in resp_list:
            text = itm["message"]["text"]
            chat_id = itm["message"]["chat"]["id"]
            if text == "hello":
                send_mssg(chat_id, "Hiiiii... Welcome to this bottttttttt")
            else:
                send_mssg(chat_id, "hehe, Ye kya h !!")


def send_mssg(recipient_id, text_to_send):
    try:
        resp = requests.get(
            f"{BASE_URL}/sendMessage?chat_id={recipient_id}&text={text_to_send}"
        )
    except Exception as e:
        print(f"Error while sending: {e}")


get_all_updates()
