import psycopg2
import psycopg2.extras
import json

def select_clues_by_season(cur, season):
    query = "SELECT g.id AS game_id, g.air_date, c.id AS clue_id, ca.category_name, c.clue_text, c.answer FROM clues c, categories ca, games g WHERE c.category_id = ca.id AND ca.game_id = g.id AND (c.clue_text != '-' OR c.answer != '-') AND g.season = '" + season + "'"
    cur.execute(query)
    return cur.fetchall()

def select_all_clues(cur):
    query = "SELECT g.id AS game_id, g.air_date, c.id AS clue_id, c.clue_text, c.answer FROM clues c, categories ca, games g WHERE c.category_id = ca.id AND ca.game_id = g.id AND (c.clue_text != '-' OR c.answer != '-')"
    cur.execute(query)
    return cur.fetchall()

def select_all_contestants(cur):
    query = "SELECT id, first_name, last_name, profession FROM contestants WHERE profession IS NOT NULL"
    cur.execute(query)
    return cur.fetchall()

def insert_topic_keys(cur, table, data):
    query = "INSERT INTO " + table + " (id, run_weight, full_text, short_text) VALUES %s ON CONFLICT (Id) DO UPDATE SET run_weight = EXCLUDED.run_weight, full_text = EXCLUDED.full_text"
    psycopg2.extras.execute_values (
        cur, query, data
    )

def update_clue_topics(cur, data):
    query = "UPDATE clues SET topic_id = data.topic_id, topic_weight = data.topic_weight, topics_all = data.topics_all FROM (VALUES %s) AS data(clue_id, topic_id, topic_weight, topics_all) WHERE clues.id = data.clue_id;"
    psycopg2.extras.execute_values (
        cur, query, data, template="(%s, %s, %s, %s::jsonb)"
    )

def update_contestant_topics(cur, data):
    query = "UPDATE contestants SET profession_topic_id = data.topic_id, profession_topic_weight = data.topic_weight, profession_topics_all = data.topics_all FROM (VALUES %s) AS data(contestant_id, topic_id, topic_weight, topics_all) WHERE id = data.contestant_id;"
    psycopg2.extras.execute_values (
        cur, query, data, template="(%s, %s, %s, %s::jsonb)"
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
