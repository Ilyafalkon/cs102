import pytest

from map import (create_list_with_numbers, find_destination, find_position,
                 make_matrix)


def test_create_list_with_numbers():
    line = create_list_with_numbers("☺.☒.☼☒☺.☒.☼☒☺.☒.☼☒☺.☒.☼☒\n")
    assert line == ["1.0.501.0.501.0.501.0.50"]


def test_find_position():
    grid = "☒☒☒☒☒☒☒\n☒.☒...☒\n☒☒.☒☼☒☒\n☒..☒.☺☒\n☒.☒.☒.☒\n☒.....☒\n☒☒☒☒☒☒☒"
    matrix = make_matrix(create_list_with_numbers(grid))
    assert find_position(matrix) == (3, 5)
