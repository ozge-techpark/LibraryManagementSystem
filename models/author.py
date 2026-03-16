import sqlite3
import os

base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "..", "library.db")
class Author:
    def __init__(self, name, author_id = None):
        self.id= author_id
        self.name = name

    @staticmethod
    def add_author(name):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            print(f"Author '{name} added succesfully.")

        except sqlite3.Error as e:
            print(f"An error occured: {e}")

    @staticmethod
    def list_authors():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors")
        authors = cursor.fetchall()
        conn.close()
        return authors