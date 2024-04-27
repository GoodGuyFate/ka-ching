import sqlite3
import os

def check_and_create_database(db_file):
    """Checks if the database file exists and creates it if not."""
    if not os.path.isfile(db_file):
        create_table(db_file)
        insert_initial_score(db_file)
        print("Database created successfully!")


def create_table(db_file):
    """Creates a database table named Scores with id (primary key) and score columns."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        score INTEGER NOT NULL
                      )"""
        )

        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def insert_initial_score(db_file):
    """Inserts a row with a score of 0 into the Scores table if it's empty."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check if there are any existing scores (optional)
        cursor.execute("SELECT COUNT(*) FROM Scores")
        if cursor.fetchone()[0] == 0:  # If no rows exist (empty table)
            cursor.execute("INSERT INTO Scores (score) VALUES (0)")
            conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(db_file):
    """Creates a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def save_high_score(score):
    """Saves a new high score to the database."""
    conn = create_connection("high_scores.db")  # Reconnect to database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Scores (score) VALUES (?)", (score,))
    conn.commit()
    conn.close()


def load_high_score():
    """Retrieves the highest score from the database."""
    conn = create_connection("high_scores.db")  # Reconnect to database
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(score) FROM Scores")
    result = cursor.fetchone()

    if result is None:
        return 0  # Return 0 if no score found
    else:
        return result[0]


def close_connection(conn):
    """Closes the connection to the database."""
    if conn is not None:
        conn.close()