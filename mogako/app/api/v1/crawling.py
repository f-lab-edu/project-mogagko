import os
from typing import List

import pandas as pd
from fastapi import APIRouter

from mogako.app.celery_task.tasks import fetch_urls, KAKAO_LOCAL_SEARCH_URL

crawling_router = APIRouter()


@crawling_router.get("")
def crawling():
    load_name_list = get_load_name_list_from_excel()
    urls = make_urls_from_load_name_list(load_name_list)
    urls_count_per_worker = 5
    urls_list = list_chunk(urls, urls_count_per_worker)
    worker_count = 5
    for i, urls in enumerate(urls_list):
        fetch_urls.delay(urls=urls)
        if i == worker_count:
            break
    return {
        "total load_name count": f"{len(load_name_list)}",
        "fetch_urls worker count": f"{worker_count}",
        "urls_count_per_worker": f"{urls_count_per_worker}",
    }


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


def make_urls_from_load_name_list(load_name_list: List[str]) -> List[str]:
    road_name_list: List[str] = get_load_name_list_from_excel()
    urls = [
        KAKAO_LOCAL_SEARCH_URL.format(road_name_list[i], 1)
        for i in range(len(road_name_list))
    ]
    return urls


def list_chunk(lst, n):
    return [lst[i : i + n] for i in range(0, len(lst), n)]
