from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import re

app = Flask(__name__)

# Connect to the database
conn = psycopg2.connect(database="spotify_db", user="postgres",
                        password="root", host="localhost", port="5432")

# create a cursor
cur = conn.cursor()

# song
cur.execute(
    '''CREATE TABLE IF NOT EXISTS song1 (
    track_name varchar(100), 
    artist varchar(100),
    album varchar(100),
    release_date varchar(100), 
    popularity int, 
    songid varchar(100) PRIMARY KEY, 
    duration_min float);''')

cur.execute('''CREATE TABLE IF NOT EXISTS myall (
            track_name varchar(100),
            artist varchar(100),
            album varchar(100),
            release_date varchar(100),
            popularity int,
            spotify_url varchar(100),
            id varchar(100) PRIMARY KEY,
            duration_min float)
            ''')

cur.execute(''' COPY myall(track_name,artist,album,release_date,popularity,spotify_url,id,duration_min) \
            FROM '/Users/idamarienielsen/Documents/ku/DIS/DIS-projekt/spotify_top_1000_tracks.csv' \
            DELIMITER ',' \
            CSV HEADER; \
            ''')

cur.execute('''INSERT INTO song1(track_name, artist, album, release_date, popularity, songid, duration_min)
            SELECT DISTINCT track_name, artist, album, release_date, popularity, id, duration_min
            FROM myall
            WHERE id NOT IN (SELECT songid FROM song1); 
            ''')

# commit the changes
conn.commit()

@app.route("/", methods=["GET"])
def home():
    # Query the data from the song table
    cur = conn.cursor()
    #cur.execute("SELECT track_name, artist, album, release_date, popularity, duration_min FROM song1;")
    #songs = cur.fetchall()  # Fetch all rows from the query result

    # Get the search query from the request
    query = request.args.get("q", "").strip()  # Default to an empty string if no query is provided
    query_regex = " ".join(re.findall(r"[a-zA-Z0-9\s]+", query))
    # Query the database for matching songs
    if query_regex:
        cur.execute('''
            SELECT track_name, artist, album, release_date, popularity, duration_min
            FROM song1
            WHERE track_name ILIKE %s OR artist ILIKE %s OR album ILIKE %s;
        ''', (f"%{query_regex}%", f"%{query_regex}%", f"%{query_regex}%"))
    else:
        cur.execute('''
            SELECT track_name, artist, album, release_date, popularity, duration_min
            FROM song1;
        ''')
    
    songs = cur.fetchall()

    # Pass the data to the HTML template
    return render_template("home.html", songs=songs)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

# close the cursor and connection
cur.close()
conn.close()

# @app.route("/search", methods=["GET"])
# def search():

#     # Pass the filtered results to the HTML template
#     return render_template("home.html", songs=songs)

# albumid varchar(100) \ FOREIGN KEY (albumid) REFERENCES album(albumid) \ FOREIGN KEY ()


# # artist
# cur.execute(
#     '''CREATE TABLE IF NOT EXISTS artist (artistname varchar(100), \
#     artistid SERIAL PRIMARY KEY);''')


# # album
# cur.execute(
#     '''CREATE TABLE IF NOT EXISTS album (albumname varchar(100), \
#     albumid SERIAL PRIMARY KEY);''')


# # connect tables
# cur.execute(
#     '''CREATE TABLE IF NOT EXISTS belong ( 
#         songid varchar(100), 
#         artistid varchar(100), 
#         albumid varchar(100), 
#         PRIMARY KEY (songid, artistid, albumid), 
#         FOREIGN KEY (songid) REFERENCES song(songid), 
#         FOREIGN KEY (artistid) REFERENCES artist(artistid), 
#         FOREIGN KEY (albumid) REFERENCES album(albumid)
#     );'''
# )
