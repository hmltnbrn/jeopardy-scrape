import csv
import pg

if __name__ == "__main__":
    conn, cur = pg.connect()

    topics = []

    print("Parsing keys file...")

    with open('mallet_files/jeopardy_keys.txt') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            topics.append((row[0], float(row[1]), row[2].strip(), None))

    pg.insert_topic_keys(cur, topics)
    pg.commit(conn)

    print("Topic Keys Inserted")
