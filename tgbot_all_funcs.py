import threading
from threading import Lock
from time import sleep
from tg_const import BASE_URL, TGAPI, APIKEY
import logging
import requests
import json
import mynewsapi


comm_queue = []
last_upd_id = 688142593

queue_lock = Lock()


def updater():
    global last_upd_id, comm_queue
    while True:
        try:
            update_resp = requests.get(f"{BASE_URL}/getUpdates")
            resp_dict = json.loads(update_resp.text)

            resp_list = resp_dict["result"]
            for itm in resp_list:
                upd_id = itm["update_id"]
                if last_upd_id == 0 or upd_id > last_upd_id:
                    try:
                        usr_text = itm["message"]["text"]
                        chat_id = itm["message"]["from"]["id"]
                    except:
                        try:
                            usr_text = itm["edited_message"]["text"]
                            chat_id = itm["edited_message"]["from"]["id"]
                        except Exception as e:
                            print(e)
                    # Acquiring lock
                    queue_lock.acquire()
                    comm_queue.append((upd_id, chat_id, usr_text))
                    queue_lock.release()  # Lock released
                    last_upd_id = upd_id
        except Exception as e:
            print(f"Error occurred while getting updates: {e}")
        sleep(1)


def sender():
    global last_upd_id, comm_queue
    while True:
        try:
            if comm_queue:
                queue_lock.acquire()
                itm_to_send = comm_queue.pop(0)
                queue_lock.release()

                mssg_upd_id = itm_to_send[0]
                usr_chat_id = itm_to_send[1]
                usr_txt_recvd = itm_to_send[2]

                if usr_txt_recvd == "hello":
                    txt_to_send = "Hiiii... Welcome !!!"
                    threading.Thread(
                        target=send_all_mssg,
                        args=(usr_chat_id, txt_to_send),
                        name=f"sendThread-{mssg_upd_id}",
                    ).start()
                if usr_txt_recvd == "/news":
                    headlines_list = mynewsapi.top_headlines()
                    threading.Thread(
                        target=send_all_mssg,
                        args=(usr_chat_id, *headlines_list),
                        name=f"sendThread-{mssg_upd_id}",
                    ).start()
                if usr_txt_recvd == "/link":
                    url = f"http://127.0.0.1:8000/link?tgid={usr_chat_id}"
                    threading.Thread(
                        target=link_with_blog,
                        args=(usr_chat_id, url),
                        name=f"sendThread-{mssg_upd_id}",
                    ).start()
        except Exception as e:
            print(f"Error occurred while sending replies: {e}")


def send_mssg(chat_id, mssg_to_send):
    try:
        res = requests.post(
            f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={mssg_to_send}"
        )
        # print(f"send Status for {chat_id} = {res}")
        logging.info(f"send Status for {chat_id} = {res}")
    except Exception as e:
        print(f"Error occurred actual send mssg tg bot api: {e}")


def send_all_mssg(chat_id, *args):
    try:
        for headline_to_send in args:
            threading.Thread(
                target=send_mssg, args=(chat_id, headline_to_send), name="MESSAGE_TO_TG"
            ).start()

    except Exception as e:
        print(f"Error while sending: {e}")


def link_with_blog(chat_id, url):
    try:
        res = requests.post(
            f"{BASE_URL}/sendMessage?chat_id={chat_id}&text=like karo idhr se {url}"
        )
        # print(f"send Status for {chat_id} = {res}")
        logging.info(f"send Status for {chat_id} = {res}")
    except Exception as e:
        print(f"Error occurred actual send mssg tg bot api: {e}")
