import csv
import pg
import os
from psycopg2.extras import Json

if __name__ == "__main__":
    conn, cur = pg.connect()

    clues = []

    print("Parsing composition file...")

    with open('mallet_files/output/clues/jeopardy_composition.txt') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            topic_weight_list = [float(i) for i in row[2:]]
            clue_id = os.path.splitext(os.path.basename(row[1]))[0].split('_')[-1]
            topic_weight = topic_weight_list[0]
            topic_id = 0
            for i in range(1, len(topic_weight_list)):
                if(topic_weight_list[i] >= topic_weight):
                    topic_weight = topic_weight_list[i]
                    topic_id = i
            topics_all = Json({i: topic_weight_list[i] for i in range(len(topic_weight_list))})
            clues.append((clue_id, topic_id, topic_weight, topics_all))

    pg.update_clue_topics(cur, clues)
    pg.commit(conn)

    pg.disconnect(conn, cur)

    print("Clues Updated")
