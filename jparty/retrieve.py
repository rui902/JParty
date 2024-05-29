import csv
import json
import logging
import re
from html import unescape

import requests
from bs4 import BeautifulSoup
from google.protobuf.json_format import ParseDict

from jparty.constants import MONIES
from jparty.game import Question, Board, FinalBoard, GameData
from jparty.proto import full_pb2 as jpb2


def get_game(game_id: str):
    if len(str(game_id)) < 7:
        try:
            return get_wayback_game(game_id)

        except Exception as e:
            logging.error(e)
            return get_jarchive_game(game_id)

    if game_id.endswith(".json"):
        print(f"Loading Local JSON game: {game_id!r}")

        # Load local JSON game
        with open(game_id, "r") as j_in:
            jdata = json.load(j_in)
            j = ParseDict(jdata, jpb2.GameData())

        game_data = json_to_game(j)
        print(f"Loaded game_data: {json.dumps(game_data.to_dict(), default=str)}")
        logging.info("Loaded game_data(dict): %s", game_data.to_dict())
        logging.info(
            "Loaded game_data(json): %s", json.dumps(game_data.to_dict(), default=str)
        )
        return game_data

    # Nothing else matched, try Google Sheets
    return get_Gsheet_game(str(game_id))


def json_to_game(j: jpb2.GameData):
    boards = []
    start_value = j.default_start_value or 200
    logging.info("Default Start Value for the first round: %r", start_value)

    for rnd_num, rnd in enumerate(j.rounds):
        categories = []
        questions = []

        if rnd.default_start_value:
            start_value = rnd.default_start_value
            logging.info(
                "Default Start Value for Round#%r was customized to be: %r",
                rnd_num + 1,
                start_value,
            )

        for cat_num, cat in enumerate(rnd.categories):
            categories.append(cat.name)

            cat_value = start_value
            if cat.default_start_value:
                cat_value = cat.default_start_value
                logging.info(
                    "Category %r (Round#%r) has a custom start_value: %r",
                    cat.name,
                    rnd_num,
                    cat_value,
                )

            for q_num, q in enumerate(cat.questions):
                q_value = cat_value * (q_num + 1)

                if q.value:
                    q_value = q.value
                    logging.info(
                        "Question#%r (Round#%r / Category=%r) has a custom value: %r",
                        q_num,
                        rnd_num,
                        cat.name,
                        q_value,
                    )

                questions.append(
                    Question(
                        index=(cat_num, q_num),
                        text=q.text,
                        answer=q.answer,
                        value=q_value,
                        category=cat.name,
                        dd=q.daily_double,
                        complete=False,
                    )
                )

        if rnd_num == len(j.rounds) - 1:
            boards.append(FinalBoard(category=categories[0], question=questions[0]))

        else:
            boards.append(
                Board(categories=categories, questions=questions, dj=(rnd_num % 2 == 0))
            )

        start_value *= j.round_multiplier

    return GameData(
        rounds=boards,
        date=j.date,
        comments=j.title,
    )


def list_to_game(s):
    # Template link: https://docs.google.com/spreadsheets/d/1_vBBsWn-EVc7npamLnOKHs34Mc2iAmd9hOGSzxHQX0Y/edit?usp=sharing
    alpha = "BCDEFG"  # columns
    boards = []
    # gets single and double jeopardy rounds
    for n1 in [1, 14]:
        categories = s[n1 - 1][1:7]
        categories = list(filter(None, categories))

        questions = []
        for row in range(5):
            for col, cat in enumerate(categories):
                try:
                    address = alpha[col] + str(row + n1 + 1)
                    index = (col, row)

                    value = s[row + n1][0]
                    if not value or not value.isalnum():
                        logging.warning(
                            f"Skipping {address} (Invalid Value: {value!r} ; s[{row+n1=!r}][0])"
                        )
                        continue

                    value = int(value)

                    text = s[row + n1][col + 1]
                    if not text:
                        logging.warning(
                            f"Skipping {address} (Empty Text: {text!r} -> s[{row+n1=!r}][{col + 1!r}])"
                        )
                        continue

                    answer = s[row + n1 + 6][col + 1]
                    if not answer:
                        logging.warning(
                            f"Skipping {address} (Empty Answer: {answer!r} -> s[{row+n1+6=!r}][{col + 1!r}])"
                        )
                        continue

                    dd = address in s[n1 - 1][-1]

                    questions.append(Question(index, text, answer, cat, value, dd))

                except Exception as err:
                    logging.warning(
                        f"error loading question ({row=!r}; {col=!r}; {cat=!r}): {str(err)}"
                    )

        boards.append(Board(categories, questions, dj=(n1 == 14)))

    # gets final jeopardy round
    fj = s[-1]
    index = (0, 0)
    text = fj[2]
    answer = fj[3]
    category = fj[1]
    question = Question(index, text, answer, category)
    boards.append(FinalBoard(category, question))
    date = fj[5]
    comments = fj[7]
    return GameData(boards, date, comments)


