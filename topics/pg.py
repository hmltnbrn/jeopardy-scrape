import psycopg2
import psycopg2.extras
import json

def select_clues_by_season(cur, season):
    query = "SELECT g.id, g.air_date, c.id, c.clue_text, c.answer FROM clues c, categories ca, games g WHERE c.category_id = ca.id AND ca.game_id = g.id AND g.season = '" + season + "'"
    cur.execute(query)
    return cur.fetchall()

def select_all_clues(cur):
    query = "SELECT g.id, g.air_date, c.id, c.clue_text, c.answer FROM clues c, categories ca, games g WHERE c.category_id = ca.id AND ca.game_id = g.id"
    cur.execute(query)
    return cur.fetchall()

def connect():
    with open('../credentials/credentials.json') as cred_file:
        creds = json.load(cred_file)
    conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
    cur = conn.cursor()
    return conn, cur

def commit(conn, cur):
    conn.commit()

def disconnect(conn, cur):
    cur.close()
    conn.close()
