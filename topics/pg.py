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

def insert_topic_keys(cur, data):
    query = "INSERT INTO topics (id, run_weight, full_text, short_text) VALUES %s ON CONFLICT (Id) DO UPDATE SET run_weight = EXCLUDED.run_weight, full_text = EXCLUDED.full_text"
    psycopg2.extras.execute_values (
        cur, query, data
    )

def update_clue_topics(cur, data):
    query = "UPDATE clues SET topic_id = data.topic_id, topic_weight = data.topic_weight FROM (VALUES %s) AS data(clue_id, topic_id, topic_weight) WHERE clues.id = data.clue_id;"
    psycopg2.extras.execute_values (
        cur, query, data
    )

def connect():
    with open('../credentials/credentials.json') as cred_file:
        creds = json.load(cred_file)
    conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
    cur = conn.cursor()
    return conn, cur

def commit(conn):
    conn.commit()

def disconnect(conn, cur):
    cur.close()
    conn.close()
