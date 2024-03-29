"""
Imports for python to run the program
"""
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Style

# Initialise colorama
colorama.init()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('the-book-nook')

# Global variables to access spreadsheets
books = SHEET.worksheet('Books')
users = SHEET.worksheet('Users')


def update_returns():
    """
    Function to iterate through books spreadsheet and reset borrower
    information if past the return date
    """
    today = datetime.now().date()

    # Get all values except header from Books
    books_data = books.get_all_values()[1:]

    for row in books_data:
        return_date_value = row[4]

        if return_date_value.strip():
            # Convert date string to date
            return_date = datetime.strptime(
                return_date_value, "%d-%m-%Y").date()

            # Updating spreadsheet learned from Youtube, link in README
            # Set availability to Yes if past return date
            if return_date < today:
                books.update_cell(
                    books_data.index(row) + 2, 3, "Yes")

                # Clear username and return date if book is available
                books.update_cell(
                    books_data.index(row) + 2, 4, "")
                books.update_cell(
                    books_data.index(row) + 2, 5, "")

        else:
            continue


def login():
    """
    Checks to see if a user has registered before and if not will call a
    function to create an account.
    Logs in existing users.
    """
    print(Fore.CYAN + Style.BRIGHT +
          "Have you borrowed from The Book Nook before? (yes/no)")
    print(Style.RESET_ALL)
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
                print(Fore.GREEN + Style.BRIGHT + "User logged in.")
                print(Style.RESET_ALL)
                is_book_available(username)
                return username, password

        print(Fore.RED + Style.BRIGHT +
              "Check your details are correct, or create account to continue.")
        print(Style.RESET_ALL)
        login()

    else:
        print(Fore.RED + Style.BRIGHT + "Please only enter 'yes' or 'no'.")
        print(Style.RESET_ALL)
        login()


def create_account():
    """
    Allows a new user to create an account
    """
    print("Please enter your details using the prompts below.")

    username = validate_username_input()
    name = validate_name_input()
    email = validate_email_input()
    address = validate_address_input()
    phone = validate_phone_input()
    password = validate_password_input()

    # Add inputs from user to the Users sheet
    users.append_row([username, name, email, address, phone, password])

    print(Fore.GREEN + Style.BRIGHT +
          "\nThank you! Your account has been created "
          "and you can search books")
    print(Style.RESET_ALL)

    is_book_available(username)
    return username, password


def validate_username_input():
    """
    Validates username to check it isn't already in the users spreadsheet
    and checks length is less than 20 characters
    """
    while True:
        try:
            username = input("\nUsername: ")

            # Check if username already exists in spreadsheet
            if username in [user[0] for user in users.get_all_values()[1:]]:
                raise ValueError("Sorry, that username is taken.  Please try"
                                 " another.")

            if len(username) > 20:
                raise ValueError("Username must be 20 characters or less.")

            return username

        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + str(e))
            print(Style.RESET_ALL)


def validate_name_input():
    """
    Validates Name input to check it only uses albhabetic characters
    and is less than 50 characters long
    """
    while True:
        try:
            name = input("\nFull name: ")
            # Checking to see if only alpabetic and spaces
            # Learned from stackoverflow - link in README
            if not all(char.isalpha() or char.isspace() for char in name):
                raise ValueError("Please use only alphabetic characters.")

            if len(name) > 50:
                raise ValueError(
                    "Name should be less than 50 characters long.")
            return name
        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + str(e))
            print(Style.RESET_ALL)


def validate_email_input():
    """
    Validates Email input to check it contains @ and is less than 50
    characters long
    """
    while True:
        try:
            email = input("\nEmail: ")

            if "@" not in email:
                raise ValueError("Please enter a valid email.")

            if len(email) > 50:
                raise ValueError(
                    "Email should be less than 50 characters long.")
            return email
        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + str(e))
            print(Style.RESET_ALL)


