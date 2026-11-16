import json
import pandas as pd
from urllib.request import build_opener, install_opener, urlretrieve
from urllib.error import HTTPError

def extract_matches(text):
    start = text.index("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])


def calculate_opponent_ages(data):
    values = data["opponent_age_or_birth_date"]
    if values.iloc[0].isdigit():
        birth_dates = pd.to_datetime(values, format="%Y%m%d", errors="coerce")
        return (data["match_date"] - birth_dates).dt.days / 365.25
    return pd.to_numeric(values, errors="coerce")


def add_player_ages(data, player_birth_date):
    player_birth_date = pd.to_datetime(player_birth_date)
    data["player_age"] = ((data["match_date"] - player_birth_date).dt.days / 365.25)
    data["age_difference"] = data["player_age"] - data["opponent_age"]
    return data


def make_match_dataframe(matches, player_birth_date):
    data = pd.DataFrame({
        "match_date": [row[0] for row in matches],
        "result": [row[4] for row in matches],
        "opponent": [row[11] for row in matches],
        "opponent_age_or_birth_date": [row[16] for row in matches],})
    return clean_match_dataframe(data, player_birth_date)


def clean_match_dataframe(data, player_birth_date):
    data["match_date"] = pd.to_datetime(data["match_date"], format="%Y%m%d", errors="coerce")
    data["result"] = data["result"].replace({"W": "win", "L": "loss"})
    data["opponent_age"] = calculate_opponent_ages(data)
    return add_player_ages(data, player_birth_date)
	
def make_player_id(player_name):
    name = player_name.strip()
    if not name:
        raise ValueError("Please enter a player name.")
    if " " not in name:
        return name[0].upper() + name[1:]
    player_id = ""
    for word in name.split():
        player_id += word.capitalize()
    return player_id

def download_career_js(player_id):
    url = f"https://www.tennisabstract.com/jsmatches/{player_id}Career.js"
    filename = f"{player_id}Career.js"
    opener = build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    install_opener(opener)
    try:
        urlretrieve(url, filename)
    except HTTPError as error:
        if error.code == 404:
            raise ValueError(f"No career data found for {player_id}.")
        raise
    with open(filename, "r") as file:
        text = file.read()
    return text

def get_player_birth_date(player_id, is_womens):
    if is_womens:
        page = "wplayer-classic.cgi"
    else:
        page = "player-classic.cgi"

    url = f"https://www.tennisabstract.com/cgi-bin/{page}?p={player_id}"
    filename = f"{player_id}Profile.html"
    urlretrieve(url, filename)

    with open(filename, "r") as file:
        profile = file.read()

    age_start = profile.find("Age:")
    date_start = profile.find("(", age_start) + 1
    date_end = profile.find(")", date_start)
    birth_date = profile[date_start:date_end]
    return pd.to_datetime(birth_date, format="%d-%b-%Y")

def get_career_data(player_name):
    player_id = make_player_id(player_name)
    text = download_career_js(player_id)
    matches = extract_matches(text)
    if len(matches) == 0:
        raise ValueError(f"No matches found for {player_name}.")
    first_value = matches[0][16]
    is_womens = False
    if len(first_value) == 8 and first_value.isdigit():
        is_womens = True
    birth_date = get_player_birth_date(player_id, is_womens)
    return make_match_dataframe(matches, birth_date)