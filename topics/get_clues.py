import sys
import json
import pg

def get_clues_by_season(cur, season):
    return pg.select_clues_by_season(cur, season)

def get_all_clues(cur):
    return pg.select_all_clues(cur)

if __name__ == "__main__":
    with open('../credentials/keys.json') as key_file:
        keys = json.load(key_file)

    conn, cur = pg.connect()

    print("Selecting Clues")

    clues = get_clues_by_season(cur, '1')

    length = len(clues)

    print("Creating Text Files")

    for i in range(len(clues)):
        amtDone = float(i+1)/float(length)
        with open('../data/{game_id}_{air_date}_{clue_id}.txt'.format(game_id=clues[i][0], air_date=clues[i][1].split('T')[0], clue_id=clues[i][2]), 'w+', encoding='utf-8') as text_file:
            text_file.write("{clue_text} {answer}".format(clue_text=clues[i][3], answer=clues[i][4]))
        sys.stdout.write("\rClue " + str(clues[i][2]) + " -- Progress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
        sys.stdout.flush()
    sys.stdout.write("\n")

    print("Text Files Created")
