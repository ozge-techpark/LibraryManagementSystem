import sqlite3

class Member:

    def __init__ (self,name, email, member_id = None):
        self.name = name
        self.member_id = member_id
        self.email = email

    @staticmethod
    def add_member(name,email):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO members (name, email) VALUES (?,?)",
                (name, email)
            )
            conn.commit()
            conn.close()
            print(f"Member '{name}' registered successfully.")
        except sqlite3.IntegrityError:
            print(f"Error: The email '{email}' is already registered!")
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
    def list_members():
        conn = sqlite3.connect('library_db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        conn.close()
        return members