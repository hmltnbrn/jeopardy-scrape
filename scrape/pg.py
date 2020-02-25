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

def insert_no_duplicate(cur, table, data):
    query = "INSERT INTO " + table + " VALUES %s ON CONFLICT (Id) DO NOTHING RETURNING (Id)"
    return psycopg2.extras.execute_values (
        cur, query, data, fetch=True
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

