import json
import pandas as pd

def extract_matches(text):
    start = text.index("[")
    end = text.rfind("]") + 1
    matches = json.loads(text[start:end])
    return matches

def make_match_dataframe(matches):
    data = pd.DataFrame({
        "match_date": [row[0] for row in matches],
        "result": [row[4] for row in matches],
        "opponent": [row[11] for row in matches],
        "opponent_age_or_birth_date": [row[16] for row in matches],
    })
	data["match_date"] = pd.to_datetime(data["match_date"], format="%Y%m%d", errors="coerce")
    data["result"] = data["result"].replace({"W": "win", "L": "loss"})
    return data

def _calculate_opponent_age(match_date, value):
    if len(value) == 8 and value.isdigit():
        birth_date = pd.to_datetime(value, format="%Y%m%d", errors="coerce")
        return (match_date - birth_date).days / 365.25
    return pd.to_numeric(value, errors="coerce")