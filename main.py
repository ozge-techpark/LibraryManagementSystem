import sys
from models.member import Member
from models.book import Book
from models.author import Author
from models.loan import Loan
from models.member import USER_ROLES

def manager_menu():
    while True:
        print("1. Add Author")
        print("2. Add Book")
        print("3. List All Books")
        print("4. Delete book")
        print("5. Last 10 Loans")
        print("6. Export Loans Report")
        print("7. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter an Author name: ")
            Author.add_author(name)
        elif choice == '2':
            title = input("Enter a book title: ")
            print("\n--- Available Authors ---")
            for author in Author.list_authors():
                print(f"ID: {author[0]} | Name: {author[1]}")
            author_id = input("Enter author ID: ")
            Book.add_book(title, author_id)
        elif choice == '3':
            books = Book.list_books()
            print("All books in the library: ")
            for book in books:
                status = "Available" if book[3] == 1 else "on loan"
                print(f"ID: {book[0]} | Title: {book[1]} | Status: {status}")
        elif choice == '4':
            books = Book.list_books()
            for book in books: 
                print(f"ID: {book[0]} | Title: {book[1]}")
            target_id = int(input("Please choose a book ID for deleting the book: "))
            Book.delete_book(target_id)
        elif choice == '5':
            last_loans = Loan.get_last_ten_loans()
            for last in last_loans:
                print(f"ID: {last[0]} | Book: {last[1]} | Member: {last[2]} | Date: {last[3]}")
        elif choice == '6':
            Loan.export_loans_to_json()
            print("Report generated successfully!")    
        elif choice == '7':
            print("Logging out..")
            break
def member_menu(member_id):
    while True:
        print("1. List All Books")
        print("2. My Borrowed Books")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Logout")

        choice = input("Select an option: ")

        if choice == '1':
            books = Book.list_books()
            if books:
                for book in books:
                    status = "Available" if book[3] == 1 else "On Loan"
                    print(f"ID: {book[0]} | Title: {book[1]} | Status: {status}")
            else: 
                print("There are no books registered in the library.")
        elif choice == '2':
            loans = Loan.get_member_loans(member_id)
            if loans:
                print("Your books: ")
                for loan in loans:
                    print(f"Loan ID: {loan[0]} | Book: {loan[1]} | Date: {loan[2]}")
            else:
                print("You don't have any active loans.")
        elif choice == '3':
            book_id = input("Enter Book ID to borrow: ")
            Loan.borrow_book(book_id, member_id)
        elif choice == '4':
            loan_id = input("Enter Loan ID to return: ")
            Loan.return_book(loan_id)
        elif choice == '5':
            print("Loging out..")
            break
def main():
    while True:
        print("Welcome to Library System")
        print("1. Login ")
        print("2. Register ")
        print("3. Exit")

        start_choice = input("Select: ")
        if start_choice == '1':
            email = input("Email: ")
            password = input("Password: ")

            user = Member.login(email,password)
            if user:
                member_id, name, role_id = user
                role_name = USER_ROLES[role_id]
                print(f"Login successful. Welcome, {name} ({role_name})")

                if role_id == 1:
                    manager_menu()
                else:
                    member_menu(member_id)
            else:
                print("Error: Invalid email or password")
        elif start_choice == '2':
            name = input("Your name: ")
            email = input("Email: ")
            password = input("Password: ")
            Member.add_member(name, email, password)
        elif start_choice == '3':
            sys.exit()
if __name__ == "__main__":
    main()
