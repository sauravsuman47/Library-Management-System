--	Library Management System — (Python + MySQL + CustomTkinter)


	A full-featured desktop application to manage books, authors, members, and borrowing operations in a library.
	Built with Python, MySQL, and a modern GUI using CustomTkinter, this project demonstrates real-world CRUD operations,
	authentication, and data validation — all wrapped in a clean, user-friendly interface.



--	Features


*	Author Management

	Add and view authors with name, country, and birth year

*	Book Management

	Add books with genre, price, year, author, and available copies

	View all books with author names and availability

*	Member Registration

	Add members with email validation and password confirmation

	Passwords securely hashed using bcrypt

	View all registered members

*	Borrow & Return System

	Borrow books with member authentication

	Return books with calculation (2% of book price per day)

*	Tracks borrow/return dates, status("Returned" or "Not Returned")

*	Availability Checker

	Real-time check for available copies of any book by book ID

*	Borrowed Book History

	View all borrow records with book title, member name, dates, and status

--	Tech Stack

	Layer		Technology
	Language	Python 3.x
	GUI			CustomTkinter
	Database	MySQL
	Security	bcrypt (password hashing)
	Libraries	mysql-connector-python, tkinter, Pillow, re, decimal, datetime


Setup Instructions

Install dependencies(Mysql,Python)

--	Make sure you have these library installed

	customtkinter 
	mysql-connector-python 
	bcrypt 
	pillow

--	Set up MySQL database

	Create a database named library_db

	Run the SQL schema to create the following tables:

	author

	book

	member

	borrow
	
	To create table I already shared one db_setup.txt you can take the help of that.



--	Configure database connection

	Edit db_config.py with your MySQL credentials:

	python
	def get_connection():
		return mysql.connector.connect(
			host="localhost",
			user="your_mysql_user",
			password="your_mysql_password",
			database="library_db"
		)
--	Run the app in python terminal by giving below command.

	python GUI_customtk_main.py
	
	
	
Project Structure
Code
library-management-system/
│
├── db_config.py           # MySQL connection setup
├── author.py              # Author CRUD logic
├── book.py                # Book CRUD logic
├── member.py              # Member registration and validation
├── borrow.py              # Borrow/return logic and availability checks
├── GUI_customtk_main.py   # Main GUI application
├── library_bg.jpg         # Background image
├── library_icon.ico       # App icon
└── README.md              # Project documentation
└── db_setup.txt		   # Create sql tables
	
	
	
	About the Developer
	Saurav Suman  
	Aspiring Data Analyst | Python Developer | GUI Enthusiast
	Passionate about building real-world applications with clean UI and practical logic.
