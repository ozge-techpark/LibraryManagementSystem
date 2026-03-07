import sys
from models.member import Member
from models.book import Book
from models.author import Author
from models.loan import Loan

def manager_menu():
    while True:
        print("1. Add Author")
        print("2. Add Book")
        print("3. List All Books")
        print("4. Logout")

        choice = input("Select an option: ")

        if choice == '1':
            name = input("Enter an Author name: ")
            Author.add_author(name)
        elif choice == '2':
            title = input("Enter a book title: ")
            author_id = input("Enter author ID: ")
            Book.add_book(title, author_id)
        elif choice == '3':
            books = Book.list_books()
            print("All books in the library: ")
            for book in books:
                status = "Available" if book[3] == 1 else "on loan"
                print(f"ID: {book[0]} | Title: {book[1]} | Status: {status}")
        elif choice == '4':
            print("Loging out..")
            break
def member_menu(member_id):
    while True:
        print("1. List All Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. Logout")

        choice = input("Select an option: ")

        if choice == '1':
            books = Book.list_books()
            for book in books:
                status = "Available" if book[3] == 1 else "On Loan"
                print(f"ID: {book[0]} | Title: {book[1]} | Status: {status}")
        elif choice == '2':
            book_id = input("Enter Book ID to borrow: ")
            Loan.borrow_book(book_id, member_id)
        elif choice == '3':
            loan_id = input("Enter Loan ID to return: ")
            Loan.return_book(loan_id)
        elif choice == '4':
            print("Loging out..")
            break
def main():
    while True:
        print("Welcome to Library System")
        print("1. Login ")
        print("2. Exit")

        start_choice = input("Select: ")
        if start_choice == '1':
            email = input("Email: ")
            password = input("Password: ")

            user = Member.login(email,password)
            if user:
                member_id, name, role = user
                print(f"Login successful. Welcome, {name} ({role})")

                if role == 'manager':
                    manager_menu()
                else:
                    member_menu()
            else:
                print("Error: Invalid emsil or password")
        elif start_choice == '2':
            sys.exit()
if __name__ == "__main__":
    main()
