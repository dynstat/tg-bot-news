from tg_const import *
from newsapi import NewsApiClient
import os
import json
import aiohttp
import asyncio

# Init
newsapi = NewsApiClient(api_key=APIKEY)


def top_headlines(
    apiKey=APIKEY, country: str = "in", sources: list[str] = ["the-times-of-india"]
):
    headlines_list = []
    top_headlines = newsapi.get_top_headlines(
        sources=sources[0],
        # category="business",
        language="en",
        # country=country,
    )
    # print(json.dumps(top_headlines))
    top_headlines_list = []
    for itm in top_headlines["articles"]:
        # print(itm["title"])
        top_headlines_list.append(itm["title"])
    print(top_headlines_list)
    return top_headlines_list


# async def get_news():
#     titles_list = []
#     async with aiohttp.ClientSession() as session:
#         async with session.get(
#             f"https://newsapi.org/v2/top-headlines?country=in&apiKey={APIKEY}"
#         ) as response:
#             print("Status:", response.status)
#             print("Content-type:", response.headers["content-type"])

#             html = await response.text()
#             html_dict = json.loads(html)
#             for itm in html_dict["articles"]:
#                 titles_list.append(itm["title"])

#             # print("Body:", html[:15], "...")
#             print(titles_list)
#             return titles_list


if __name__ == "__main__":
    # asyncio.run(get_news())
    pass

# top_headlines()
