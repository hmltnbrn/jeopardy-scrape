import sys
import json
import geocoder
import pg

def get_contestants(conn, cur):
    return pg.select_all_where(cur, "contestants", "latitude IS NULL AND longitude IS NULL AND hometown IS NOT NULL")

def do_geocode(key, location):
    return geocoder.google(location=location, key=keys["gmaps_api_key"])

def update_coords(conn, cur, id, lat, lng):
    pg.update_lat_lng(cur, [(id, lat, lng)])
    pg.commit(conn, cur)

if __name__ == "__main__":
    with open('../credentials/keys.json') as key_file:
        keys = json.load(key_file)

    conn, cur = pg.connect()

    print("Using Google Geocoding API")

    contestants = get_contestants(conn, cur)[0:2]

    length = len(contestants)

    for i in range(length):
        amtDone = float(i+1)/float(length)
        lat, lng = do_geocode(keys["gmaps_api_key"], contestants[i][4]).latlng
        update_coords(conn, cur, contestants[i][0], str(lat), str(lng))
        sys.stdout.write("\rContestant " + str(contestants[i][0]) + " -- " + contestants[i][1] + " " + contestants[i][2] + " -- Progress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100))
        sys.stdout.flush()
    sys.stdout.write("\n")

    pg.disconnect(conn, cur)

    print("Data successfully updated")
