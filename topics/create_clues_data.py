import sys
import pg
import argparse

def get_clues_by_season(cur, season):
    return pg.select_clues_by_season(cur, season)

def create_text_files(cur, start_season = 1, end_season = 35):
    print('Starting with season {start_season} and ending with season {end_season}'.format(start_season = str(start_season), end_season = str(end_season)))
    for season in range(start_season, end_season + 1):
        current_season = str(season)
        clues = get_clues_by_season(cur, current_season)
        length = len(clues)
        for i in range(len(clues)):
            amtDone = float(i+1)/float(length)
            with open('mallet_files/data/clues/{game_id}_{air_date}_{clue_id}.txt'.format(game_id=clues[i][0], air_date=clues[i][1].split('T')[0], clue_id=clues[i][2]), 'w+', encoding='utf-8') as text_file:
                text_file.write("{clue_text} {answer}".format(clue_text=clues[i][3], answer=clues[i][4]))
            sys.stdout.write("\r Season " + current_season + " Clue " + str(clues[i][2]) + " -- Progress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
            sys.stdout.flush()
        sys.stdout.write("\n")

if __name__ == "__main__":
    conn, cur = pg.connect()

    parser = argparse.ArgumentParser(description="Select Clues for Mallet")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--season", nargs=2, metavar=('start_season', 'end_season'), type=int, help="Get specific seasons")
    group.add_argument("-a", "--all", action='store_true', help="Get all seasons")
    args = parser.parse_args()

    if args.all:
        create_text_files(cur)
    elif args.season:
        create_text_files(cur, args.season[0], args.season[1])

    pg.disconnect(conn, cur)

    print("Text Files Created")
