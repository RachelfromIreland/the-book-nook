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
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True