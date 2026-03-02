import sqlite3

class Book:
    def __init__(self, title,author_id, is_available = 1, book_id = None):
        self.id= book_id
        self.title = title
        self.author_id = author_id
        self.is_available = is_available 

    @staticmethod
    def add_book(title, author_id):
        try: 
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO books (title, author_id, is_available) VALUES (?,?,?)",
                (title, author_id ,1)
            )

            conn.commit()
            conn.close()
            print(f"Book '{title}' added succesfully.")
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
        
    @staticmethod
    def list_books():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        query = """
        SELECT  b.book_id, b.title, a.name, b.is_available
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        """
        cursor.execute (query)
        conn.close()
        return Book
