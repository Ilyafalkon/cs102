import pathlib
from pprint import pp as pp
from typing import final


def read_file(path: pathlib.Path):
    path = pathlib.Path(path)
    with path.open() as f:
        text = f.read()
    return text


def devide_text_for_dates(text: str):
    text = text[: text.find("END")]
    # finding the end of the text and cutting there
    data = {}
    dates = True
    while dates:
        text = text[text.find("DATES") + 6 :]
        place_of_the_date = text.index("/")
        data[text[:place_of_the_date]] = text[place_of_the_date : text.find("DATES")]
        if text.find("DATES") == -1:
            dates = False
    return data


def rid_of_comments(piece_of_text: str):
    text_without_comments = ""
    comments = True
    while comments:
        text_without_comments += piece_of_text[: piece_of_text.find("--")]
        piece_of_text = piece_of_text[piece_of_text.find("--") :]
        piece_of_text = piece_of_text[piece_of_text.find("\n") :]
        if piece_of_text.find("--") == -1:
            comments = False
    return text_without_comments


def rid_of_symbols(text: str):
    newtext = text.replace("\n", " ")
    return newtext


def parse_ids(text: str):
    ids = []
    keyword = True
    while keyword:
        text = text[text.find(" KEYWORD ") :]
        ids.append(text[text.find(" KEYWORD ") : text.find("/ /")])
        text = text[text.find("/ /") :]
        if text.find(" KEYWORD ") == -1:
            keyword = False
    return ids


def pretty_data(data: dict):
    pretty_data = {}
    for key in data:
        datas = rid_of_comments(data[key])
        datas = rid_of_symbols(datas)
        parsed = parse_ids(datas)
        ids = []
        for id in parsed:
            text = id.replace(" KEYWORD ", "")
            text = text.replace("/", ",")
            text = text.strip()
            ids.append(text)
        pretty_data[key] = ids
    return pretty_data


def final_fun(dict):
    ids = {}
    new_dict = {}
    for key in dict:
        id = dict[key]
        if id == [""]:
            continue
        for i in id:
            i = i.replace("1*", "D1")
            i = i.replace("2*", "D1, D2")
            i = i.replace("3*", "D1, D2, D3")
            i = i.replace("4*", "D1, D2, D3, D4")
            i = i.replace("5*", "D1, D2, D3, D4, D5")
            i = i.replace("6*", "D1, D2, D3, D4, D5, D6")
            i = i.replace("7*", "D1, D2, D3, D4, D5, D6, D7")
            i = i.replace(",", "")
            ids[i.split()[0]] = i.split()[1:]

            for keys in ids:
                a = {}
                b = {}
                if len(ids[keys]) != 7:
                    for i in range(7, len(ids[keys]), 8):
                        a[ids[keys][i]] = ids[keys][i + 1 : i + 8]
                    a[keys] = ids[keys][0:7]
            if a == {}:
                new_dict[key] = ids
            else:
                new_dict[key] = a
            ids = {}
    return new_dict


if __name__ == "__main__":
    path = pathlib.Path("text")
    text_to_pars = read_file(path)
    data = devide_text_for_dates(text=text_to_pars)
    pretty = pretty_data(data)
    text = final_fun(pretty)
    pp(text)
