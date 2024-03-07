# The Book Nook

**The Book Nook** is a small virtual library where a user can search for and borrow a book.  

![Program Startup Screenshot](/documents/program_screenshot.JPG)

The user has the option to log in to an existing account or create a new one.  Once logged in they can search for book titles. 

The site can be accessed by this [link](https://the-book-nook-f0acb363dd7b.herokuapp.com/).


## Contents

* [User Stories](#user-stories)
    * [First-Time User Goals](#first-time-user-goals)
    * [Returning User Goals](#returning-user-goals)
* [Features](#features)
    * [Existing Features](#existing-features)
    * [Future Features](#future-features)
* [Concept](#concept)
    * [Flow Chart](#flow-chart)
    * [Colors](#colors)
* [Testing](#testing)
    * [Manual Testing](#manual-testing)
    * [Bugs](#bugs)
    * [Validator Testing](#validator-testing)
* [Technologies Used](#technologies-used)
* [Deployment](#deployment)
* [Future Improvements](#future-improvements)
* [Credits](#credits)
* [Tools](#tools)
* [Acknowledgments](#acknowledgments)

    

## User Stories

### First-Time User Goals:
- As a First Time User, I want the program to be easy to read and intuitive to navigate to ensure a pleasant user experience.
- As a First Time User, I want to easily create an account.
- As a First Time User, I want to be able to borrow a book.

### Returning User Goals:
- As a Returning User, I want to be able to log in to my previously made account.
- As a Returning User, I want to see if a book I've had my eye on for a while which was previously unavailable is available to borrow.


## Features

### Existing Features
- Welcome Message with a prompt asking a user if they have visited before.    
    - Inputting 'yes' will prompt the user to enter their username and password.
    - Inputting 'no' will allow the user to create an account.
        - Validation functions ensure inputs meet the prompted requirements.
    - Any other response prompts a message stating a 'yes' or 'no' response is required.
- After login, a user can search for books by title.  
    - If the book is available the user will have the option to check it out.
    - If a book is unavailable the user will be informed of the return date.
    - If a title is not found the user will be prompted to try again and informed that titles are case sensitive.
- After searching for a book and taking one of the first two steps above, the user is given the option to search again or exit the program.  Choosing to exit begins the program again.
- Program data is stored on Google Sheets.
    - Users are saved in this format (this example can be used to log in to an existing account):

    ![Users Spreadsheet Example](/documents/users_sheet.png)

    - Books are saved in this format:

    ![Books Spreadsheet Example](/documents/books_sheet.png)

    
    - A copy of the spreadsheet has been uploaded to the repository and can be downloaded [here](/documents/the-book-nook.xlsx).


### Future Features
- Give a user the option to manually return a book. 
- Using a feature like password hashing so passwords are stored and displayed more securely.


## Concept
### Flowchart
The original idea for the project can be seen in the basic flowchart below.  Specific functions and more detailed processes were added while writing the code.

![Flowchart](/documents/flowchart.png)

### Colors
Colorama was used to add color to the program.
- Error messages appear in red to make them more noticeable to the user.
- Positive messages, if a book is available for example, appear in green.
- Important notes to the user appear in yellow, for example noting that book titles must appear as they do on the book.
- The first prints from the program appear in cyan to make them different from the other text and appeal more to the user.


## Testing

### Manual Testing
#### Testing User Stories: First Time Visitors
| User Goal | How It Is Achieved |
| ---| ---|
| As a First Time User, I want the program to be easy to read and intuitive to navigate to ensure a pleasant user experience. | Colorama styles break up the text in the console and the prompts are descriptive and easy to understand. |
| As a First Time User, I want to easily create an account. | The user is walked through creating an account step by step with prompts, and error messages in red tell them when they need to edit their response. |
| As a First Time User, I want to be able to borrow a book. | After creating an account the user is prompted to search titles from the library and can check out any available ones. |


#### Testing User Stories: Returning Visitors
| User Goal | How It Is Achieved |
| ---| ---|
| As a Returning User, I want to be able to log in to my previously made account. | If a user states that they have used the program before they will be prompted to log in using their existing username and password. |
| As a Returning User, I want to see if a book I've had my eye on for a while which was previously unavailable is available to borrow. | The return date for the books is updated automatically on starting the program, any dates which have passed are removed and availability is set to 'Yes'. |


#### Full Testing

Full Testing was performed on the following physical devices.

##### Devices Tested:
- Windows PC with 32” Monitor
- Poco M4 Pro
- Windows laptop 17”

#### Functionality Tests
- All functions were tested frequently at the time of writing by using print statements to check if they were functioning as expected from writing the basic outline of the function through to testing the completed function.
- A Google spreadsheet with minimal rows of data was used to test functionality before more books were added.

### Bugs
#### Solved Bugs
| Bug | Solution |
| ---| ---|
| All books in the spreadsheet were flagged as unavailable whether availability was 'no' or not. | Solution: Used .value() to return the cell value to be able to compare it to the string used in the function. |
| The program crashed when trying to update the books spreadsheet and when running the function to update the return dates. | Used .strptime() to ensure the date format in the code matched the date format of the spreadsheet. Checked the cell format on the spreadsheet when the error persisted and ensured the entire column was formatted the same way. |
| Running the update returns function just resulted in an error on the console. | After running some more tests and Googling the error messages, the empty cells in the column were found to be preventing the function from working.  Adding an extra if statement to only have the function look for cells with dates resolved the issue. |

#### Unsolved Bugs
No unsolved bugs were detected after testing.

### Validator Testing
- The program was tested using [PEP8](https://pep8ci.herokuapp.com/). No errors were found.
- A screenshot of the results can be found [here](/documents/PEP8_validation.png).


## Technologies Used
- VSCode was used as the main tool to write and edit code.
- Git was used for the version control of the program.
- GitHub was used to host the code of the program.
- Heroku was used to deploy the program.

## Deployment
This project was deployed using Code Institute's mock terminal for Heroku.

The steps to deploy are as follows:
- Fork or clone this repository.
- Create a new Heroku app.
- Set the buildbacks to Python and NodeJS, in that order.
- Link the repository to the Heroku app.
- Click the deploy button. 

The live link can be found [here](https://the-book-nook-f0acb363dd7b.herokuapp.com/).

## Future improvements
- In the future, I would like to be able to implement more thorough user input validation.  At present validation is very simple and could be manipulated by a user.  For example, instead of checking for an email specifically the current validation checks if the inputted text contains '@'.  While this works for now, I would like to improve this as I learn more.
- I would also like to implement a feature where a user can search for books by author, right now searches can only be completed by book name.
- I would also like to give users more leeway when searching for books.  I think this is important from an accessibility standpoint as right now the title needs to be searched exactly as it appears in the spreadsheet.  Being able to incorporate all cases and even minor spelling mistakes when searching would improve the user experience.
- For future projects, I would like to improve my commit messages.  I was very focused at the beginning of the project and would write a function and change it until it worked and then commit it.  This resulted in one commit message per function, which I think can be improved on next time.

## Credit
- Using `strftime()` learned from [Programiz](https://www.programiz.com/python-programming/datetime/strftime).
- Updating Google spreadsheets learned from [Pretty Printed](https://www.youtube.com/watch?v=yPQ2Gk33b1U) and [Worth Web Scraping - Mike](https://www.youtube.com/watch?v=3OnT1PfDrfE) on YouTube.
- Checking a username and password against spreadsheet data adapted for this project from a post on [StackOverflow](https://stackoverflow.com/questions/73587363/comparing-password-cell-to-username-cell-in-excel-using-python).
- Validating to see if the input is alphabetic with a space also adapted from a post on [StackOverflow](https://stackoverflow.com/questions/59495030/combine-isalpha-and-isspace-into-1-statement).
- Calculating the difference between two dates to generate the return date adapted from [GeeksforGeeks](https://www.geeksforgeeks.org/python-difference-between-two-dates-in-minutes-using-datetime-timedelta-method/).
- Colorama guide found on [LinuxHint](https://linuxhint.com/colorama-python/).

## Tools
- [Lucid Chart](https://www.lucidchart.com/pages/examples/flowchart-maker) was used to create the flowchart.

## Acknowledgments
- This project was completed with the guidance of my mentor, Rory Patrick Sheridan.  His feedback was invaluable and his guidance made completing this project a very educational experience.
- User testing was completed by my fiancé, Caolán Curran.  His feedback enabled me to improve the program and create a more pleasant user experience.  He also compiled the list of books seen in the final project.
