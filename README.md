# DIS-projekt

## ER
![ER Diagram](spotifyER.png)

## Regex
`[a-zA-Z0-9\s\.&\-\'\+]+` is used to find songs/albums/artists that have the given input in them. 
We then show only matches.

## preparation
- prerequisites: python3, flask, psycopg2
- create a database with PostGres, named `spotify_db` with `CREATE DATABASE spotify_db;` in the PostGres terminal

## how to run
- clone this repository
- run `python3 main.py` in the root directory of this repo
- open http://127.0.0.1:5001 as shown in the terminal
- interact with the database (handled with SQL) using the search bar (searches among songs, albums and artists)