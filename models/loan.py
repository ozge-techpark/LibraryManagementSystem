import sqlite3
import os
from datetime import datetime
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
                print("Error: Book is not available or Member not found.")

            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def return_book(loan_id):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            
            cursor.execute("SELECT book_id, book_title FROM loans WHERE loan_id = ?", (loan_id,))
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
                print(f"Error: Loan record with ID {loan_id} not found.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def get_member_loans(member_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """ SELECT loan_id, book_title, loan_date, FROM loans WHERE member_id = ? AND return_date IS NULL"""

        cursor.execute(query, (member_id,))
        user_loans = cursor.fetchall()
        conn.close()
        return user_loans