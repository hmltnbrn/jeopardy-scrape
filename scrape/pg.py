import psycopg2
import psycopg2.extras
import json

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

def connect():
    with open('../database/credentials.json') as cred_file:
        cred = json.load(cred_file)
    conn = psycopg2.connect(host=cred["host"],database=cred["database"], user=cred["user"], password=cred["password"])
    cur = conn.cursor()
    return conn, cur

def commit(conn, cur):
    conn.commit()

def disconnect(conn, cur):
    cur.close()
    conn.close()

