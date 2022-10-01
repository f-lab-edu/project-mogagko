from typing import List

import pandas as pd
import asyncio
import aiohttp
from dotenv import load_dotenv
import os

from mogako.app.entity.cafe import Cafe

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAKAO_LOCAL_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query={}&category_group_code=CE7&page={}"

load_dotenv(os.path.join(BASE_DIR, "..", ".env"))


def get_load_name_list_from_excel() -> List[str]:
    df_sheet_multi = pd.read_excel(
        os.getcwd() + "/../../road_name.xlsx", sheet_name=None
    )
    road_name_list = []
    for key in df_sheet_multi.keys():
        for i in range(len(df_sheet_multi[key]["도로명"])):
            try:
                road_name_list.append(
                    f"{df_sheet_multi[key]['시군구'][i]} {df_sheet_multi[key]['도로명'][i]}"
                )
            except KeyError:
                # 시군구 없는 Case
                road_name_list.append(f"{df_sheet_multi[key]['도로명'][i]}")
    return road_name_list


async def fetch_url(
    session: aiohttp.ClientSession,
    url_queue: asyncio.Queue,
    response_queue: asyncio.Queue,
):
    headers = {
        "Authorization": f"KakaoAK {os.environ.get('KAKAO_AK')}",
        "charset": "UTF-8",
    }

    while not (url_queue.empty() and response_queue.empty()):
        # Subscribe to url_queue
        url = await url_queue.get()

        async with session.get(url, headers=headers) as result:
            data = await result.json()
            # Publish to response_queue
            await response_queue.put((url, data))


async def create_cafe_from_res(
    cafe_list: List[Cafe],
    url_queue: asyncio.Queue,
    response_queue: asyncio.Queue,
):
    await asyncio.sleep(1)
    while not (url_queue.empty() and response_queue.empty()):
        # Subscribe to response_queue
        url, data = await response_queue.get()
        print(url)
        print(data)

        if not data["meta"]["is_end"]:
            base_url, cur_page = url.split("page=")
            next_url = f"{base_url}page={str(int(cur_page) + 1)}"
            await url_queue.put(next_url)
        for document in data["documents"]:
            cafe_list.append(
                Cafe(
                    name=document["place_name"],
                    address=document["address_name"],
                )
            )


async def create_request_task(url_queue: asyncio.Queue, urls: List[str]):
    for url in urls:
        await url_queue.put(url)


async def main():
    cafe_list: List[Cafe] = []
    road_name_list: List[str] = get_load_name_list_from_excel()
    urls = [
        KAKAO_LOCAL_SEARCH_URL.format(road_name_list[i], 1)
        for i in range(len(road_name_list))
    ]

    url_queue = asyncio.Queue()
    response_queue = asyncio.Queue()

    producer = asyncio.create_task(
        (create_request_task(url_queue=url_queue, urls=urls))
    )

    session = aiohttp.ClientSession()
    fetch_tasks = [
        # coroutine to task
        asyncio.create_task(
            fetch_url(
                session=session, url_queue=url_queue, response_queue=response_queue
            )
        )
        for i in range(5)
    ]
    parsing_tasks = [
        # coroutine to task
        asyncio.create_task(
            create_cafe_from_res(
                cafe_list=cafe_list, url_queue=url_queue, response_queue=response_queue
            )
        )
        for i in range(5)
    ]
    await asyncio.gather(producer, *fetch_tasks, *parsing_tasks)
    await session.close()
    breakpoint()


if __name__ == "__main__":
    asyncio.run(main())
