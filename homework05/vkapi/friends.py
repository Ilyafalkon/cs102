import dataclasses
import math
import time
import typing as tp

from vkapi import config, session  # type: ignore
from vkapi.exceptions import APIError  # type: ignore

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    parameters = {
        "user_id": user_id,
        "count": count,
        "offset": offset,
        "fields": fields,
        "access_token": config.VK_CONFIG["access_token"],
        "v": config.VK_CONFIG["version"],
    }
    response = session.get("friends.get", params=parameters)
    if response.ok:
        json = response.json()
    else:
        raise APIError("HTTPError")
    if "error" in json:
        raise APIError(json["error"]["error_msg"])
    else:
        json = json["response"]
    return FriendsResponse(count=json["count"], items=json["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    if target_uids is None:
        parameters = {
            "source_uid": source_uid,
            "target_uid": target_uid,
            "order": order,
            "count": count,
            "offset": offset,
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
        }
        response = session.get("friends.getMutual", params=parameters)
        if response.ok:
            json = response.json()
        else:
            raise APIError("HTTPError")
        if "error" in json:
            raise APIError(json["error"]["error_msg"])
        else:
            json = json["response"]
        return json

    data = []
    times_for_requests = (len(target_uids) - 1) // 100 + 1
    if progress is not None:
        progress = progress(range(times_for_requests))
    else:
        progress = range(times_for_requests)
    for i in progress:
        parameters = {
            "source_uid": source_uid,
            "target_uids": ",".join([str(element) for element in target_uids]),
            "order": order,
            "count": count,
            "offset": offset + 100 * i,
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
        }
        response = session.get("friends.getMutual", params=parameters)
        if response.ok:
            json = response.json()
        else:
            raise APIError("HTTPError")
        if "error" in json:
            raise APIError(json["error"]["error_msg"])
        else:
            json = json["response"]
        for info in json:
            data.append(
                MutualFriends(
                    id=info["id"],
                    common_friends=info["common_friends"],
                    common_count=info["common_count"],
                )
            )
        time.sleep(0.33)
    return data
