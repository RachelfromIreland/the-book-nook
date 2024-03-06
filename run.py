"""
Imports for python to run the program
"""
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('the-book-nook')

books = SHEET.worksheet('Books')
users = SHEET.worksheet('Users')


def update_returns():
    """
    Function to iterate through books spreadsheet and reset borrower information
    if past the return date
    """
    today = datetime.now().date()

    # Find borrowed books by availabile column
    on_loan = books.findall("No")


def login():
    """
    Checks to see if a user has registered before and if not will call a
    function to create an account.
    Logs in existing users
    """
    print("Have you borrowed from The Book Nook before? (yes/no)")
    past_user = input().lower()

    # If new user will be prompted to create an account.
    if past_user == "no":
        print("You will need to create an account.")
        create_account()

    # If existing user will be prompted to log in and info checked against
    # users sheet
    # Checking username and password against spreadsheet adapted from
    # stackoverflow - link in README
    elif past_user == "yes":
        print("Please enter your username and password below.")
        username = input("Username: ")
        password = input("Password: ")

        user_info = users.get_all_values()
        for info in user_info[1:]:
            if info[0] == username and info[5] == password:
                print("User logged in.")
                is_book_available(username)
                return username, password

        print("No record of user, must create account to continue.")
        return login()

    else:
        print("Please only enter 'yes' or 'no'.")
        return login()


def create_account():
    """
    Allows a new user to create an account
    """
    print("Please enter your details using the prompts below.")
    print("Separate lines in your shipping address with a comma.")

    username = input("Username: ")
    name = input("Full name: ")
    email = input("Email: ")
    address = input("Address: ")
    phone = input("Phone: ")
    password = input("Password: ")

    # Add inputs from user to the Users sheet
    users.append_row([username, name, email, address, phone, password])

    print("Thank you! Your account has been created and you can search books")

    is_book_available(username)
    return username, password


def is_book_available(username):
    """
    Check if the book title is available
    Run a while loop to get a book input that exists in the library
    """
    while True:
        print("Please enter the name of the book you wish to check.")
        print("Ensure the title you input appears as it does on the book.")

        title = input("Enter book title here: ")

        if check_title(title):
            print("Book found! Checking availability...")
            get_book_info(title, username)

            return title, username


def check_title(title):
    """
    Check if provided book title exists in the books spreadsheet
    """
    try:
        book_list = SHEET.worksheet('Books')
        if not book_list.find(title):
            raise ValueError(f"The book '{title}' was not found in the"
                             f"library.\nPlease check spelling and try again.")

    except ValueError as e:
        print(f"Sorry! {e}\n")
        return False

    return True


def get_book_info(title, username):
    """
    Checks book info after book title is found, returns date available to user
    """
    book_info = books.find(title)
    book_availablity = books.cell(book_info.row, 3)
    date_for_book = books.cell(book_info.row, 5).value

    if book_availablity.value == "Yes":
        print(f"The book '{title}' is available!")
        borrow_book(title, username)

    else:
        print(f"The book '{title}' is checked out.\n"
              f"It will be available again on {date_for_book}.")


def borrow_book(title, username):
    """
    Asks the user if they would like to borrow the selected book
    """
    print("Would you like to borrow this book? (yes/no)")
    wants_book = input().lower()

    if wants_book == "yes":
        update_books_borrowed(title, username)

    elif wants_book == "no":
        is_book_available(username)

    else:
        print("Please answer 'yes' or 'no'.")


def update_books_borrowed(title, username):
    """
    Update the Books sheet if a user checks out a book
    """

    borrowed_book = books.find(title)

    # Get current date and calculate return date
    # Learned from geeksforgeeks - link in README
    today = datetime.now().date()
    return_date = today + timedelta(days=14)

    # Convert return date to a string - learned from programiz - link in README
    return_date_str = return_date.strftime("%Y:%m:%d")

    # Update book availability to "no"
    # Add username and return date to relevant cells
    books.update_cell(borrowed_book.row, 3, "No")
    books.update_cell(borrowed_book.row, 4, username)
    books.update_cell(borrowed_book.row, 5, return_date_str)

    print(f"You have borrowed {title}.\nThis book is due back on"
          "{return_date}.\nThank you for using the Book Nook!")


print("Welcome to The Book Nook!\nBorrow from our range of classic books.")
login()
