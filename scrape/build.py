import pg
from genderize import Genderize
import geocoder
import json

with open('../credentials/keys.json') as key_file:
    keys = json.load(key_file)

def get_gender(name):
    return Genderize().get([name])

def games(cur, data):
    pg.insert(cur, "Games", [(data["id"], data["air_date"], data["season"], data["show_number"], data["before_double"], data["contained_tiebreaker"], data["no_winner"], data["unknown_winner"])])

def contestants(cur, data, game_id, findGender, findLocation):
    contestants = []
    game_contestants = []
    for i in data:
        gender = None
        probability = None
        lat = None
        lng = None
        if(i["first_name"] and findGender):
            gender_data = get_gender(i["first_name"])[0]
            gender = gender_data["gender"]
            probability = gender_data["probability"] if gender_data["gender"] is not None else None
        if(i["home_town"] and findLocation):
            geo = geocoder.google(location=i["home_town"], key=keys["gmaps_api_key"])
            lat, lng = geo.latlng
        contestants.append((i["id"], i["first_name"], i["last_name"], i["profession"], i["home_town"], gender, probability, lat, lng))
        game_contestants.append((game_id, i["id"], i["game_status"]["position"], i["game_status"]["winner"], i["game_status"]["jeopardy_total"], i["game_status"]["double_jeopardy_total"], i["game_status"]["final_jeopardy_total"], i["game_status"]["final_jeopardy_wager"]))
    pg.insert_once(cur, "Contestants", contestants)
    pg.insert(cur, "GameContestants", game_contestants)

def clues(cur, data, category_id):
    clues = []
    rights = []
    wrongs = []
    for i in data:
        clues.append((i["id"], category_id, i["clue"], i["value"], i["answer"], i["daily_double"], i["daily_double_wager"], i["triple_stumper"]))
        for j in range(len(i["rights"])):
            rights.append((i["id"], i["rights"][j]))
        for k in range(len(i["wrongs"])):
            wrongs.append((i["id"], i["wrongs"][k]))
    pg.insert(cur, "Clues", clues)
    pg.insert(cur, "ClueRights", rights)
    pg.insert(cur, "ClueWrongs", wrongs)

def categories(cur, data, game_id, round_id):
    categories = []
    for i in data:
        categories.append((i["id"], game_id, round_id, i["name"]))
    pg.insert(cur, "Categories", categories)
    for i in data:
        clues(cur, i["clues"], i["id"])

def rounds(cur, data, game_id):
    for i in data:
        categories(cur, i["categories"], game_id, i["id"])
