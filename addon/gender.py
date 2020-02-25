import sys
import json
from genderize import Genderize
import pg

def get_contestants(cur):
    return pg.select_all_where(cur, "contestants", "gender IS NULL")

def get_gender(name):
    return Genderize().get([name])

def update_gender(conn, cur, id, gender, probability):
    pg.update_gender(cur, [(id, gender, probability)])
    pg.commit(conn)

if __name__ == "__main__":
    with open('../credentials/keys.json') as key_file:
        keys = json.load(key_file)

    conn, cur = pg.connect()

    print("Using Gender API")

    contestants = get_contestants(cur)

    length = len(contestants)

    for i in range(length):
        amtDone = float(i+1)/float(length)
        gender_data = get_gender(contestants[i][1])[0]
        gender = gender_data["gender"]
        probability = gender_data["probability"] if gender_data["gender"] is not None else None
        update_gender(conn, cur, contestants[i][0], gender, probability)
        sys.stdout.write("\rContestant " + str(contestants[i][0]) + " -- " + contestants[i][1] + " " + contestants[i][2] + " -- Progress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
        sys.stdout.flush()
    sys.stdout.write("\n")

    pg.disconnect(conn, cur)

    print("Data successfully updated")
