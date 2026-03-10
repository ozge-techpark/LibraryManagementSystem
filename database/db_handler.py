import sqlite3

def create_connection():
    conn = sqlite3.connect('library.db') 
    return conn 

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()


    cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL)
''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS members(
                member_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role INTEGER DEFAULT 2)
''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS books(
                book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT NOT NULL, author_id INTEGER, is_available BOOLEAN DEFAULT 1, 
                FOREIGN KEY (author_id) REFERENCES authors(author_id))
''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                loan_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (member_id) REFERENCES members (member_id))
''')
    conn.commit()
    conn.close()
print("Database created succesfully")
if __name__ == "__main__":
    create_tables()