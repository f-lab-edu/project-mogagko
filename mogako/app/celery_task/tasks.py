import asyncio
import os
import uuid
from typing import List, Dict, Any, Optional

import aiohttp
from dotenv import load_dotenv

from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mogako.db.model.cafe import Cafe

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
def bulk_insert_cafes(cafe_jsons: Dict[str, Any]):
    kakao_cafe_ids = cafe_jsons.keys()
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4",
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    already_exist_kakao_cafe_ids = (
        session.query(Cafe.kakao_cafe_id)
        .filter(Cafe.kakao_cafe_id.in_(kakao_cafe_ids))
        .all()
    )
    print("bulk_insert_cafes")
    already_exist_kakao_cafe_ids = [
        str(kakao_cafe_id[0]) for kakao_cafe_id in already_exist_kakao_cafe_ids
    ]
    objects = [
        Cafe(external_key=str(uuid.uuid4()), **cafe_json)
        for cafe_json in cafe_jsons.values()
        if cafe_json["kakao_cafe_id"] not in already_exist_kakao_cafe_ids
    ]
    session.bulk_save_objects(objects)
    session.commit()
    session.close()


@celery.task(name="parse_responses")
def parse_responses(responses: List[Dict[str, Any]]):
    print("parse_responses")
    cafe_jsons = {}
    next_urls = []
    for response in responses:
        next_url = _parse_next_url(response=response)
        if next_url:
            next_urls.append(next_url)
        cafe_jsons_of_response = _parse_cafe_jsons(response=response)
        cafe_jsons.update(cafe_jsons_of_response)

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


def _parse_cafe_jsons(response: Dict[str, Any]) -> Dict[str, Any]:
    cafe_jsons = {}
    try:
        for cafe in response["documents"]:
            cafe_jsons[cafe["id"]] = {
                "name": cafe["place_name"],
                "address": cafe["address_name"],
                "kakao_cafe_id": cafe["id"],
            }
    except KeyError:
        print(f"KeyError: {response}")
        return {}
    return cafe_jsons
