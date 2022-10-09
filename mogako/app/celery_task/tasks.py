import asyncio
import os
from typing import List, Dict, Any, Optional

import aiohttp
from dotenv import load_dotenv

from celery import Celery


celery = Celery(
    __name__, broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0"
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAKAO_LOCAL_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query={}&category_group_code=CE7&page={}"

load_dotenv(os.path.join(BASE_DIR, "..", "..", ".env"))


@celery.task(name="fetch_urls")
def fetch_urls(urls: List[str]) -> None:
    print("fetch_urls")
    asyncio.run(afetch_urls(urls))


async def afetch_urls(urls: List[str]):
    responses: List[Dict[str, Any]] = []
    print("afetch_urls")
    async with aiohttp.ClientSession() as session:
        tasks = [afetch_url(session, url, responses) for url in urls]
        await asyncio.gather(*tasks)
    # Publish responses
    parse_responses.delay(responses=responses)


async def afetch_url(session: aiohttp.ClientSession, url: str, responses):
    headers = {
        "Authorization": f"KakaoAK {os.environ.get('KAKAO_AK')}",
        "charset": "UTF-8",
    }
    async with session.get(url, headers=headers) as result:
        try:
            response = await result.json()
            response["fetched_url"] = url
            responses.append(response)
        except aiohttp.ContentTypeError:
            print(f"{result}")


@celery.task(name="bulk_insert_cafes")
def bulk_insert_cafes(cafe_jsons: List[Dict[str, Any]]):
    print("bulk_insert_cafes")
    with open("./test.txt", "a+") as file:
        file.write(f"length: {len(cafe_jsons)}\n")
        file.write(f"cafes: {cafe_jsons}\n")


@celery.task(name="parse_responses")
def parse_responses(responses: List[Dict[str, Any]]):
    print("parse_responses")
    cafe_jsons = []
    next_urls = []
    for response in responses:
        next_url = _parse_next_url(response=response)
        if next_url:
            next_urls.append(next_url)
        cafe_jsons_of_response = _parse_cafe_jsons(response=response)
        cafe_jsons.extend(cafe_jsons_of_response)

    # Publish urls
    if next_urls:
        print("have_next_url")
        fetch_urls.delay(urls=next_urls)

    # Publish cafe_jsons
    if cafe_jsons:
        bulk_insert_cafes.delay(cafe_jsons=cafe_jsons)


def _parse_next_url(response: Dict[str, Any]) -> Optional[str]:
    try:
        if not response["meta"]["is_end"]:
            base_url, cur_page = response["fetched_url"].split("page=")
            return f"{base_url}page={str(int(cur_page) + 1)}"
    except KeyError:
        print(f"KeyError: {response}")
    return None


def _parse_cafe_jsons(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    cafe_jsons = []
    try:
        for cafe in response["documents"]:
            cafe_jsons.append(
                {
                    "name": cafe["place_name"],
                    "address": cafe["address_name"],
                }
            )
    except KeyError:
        print(f"KeyError: {response}")
        return []
    return cafe_jsons