def get_Gsheet_game(file_id):
    csv_url = f"https://docs.google.com/spreadsheet/ccc?key={file_id}&output=csv"
    with requests.get(csv_url, stream=True) as r:
        lines = (line.decode("utf-8") for line in r.iter_lines())
        r3 = list(csv.reader(lines))
        # print(f"r3: {r3}")
        logging.warning("r3: %s", r3)
        return list_to_game(list(r3))


def findanswer(clue):
    return re.findall(r'correct_response">(.*?)</em', unescape(str(clue)))[0]


def get_jarchive_game(game_id):
    return get_generic_game(
        game_id, f"http://www.j-archive.com/showgame.php?game_id={game_id}"
    )


def get_generic_game(game_id, url):
    logging.info(f"getting game {game_id} from url {url}")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    datesearch = re.search(
        r"- \w+, (.*?)$", soup.select("#game_title > h1")[0].contents[0]
    )

    if datesearch is None:
        return None

    date = datesearch.groups()[0]
    comments = soup.select("#game_comments")[0].contents
    comments = comments[0] if len(comments) > 0 else ""

    # Normal Rounds
    boards = []

    rounds = soup.find_all(class_="round")
    rounds = rounds

    for i, ro in enumerate(rounds):
        categories_objs = ro.find_all(class_="category")
        categories_objs = categories_objs

        categories = [c.find(class_="category_name").text for c in categories_objs]
        categories = categories

        questions = []
        for clue in ro.find_all(class_="clue"):
            text_obj = clue.find(class_="clue_text")
            if text_obj is None:
                logging.info("this game is incomplete")
                return None

            text = text_obj.text
            index_key = text_obj["id"]
            index = (
                int(index_key[-3]) - 1,
                int(index_key[-1]) - 1,
            )  # get index from id string
            dd = clue.find(class_="clue_value_daily_double") is not None
            value = MONIES[i][index[1]]
            answer = findanswer(clue)
            questions.append(
                Question(index, text, answer, categories[index[0]], value, dd)
            )
        boards.append(Board(categories, questions, dj=(i == 1)))

    # Final Jeopardy
    final_round_obj = soup.find_all(class_="final_round")[0]
    category_obj = final_round_obj.find_all(class_="category")[0]
    category = category_obj.find(class_="category_name").text
    clue = final_round_obj.find_all(class_="clue")[0]
    text_obj = clue.find(class_="clue_text")
    if text_obj is None:
        logging.info("this game is incomplete")
        return None

    text = text_obj.text
    answer = findanswer(final_round_obj)
    question = Question((0, 0), text, answer, category)

    boards.append(FinalBoard(category, question))

    return GameData(boards, date, comments)


def get_wayback_game(game_id):
    # kudos to Abhi Kumbar: https://medium.com/analytics-vidhya/the-wayback-machine-scraper-63238f6abb66
    # this query's the wayback cdx api for possible instances of the saved jarchive page with the specified game id & returns the latest one
    JArchive_url = f"j-archive.com/showgame.php?game_id={str(game_id)}"  # use the url w/o the http:// or https:// to include both in query
    url = f"http://web.archive.org/cdx/search/cdx?url={JArchive_url}&collapse=digest&limit=-2&fastLatest=true&output=json"  # for some reason, using limit=-1 does not work
    urls = requests.get(url).text
    parse_url = json.loads(urls)  # parses the JSON from urls.
    if len(parse_url) == 0:  # if no results, return None
        logging.info("no games found in wayback")
        # alternative: use fallback to get game from scraping j-archive directly
        raise Exception("no games found in wayback")

    ## Extracts timestamp and original columns from urls and compiles a url list.
    url_list = []
    for i in range(1, len(parse_url)):  # gets the wayback url
        orig_url = parse_url[i][2]
        tstamp = parse_url[i][1]
        waylink = tstamp + "/" + orig_url
        final_url = f"http://web.archive.org/web/{waylink}"
        url_list.append(final_url)
    latest_url = url_list[-1]
    return get_generic_game(game_id, latest_url)


def get_game_sum(soup):
    date = re.search(
        r"- \w+, (.*?)$", soup.select("#game_title > h1")[0].contents[0]
    ).groups()[0]
    comments = soup.select("#game_comments")[0].contents

    return date, comments


def get_random_game():
    r = requests.get("http://j-archive.com/")
    soup = BeautifulSoup(r.text, "html.parser")

    link = soup.find_all(class_="splash_clue_footer")[1].find("a")["href"]
    return int(link[21:])
