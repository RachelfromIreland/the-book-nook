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
    else:
        print(f"The book '{title}' is checked out.\nIt will be available again on {date_for_book}.")

is_book_available()