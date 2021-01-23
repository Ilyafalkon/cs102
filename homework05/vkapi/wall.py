import textwrap
import time
import typing as tp
from string import Template

import pandas as pd  # type: ignore
from pandas import json_normalize

from vkapi import config, session  # type: ignore
from vkapi.exceptions import APIError  # type: ignore


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    code = f"""
    var result = [];
        while (i< {max_count}){{
            if ({offset}+i+100 > {count}){{
                result.push(API.wall.get({{
                    "owner_id": "{owner_id}",
                    "domain": "{domain}",
                    "offset": "{offset} + i",
                    "count": "{count} - (i+{offset})",
                    "filter": "{filter}",
                    "extended": "{extended}",
                    "fields": "{fields}"

                }}))
            }}
            result.push(API.wall.get({{
                    "owner_id": "{owner_id}",
                    "domain": "{domain}",
                    "offset": "{offset} + i",
                    "count": "{count}",
                    "filter": "{filter}",
                    "extended": "{extended}",
                    "fields": "{fields}"
        }}))
        }}
        return result;
    """
    data = {"code": code, "access_token": config.VK_CONFIG["access_token"], "v": config.VK_CONFIG}
    response = session.post("execute", data=data)
    if response.ok:
        json = response.json()["response"]
    return json["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    times_for_requests = count / 2500
    if times_for_requests % 1 != 0:
        times_for_requests = int((times_for_requests + 1) // 1)
    if progress is not None:
        progress = progress(range(int(times_for_requests)))
    else:
        progress = range(int(times_for_requests))
    wall = pd.DataFrame()
    for i in progress:
        posts = get_posts_2500(
            owner_id=owner_id,
            domain=domain,
            offset=offset,
            count=count,
            max_count=max_count,
            filter=filter,
            extended=extended,
            fields=fields,
        )
        data = json_normalize(posts)
        wall = wall.append(data)
        time.sleep(1)
    return wall
