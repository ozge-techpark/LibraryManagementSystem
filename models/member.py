import sqlite3
import os
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "..", "library.db")
USER_ROLES = {
    1: "manager",
    2: "member"
}
class Member:

    def __init__ (self,name, email, password, role_id = 2, member_id = None):
        self.name = name
        self.member_id = member_id
        self.email = email
        self.password = password
        self.role_id = role_id
    

    @staticmethod
    def add_member(name,email,password, role_id = 2):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO members (name, email, password, role) VALUES (?,?,?,?)",
                (name, email, password, role_id)           
                )
            conn.commit()
            conn.close()
            print(f"User {name} created as {USER_ROLES[role_id]}!")
            print("Register successful. You can login now..")
        except sqlite3.IntegrityError:
            print(f"Error: The email '{email}' is already registered!")
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def login(email,password):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT member_id, name, role FROM members WHERE email = ? AND password = ?",
                (email, password)
            )
            user = cursor.fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print(f"Login error: {e}")
            return None
    @staticmethod
    def list_members():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        conn.close()
        return members