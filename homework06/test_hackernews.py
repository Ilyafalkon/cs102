import pytest

import hackernews


def test_clear():
    assert hackernews.clean("Something") == "Something"
    assert hackernews.clean("S, o, m, e, t, h, i, n, g") == "S o m e t h i n g"
    assert hackernews.clean("some.thing") == "something"
