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
transactions = SHEET.worksheet('Transactions')

def is_book_available():
    """
    Check if the book title is available
    Run a while loop to get a book input that exists in the library
    """
    while True:
        print("Please enter the name of the book you wish to check.")
        print("Ensure the title you input appears as it does on the book cover.")

        title = input("Enter book title here:\n")

        if validate_title(title):
            print("Book found! Checking availability...")
            get_book_info(title)

            return title
    

def validate_title(title):
    """
    Check if provided book title exists in the books spreadsheet
    """
    try:
        books = SHEET.worksheet('Books')
        if not books.find(title):
            raise ValueError(f"The book '{title}' was not found in the library.\nPlease check spelling and try again.")
        
    except ValueError as e:
        print(f"Sorry! {e}\n")
        return False
    
    return True

def get_book_info(title):
    """
    Checks book info after book title is found, returns date available to user
    """
    books = SHEET.worksheet('Books')
    book_info = books.find(title)
    is_available = books.cell(book_info.row, 3)
    date_for_book = books.cell(book_info.row, 5).value

    if is_available == "Yes":
        print(f"The book '{title}' is available!")
        is_new_user()
    else:
        print(f"The book '{title}' is checked out.\nIt will be available again on {date_for_book}.")

def is_new_user():
    """
    Checks to see if a user has registered before and if not will call a funtion to create an account.
    Logs in existing users
    """
    print("Have you borrowed from The Book Nook before? (yes/no)")
    new_user = input().lower()

    #If new user will be prompted to create an account.  WRITE NEW ACCOUNT FUNCTION LATER
    if new_user == "no":
        print("You will need to create an account.")

    #If existing user will be prompted to log in and info checked against users sheet
    #Checking username and password against spreadsheet adapted from stackoverflow - link in README
    elif new_user == "yes":
        print("Please enter your username and password below.")
        username = input("Username: ")
        password = input("Password: ")

        user_info = users.get_all_values()
        for info in user_info[1:]:
            if info[0] == username and info[5] ==password:
                print("User logged in.")
                return username, password
        
        print("No record of user, must create account to continue.")
        return is_new_user()
    
    else:
        print("Please only enter 'yes' or 'no'.")
        return is_new_user()

is_book_available()