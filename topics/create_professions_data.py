import sys
import pg
import argparse

def get_contestants(cur):
    return pg.select_all_contestants(cur)

def create_text_files(cur):
    print('Creating profession text files...')
    contestants = get_contestants(cur)
    length = len(contestants)
    for i in range(length):
        amtDone = float(i+1)/float(length)
        last_name = contestants[i][2].replace('"', '').replace(' ', '-') if contestants[i][2] is not None else contestants[i][2]
        with open('mallet_files/data/professions/{contestant_id}_{first_name}_{last_name}.txt'.format(contestant_id=contestants[i][0], first_name=contestants[i][1], last_name=last_name), 'w+', encoding='utf-8') as text_file:
            text_file.write("{profession}".format(profession=contestants[i][3]))
        sys.stdout.write("\r Contestant " + contestants[i][0] + " -- Progress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
        sys.stdout.flush()
    sys.stdout.write("\n")

if __name__ == "__main__":
    conn, cur = pg.connect()

    create_text_files(cur)

    pg.disconnect(conn, cur)

    print("Text Files Created")
