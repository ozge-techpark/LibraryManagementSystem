import sqlite3
import os
from datetime import datetime
import json
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "..", "library.db")

class Loan:
    @staticmethod
    def borrow_book(book_id, member_id): 
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT title, is_available FROM books WHERE book_id = ?", (book_id,))
            book_res = cursor.fetchone()

            
            cursor.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            member_res = cursor.fetchone()

            if book_res and book_res[1] == 1 and member_res:
                book_title = book_res[0]
                member_name = member_res[0]
                loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute(
                    "INSERT INTO loans (book_id, book_title, member_id, member_name, loan_date) VALUES (?, ?, ?, ?, ?)",
                    (book_id, book_title, member_id, member_name, loan_date)
                )

                cursor.execute("UPDATE books SET is_available = 0 WHERE book_id = ?", (book_id,))
                conn.commit()
                print(f"Success: '{book_title}' borrowed by {member_name} successfully!")
            else:
                print("Error: Book is not available.")

            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def return_book(loan_id, member_id = None):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            
            if member_id:
                cursor.execute("""SELECT book_id, book_title FROM loans WHERE loan_id = ? AND member_id = ? AND return_date IS NULL
                """, (loan_id, member_id))
            else:
                cursor.execute("""
                SELECT book_id, book_title FROM loans 
                WHERE loan_id = ? AND return_date IS NULL
            """, (loan_id,))
            result = cursor.fetchone()

            if result:
                book_id, book_title = result[0], result[1]
                return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                
                cursor.execute(
                    "UPDATE loans SET return_date = ? WHERE loan_id = ?", 
                    (return_date, loan_id)
                )

                
                cursor.execute(
                    "UPDATE books SET is_available = 1 WHERE book_id = ?", 
                    (book_id,) 
                )
                
                conn.commit()
                print(f"Success: '{book_title}' has been returned successfully.")
            else:
                print("Error: Invalid Loan ID or this book was not borrowed by you.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def get_member_loans(member_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
        SELECT loan_id, book_title, loan_date 
        FROM loans 
        WHERE member_id = ? AND return_date IS NULL
        """

        cursor.execute(query, (member_id,))
        user_loans = cursor.fetchall()
        conn.close()
        return user_loans
    @staticmethod 
    def get_last_ten_loans():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT loan_id, book_title, member_name, loan_date FROM loans ORDER BY loan_date DESC LIMIT 10"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    @staticmethod
    def get_member_history(member_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
        SELECT book_title, loan_date, return_date
        FROM loans
        WHERE member_id = ?
        ORDER BY loan_date DESC
        """
        cursor.execute(query, (member_id,))
        history = cursor.fetchall()
        conn.close()
        return history
    @staticmethod
    def export_loans_to_json():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM loans")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]

        with open("loans_report.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii= False, indent= 4)

        conn.close()
    @staticmethod
    def get_all_active_loans():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
                    SELECT loan_id, book_title, member_name
                    FROM loans
                    WHERE return_date is NULL
                    """)
        results = cursor.fetchall()
        conn.close()
        return results
    @staticmethod
    def books_loans():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
        SELECT book_title, member_name, loan_date, return_date
        FROM loans
        ORDER BY loan_date DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results