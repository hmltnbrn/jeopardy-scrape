import psycopg2
import psycopg2.extras
import json

def select_all(cur, table):
    query = "SELECT * FROM " + table
    cur.execute(query)
    return cur.fetchall()

def select_all_where(cur, table, where_string):
    query = "SELECT * FROM " + table + " WHERE " + where_string
    cur.execute(query)
    return cur.fetchall()

def update_lat_lng(cur, data):
    query = "UPDATE contestants SET latitude = data.latitude, longitude = data.longitude FROM (VALUES %s) AS data(id, latitude, longitude) WHERE contestants.id = data.id;"
    psycopg2.extras.execute_values (
        cur, query, data
    )

def update_gender(cur, data):
    query = "UPDATE contestants SET gender = data.gender, gender_probability = data.probability FROM (VALUES %s) AS data(id, gender, probability) WHERE contestants.id = data.id;"
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
