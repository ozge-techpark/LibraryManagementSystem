import sqlite3
from datetime import datetime


class Loan:
    @staticmethod
    def borrow_book(book_id, member_id):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            cursor.execute("SELECT is_available FROM books WHERE book_id = ?",(book_id,))
            result = cursor.fetchone()

            if result and result[0] == 1:
                loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO loans (book_id,member_id,loan_date) VALUES (?,?,?)",
                    (book_id, member_id, loan_date)
                )
                cursor.execute("UPDATE books SET is_available = 0 WHERE book_id = ?", (book_id))
                conn.commit()
                print("Success: Book borrowed successfully")
            else: 
                print("Error: Book is already borrowed or not registered.")
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    @staticmethod
    def return_book(loan_id):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            cursor.execute("SELECT book_id FROM loans WHERE loan_id = ?", (loan_id))
            result = cursor.fetchone()

            if result:
                book_id = result[0]
                return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("UPDATE loans SET return_date = ? WHERE loan_id = ?", (return_date, loan_id))

                cursor.execute("UPDATE books SET is_available = 1 WHERE book_id = ?", (book_id))
                conn.commit()

            else:
                print("Error: Loan record not found.")
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        

