import sqlite3

class Member:

    def __init__ (self,name, email, password, role='member', member_id = None):
        self.name = name
        self.member_id = member_id
        self.email = email
        self.password = password
        self.role = role


    @staticmethod
    def add_member(name,email,password, role='member'):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO members (name, email, password, role) VALUES (?,?,?,?)",
                (name, email, password, role)           
                )
            conn.commit()
            conn.close()
            print(f"User {name} created as {role}!")
        except sqlite3.IntegrityError:
            print(f"Error: The email '{email}' is already registered!")
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
    def login(email,password):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT member_id, name, role FROM members WHERE wmail = ? AND password = ?",
                (email, password)
            )
            user = cursor.fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print(f"Login error: {e}")
            return None
    def list_members():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        conn.close()
        return members