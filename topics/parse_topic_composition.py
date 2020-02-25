import csv
import pg
import os

if __name__ == "__main__":
    conn, cur = pg.connect()

    clues = []

    print("Parsing composition file...")

    with open('mallet_files/jeopardy_composition.txt') as tsvfile:
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
            clues.append((clue_id, topic_id, topic_weight))

    pg.update_clue_topics(cur, clues)
    pg.commit(conn)

    print("Clues and Topics Updated")
