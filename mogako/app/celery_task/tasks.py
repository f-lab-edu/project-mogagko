import os
from typing import List, Dict, Any, Optional

import aiohttp
from dotenv import load_dotenv

from mogako.app.main import celery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAKAO_LOCAL_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query={}&category_group_code=CE7&page={}"

load_dotenv(os.path.join(BASE_DIR, "..", "..", ".env"))


@celery.task(name="fetch_urls")
async def fetch_urls(urls: List[str]):
    headers = {
        "Authorization": f"KakaoAK {os.environ.get('KAKAO_AK')}",
        "charset": "UTF-8",
    }
    responses = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url, headers=headers) as result:
                response = await result.json()
                response["fetched_url"] = url
                responses.append(response)
    # Publish responses
    parse_responses.delay(responses=responses)


@celery.task(name="bulk_insert_cafes")
def bulk_insert_cafes(cafes: List[Dict[str, Any]]):
    with open("./test.txt", "w") as file:
        file.write(f"length: {len(cafes)}")
        file.write(f"cafes: {cafes}")


@celery.task(name="parse_responses")
def parse_responses(responses: List[Dict[str, Any]]):
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
        fetch_urls.delay(urls=next_urls)

    # Publish cafe_jsons
    if cafe_jsons:
        bulk_insert_cafes.delay(cafe_jsons=cafe_jsons)


def _parse_next_url(response: Dict[str, Any]) -> Optional[str]:
    if not response["meta"]["is_end"]:
        base_url, cur_page = response["fetched_url"].split("page=")
        return f"{base_url}page={str(int(cur_page) + 1)}"
    return None


def _parse_cafe_jsons(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    cafe_jsons = []
    for cafe in response["documents"]:
        cafe_jsons.append(
            {
                "name": cafe["place_name"],
                "address": cafe["address_name"],
            }
        )
    return cafe_jsons
