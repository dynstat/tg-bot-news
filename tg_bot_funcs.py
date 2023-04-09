from tg_const import BASE_URL, TGAPI, APIKEY

# import requests
import aiohttp
import asyncio
import json
import mynewsapi


last_upd_id = 0


async def read_reply_mssg():
    global last_upd_id
    while True:
        print(f"{BASE_URL}/getUpdates")
        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"{BASE_URL}/getUpdates") as resp:
                all_updates = await resp.text()
                resp_dict = json.loads(all_updates)

        # print(resp)
        # resp_dict = json.loads(resp.text)
        resp_list = resp_dict["result"]
        for itm in resp_list:
            upd_id = itm["update_id"]
            if last_upd_id == 0 or upd_id > last_upd_id:
                text = itm["message"]["text"]
                chat_id = itm["message"]["chat"]["id"]
                if text == "hello":
                    await send_mssg(chat_id, "Hiiiii... Welcome to this bottttttttt")
                    last_upd_id = upd_id
                elif text == "/news":
                    all_titles_list = await mynewsapi.get_news()
                    await send_mssg(chat_id, *all_titles_list)
                    pass
                else:
                    await send_mssg(chat_id, "hehe, Ye kya h !!")
                    last_upd_id = upd_id


async def send_mssg(recipient_id, *args):
    try:
        for text_to_send in args:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    f"{BASE_URL}/sendMessage?chat_id={recipient_id}&text={text_to_send}"
                ) as resp:
                    resp_status = await resp.text()
                    resp_status_dict = json.loads(resp_status)
    except Exception as e:
        print(f"Error while sending: {e}")


async def main():
    # status = asyncio.create_task(read_reply_mssg())
    await read_reply_mssg()
    # asyncio.gather(status)


if __name__ == "__main__":
    # read_reply_mssg()

    asyncio.run(main())
