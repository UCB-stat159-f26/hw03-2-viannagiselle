import json
import pandas as pd

def extract_matches(text):
    start = text.index("[")
    end = text.rfind("]") + 1
    matches = json.loads(text[start:end])
    return matches

def make_match_dataframe(matches):
    return pd.DataFrame({
        "match_date": [row[0] for row in matches],
        "result": [row[4] for row in matches],
        "opponent": [row[11] for row in matches],
        "opponent_age_or_birth_date": [row[16] for row in matches],
    })

