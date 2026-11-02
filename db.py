# db.py - leaderboard storage for Space War
#
# Talks to the MySQL/MariaDB server that comes with XAMPP.
# The game imports this file; all SQL lives here so the game code stays clean.

import mysql.connector

# XAMPP defaults: user "root" with an EMPTY password on localhost:3306.
# If you set a MySQL password in XAMPP, put it here.
DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "",
    "connection_timeout": 3,   # fail fast if MySQL isn't running
}
DB_NAME = "space_war"


def _connect(use_database=True):
    config = dict(DB_CONFIG)
    if use_database:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)


def init_db():
    """Create the database and the scores table if they don't exist yet.
    Safe to call every time the game starts."""
    conn = _connect(use_database=False)
    try:
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS " + DB_NAME +
                    " CHARACTER SET utf8mb4")
        cur.execute("USE " + DB_NAME)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(30) NOT NULL,
                score       INT         NOT NULL,
                played_at   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) DEFAULT CHARSET=utf8mb4
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_score(player_name, score):
    """Insert one finished game. Uses %s placeholders (a parameterised query),
    so a player typing SQL as their name can't break or hack the database."""
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scores (player_name, score) VALUES (%s, %s)",
            (player_name, score),
        )
        conn.commit()
    finally:
        conn.close()


def top_scores(limit=5):
    """Return the best scores as a list of (player_name, score) tuples.
    Ties are won by whoever got the score first."""
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT player_name, score FROM scores "
            "ORDER BY score DESC, played_at ASC, id ASC LIMIT %s",
            (limit,),
        )
        return cur.fetchall()
    finally:
        conn.close()