def validate_address_input():
    """
    Validates Address input to check it contains ','
    and is less than 100 characters long
    """
    print(Fore.YELLOW + Style.BRIGHT +
          "\nPlease separate lines in your shipping address with a comma.")
    print(Style.RESET_ALL)
    while True:
        try:
            address = input("Address: ")

            if "," not in address:
                raise ValueError("Please separate address lines with a comma"
                                 "(,) for shipping.")

            if len(address) > 100:
                raise ValueError(
                    "Address should be less than 100 characters long.")
            return address
        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + str(e))
            print(Style.RESET_ALL)


def validate_phone_input():
    """
    Validates Phone input to check if numeric
    and is less than 15 characters long
    """
    while True:
        try:
            phone = input("\nPhone: ")

            if not phone.isnumeric() or len(phone) > 12:
                raise ValueError("Please enter a valid phone number.")

            return phone
        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + str(e))
            print(Style.RESET_ALL)


def validate_password_input():
    """
    Check password contains both upper and lowercase letters, a number
    and is at least 8 characters long
    """
    while True:
        try:
            password = input("\nPassword: ")

            if len(password) < 8:
                raise ValueError(
                    "Password must be at least 8 characters long.")

            if not any(character.islower() for character in password):
                raise ValueError("Password must contain at least one"
                                 " lowercase letter.")

            if not any(character.isupper() for character in password):
                raise ValueError(
                    "Password must contain at least one uppercase letter.")

            if not any(character.isnumeric() for character in password):
                raise ValueError("Password must contain at least one digit.")

            return password

        except ValueError as e:
            print(Fore.RED + Style.BRIGHT + str(e))
            print(Style.RESET_ALL)


def is_book_available(username):
    """
    Check if the book title is available
    Run a while loop to get a book input that exists in the library
    """
    while True:
        print("Please enter the name of the book you wish to check, or enter"
              " 'exit' to Exit.")

        print(Fore.YELLOW + Style.BRIGHT +
              "Ensure the title you input appears as it does on the book.")
        print(Style.RESET_ALL)

        title = input("Enter book title here: ")

        if title.lower() == 'exit':
            print("\nThank you for visiting.  Returning to main menu...\n")
            login()

        if check_title(title):
            print(Fore.GREEN + Style.BRIGHT +
                  "Book found! Checking availability...")
            print(Style.RESET_ALL)
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
                             f"library.\nPlease check spelling and try again."
                             f"\nNOTE! Titles are case sensitive")

    except ValueError as e:
        print(Fore.YELLOW + Style.BRIGHT + f"Sorry! {e}\n")
        print(Style.RESET_ALL)
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
        print(Fore.GREEN + Style.BRIGHT + f"The book '{title}' is available!")
        print(Style.RESET_ALL)
        borrow_book(title, username)

    else:
        print(Fore.YELLOW + Style.BRIGHT +
              f"The book '{title}' is checked out.\n"
              f"It will be available again on {date_for_book}.")
        print(Style.RESET_ALL)
        another_book(username)


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
        print(Fore.RED + Style.BRIGHT + "Please answer 'yes' or 'no'.")
        print(Style.RESET_ALL)


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
    return_date_str = return_date.strftime("%d-%m-%Y")

    # Update book availability to "no"
    # Add username and return date to relevant cells
    books.update_cell(borrowed_book.row, 3, "No")
    books.update_cell(borrowed_book.row, 4, username)
    books.update_cell(borrowed_book.row, 5, return_date_str)

    print(Fore.GREEN + Style.BRIGHT +
          f"You have borrowed {title}.\nThis book is due back on "
          f"{return_date_str}.\nThank you for using the Book Nook!")
    print(Style.RESET_ALL)

    another_book(username)


def another_book(username):
    """
    Gives the user the option to select another book after checking one out
    """
    print("Would you like to select another book? (yes/no)")
    extra_book = input().lower()

    # If new user will be prompted to create an account.
    if extra_book == "no":
        print("Thank you for using The Book Nook.\n")
        main()

    elif extra_book == "yes":
        is_book_available(username)

    else:
        print("Please only enter 'yes' or 'no'.")


def main():
    """
    Run all program functions
    """
    update_returns()
    print(Fore.CYAN + Style.BRIGHT +
          "Welcome to The Book Nook!\nBorrow from our range of classic books.")
    print(Style.RESET_ALL)
    login()


main()
