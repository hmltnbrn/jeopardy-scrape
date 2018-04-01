import sys
import json
import datetime
import psycopg2
import psycopg2.extras
# import game_links
import game_data

def insert(cur, table, data):
    query = "INSERT INTO " + table + " VALUES %s"
    psycopg2.extras.execute_values (
        cur, query, data
    )

def insert_once(cur, table, data):
    query = "INSERT INTO " + table + " VALUES %s ON CONFLICT (Id) DO NOTHING"
    psycopg2.extras.execute_values (
        cur, query, data
    )

def games(cur, data):
    insert(cur, "Games", [(data["id"], data["air_date"], data["season"], data["show_number"], data["before_double"])])

def contestants(cur, data, game_id):
    contestants = []
    game_contestants = []
    for i in data:
        contestants.append((i["id"], i["first_name"], i["last_name"], i["profession"], i["home_town"]))
        game_contestants.append((game_id, i["id"], i["game_status"]["winner"], i["game_status"]["jeopardy_total"], i["game_status"]["double_jeopardy_total"], i["game_status"]["final_jeopardy_total"], i["game_status"]["final_jeopardy_wager"]))
    insert_once(cur, "Contestants", contestants)
    insert(cur, "GameContestants", game_contestants)

def clues(cur, data, category_id):
    clues = []
    rights = []
    wrongs = []
    for i in data:
        clues.append((i["id"], category_id, i["clue"], i["value"], i["answer"], i["daily_double"], i["daily_double_wager"], i["triple_stumper"]))
        for j in xrange(len(i["rights"])):
            rights.append((i["id"], i["rights"][j]))
        for k in xrange(len(i["wrongs"])):
            wrongs.append((i["id"], i["wrongs"][k]))
    insert(cur, "Clues", clues)
    insert(cur, "ClueRights", rights)
    insert(cur, "ClueWrongs", wrongs)

def categories(cur, data, game_id, round_id):
    categories = []
    for i in data:
        categories.append((i["id"], game_id, round_id, i["name"]))
    insert(cur, "Categories", categories)
    for i in data:
        clues(cur, i["clues"], i["id"])

def rounds(cur, data, game_id):
    rounds = []
    for i in data:
        categories(cur, i["categories"], game_id, i["id"])

if __name__ == "__main__":
    with open('../database/credentials.json') as cred_file:
        cred = json.load(cred_file)

    conn = psycopg2.connect(host=cred["host"],database=cred["database"], user=cred["user"], password=cred["password"])
    cur = conn.cursor()

    jeopardy_data = game_data.get(sys.argv[1], sys.argv[2])

    games(cur, jeopardy_data)
    contestants(cur, jeopardy_data["contestants"], jeopardy_data["id"])
    rounds(cur, jeopardy_data["rounds"], jeopardy_data["id"])

    conn.commit()

    cur.close()
    conn.close()
