import datetime as dt
import statistics
import typing as tp

from dateutil.relativedelta import relativedelta
from vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    ages = []
    friends = get_friends(user_id=user_id, fields=["bdate"]).items
    for friend in friends:
        try:
            friend_bdate = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")
            if friend_bdate is not None:
                delta = relativedelta(dt.datetime.now(), friend_bdate)
                age = delta.years
                ages.append(age)
        except:
            pass
    if ages == []:
        return None
    return statistics.median(ages)
