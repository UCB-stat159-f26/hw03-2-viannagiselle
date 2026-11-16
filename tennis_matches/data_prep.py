import json
import pandas as pd


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