import sys
import pg
import build
import game_links
import game_data

def by_season(conn, cur, links):
    for season in links:
        length = len(links[season])
        for i in xrange(length):
            jeopardy_data = game_data.get(links[season][i], season)
            amtDone = float(i+1)/float(length)
            if(len(jeopardy_data) > 0):
                build.games(cur, jeopardy_data)
                build.contestants(cur, jeopardy_data["contestants"], jeopardy_data["id"])
                build.rounds(cur, jeopardy_data["rounds"], jeopardy_data["id"])
                pg.commit(conn, cur)
                sys.stdout.write("\rSeason " + str(season) + " Progress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100) + " Episode " + jeopardy_data["show_number"] + " scrape and insert done...")
        sys.stdout.write("\n")

def by_episode(conn, cur, link, season):
    jeopardy_data = game_data.get(link, season)
    build.games(cur, jeopardy_data)
    build.contestants(cur, jeopardy_data["contestants"], jeopardy_data["id"])
    build.rounds(cur, jeopardy_data["rounds"], jeopardy_data["id"])
    pg.commit(conn, cur)
    sys.stdout.write("\rSeason " + str(season) + " Episode " + jeopardy_data["show_number"] + " scrape and insert done...")
    sys.stdout.write("\n")

if __name__ == "__main__":
    conn, cur = pg.connect()

    if sys.argv[1] == '--ep':
        by_episode(conn, cur, sys.argv[2], sys.argv[3])
    else:
        if len(sys.argv) == 3:
            # first argument is season to start on
            # second argument is season to end on
            links = game_links.get(int(sys.argv[1]), int(sys.argv[2]))
        elif len(sys.argv) == 2:
            # first argument is season to start on
            # no second argument will default to last possible season
            links = game_links.get(int(sys.argv[1]))
        else:
            # no arguments will default to first season and last possible season
            links = game_links.get()
        by_season(conn, cur, links)

    pg.disconnect(conn, cur)

    print "Data successfully uploaded"
