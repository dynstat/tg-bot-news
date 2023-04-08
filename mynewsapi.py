from tg_const import *
from newsapi import NewsApiClient
import os
import json

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
    print(json.dumps(top_headlines))
    top_headlines_list = []
    for itm in top_headlines["articles"]:
        # print(itm["title"])
        top_headlines_list.append(itm["title"])
    print(top_headlines_list)
    return top_headlines_list


top_headlines()
