import customtkinter
from PIL import Image
from tkinter import messagebox
from author import add_author, view_authors
from book import add_book, view_books, add_book_copies
from member import add_member, view_members
from borrow import borrow_book, return_book, view_borrowed_books, check_book_availability


class LibraryGUI:
    def __init__(self):
        # Theme setup
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        # Main window
        self.window = customtkinter.CTk()
        self.window.geometry("1450x1080")
        self.window.title("Library Management System")
        self.window.wm_iconbitmap("library_icon.ico")

        # Background image
        bg_image = customtkinter.CTkImage(light_image=Image.open("library_bg.jpg"), size=(1450, 1080))
        bg_label = customtkinter.CTkLabel(self.window, image=bg_image, text="")
        bg_label.pack()

        # Main frame
        self.main_frame = customtkinter.CTkFrame(master=bg_label, width=900, height=700, corner_radius=20, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = customtkinter.CTkLabel(self.main_frame, text="Library Management System", font=("Montserrat", 26, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 40))

        # Menu buttons
        menu_items = [
            ("Add Author", self.add_author),
            ("View Authors", self.view_authors),
            ("Add Book", self.add_book),
            ("Add Book Copies", self.add_book_copies),
            ("View Books", self.view_books),
            ("Add Member", self.add_member),
            ("View Members", self.view_members),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("View Borrowed Books", self.view_borrowed_books),
            ("Check Book Availability", self.check_availability),
            ("Exit", self.window.quit)
        ]

        # Grid placement for all except Exit
        for index, (label, command) in enumerate(menu_items[:-1]):  # skip Exit
            row = index // 2 + 1
            col = index % 2
            button = customtkinter.CTkButton(
                self.main_frame,
                text=label,
                command=command,
                width=250,
                height=40,
                fg_color="black"
            )
            button.grid(row=row, column=col, padx=20, pady=10)

        # Center only Exit button
        exit_label, exit_command = menu_items[-1]
        exit_button = customtkinter.CTkButton(
            self.main_frame,
            text=exit_label,
            command=exit_command,
            width=300,
            height=40,
            fg_color="red"
        )
        exit_button.grid(row=(len(menu_items)//2)+2, column=0, columnspan=2, pady=20)

        # Center columns
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        self.window.mainloop()

    # Placeholder methods
    #def add_author(self):
        #messagebox.showinfo("Add Author", "This will open the Add Author form.")
    def add_author(self):
        add_window = customtkinter.CTkToplevel(self.window)
        add_window.title("Add Author")
        add_window.geometry("400x350")
        
        
        add_window.lift()
        add_window.grab_set()

        name_label = customtkinter.CTkLabel(add_window, text="Author Name:")
        name_label.pack(pady=(20, 5))
        name_entry = customtkinter.CTkEntry(add_window, width=300)
        name_entry.pack()

        country_label = customtkinter.CTkLabel(add_window, text="Country:")
        country_label.pack(pady=(20, 5))
        country_entry = customtkinter.CTkEntry(add_window, width=300)
        country_entry.pack()

        birth_label = customtkinter.CTkLabel(add_window, text="Birth Year:")
        birth_label.pack(pady=(20, 5))
        birth_entry = customtkinter.CTkEntry(add_window, width=300)
        birth_entry.pack()

        def save_author():
            name = name_entry.get().strip()
            country = country_entry.get().strip()
            birth_year = birth_entry.get().strip()

            try:
                add_author(name, country, birth_year)
                messagebox.showinfo("Success", f"Author '{name}' added successfully!")
                add_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add author:\n{e}")

        save_button = customtkinter.CTkButton(add_window, text="Save Author", command=save_author)
        save_button.pack(pady=30)

    

    def view_authors(self):
        view_window = customtkinter.CTkToplevel(self.window)
        view_window.title("View Authors")
        view_window.geometry("650x500")
        
        view_window.lift()
        view_window.grab_set()
        
        title = customtkinter.CTkLabel(view_window, text="All Authors", font=("Montserrat", 20, "bold"))
        title.pack(pady=10)

        scroll_frame = customtkinter.CTkScrollableFrame(view_window, width=600, height=400)
        scroll_frame.pack(pady=10)

        # Table headers
        headers = ["Author ID", "Name", "Country", "Birth Year"]
        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(scroll_frame, text=header, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        # Fetch and display authors
        try:
            authors = view_authors()
            for row_index, author in enumerate(authors, start=1):
                for col_index, value in enumerate(author):
                    cell = customtkinter.CTkLabel(scroll_frame, text=str(value), font=("Arial", 12))
                    cell.grid(row=row_index, column=col_index, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch authors:\n{e}")



    
    

    def add_book(self):
        book_window = customtkinter.CTkToplevel(self.window)
        book_window.title("Add Book")
        book_window.geometry("450x600")

        book_window.lift()
        book_window.grab_set()
        
        
        
        def add_field(label_text):
            label = customtkinter.CTkLabel(book_window, text=label_text)
            label.pack(pady=(15, 5))
            entry = customtkinter.CTkEntry(book_window, width=300)
            entry.pack()
            return entry

        title_entry = add_field("Title:")
        genre_entry = add_field("Genre:")
        year_entry = add_field("Published Year:")
        price_entry = add_field("Price:")
        author_id_entry = add_field("Author ID:")
        copies_entry = add_field("Available Copies:")

        def save_book():
            title = title_entry.get().strip()
            genre = genre_entry.get().strip()
            year = year_entry.get().strip()
            price = price_entry.get().strip()
            author_id = author_id_entry.get().strip()
            copies = copies_entry.get().strip()

            try:
                add_book(title, genre, year, price, author_id, copies)
                messagebox.showinfo("Success", f"Book '{title}' added successfully!")
                book_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add book:\n{e}")

        save_button = customtkinter.CTkButton(book_window, text="Save Book", command=save_book)
        save_button.pack(pady=30)



    

    def view_books(self):
        view_window = customtkinter.CTkToplevel(self.window)
        view_window.title("View Books")
        view_window.geometry("900x500")

        view_window.transient(self.window)
        view_window.grab_set()
        view_window.focus_force()
        view_window.lift()
        view_window.attributes("-topmost", True)

        title = customtkinter.CTkLabel(view_window, text="All Books", font=("Montserrat", 20, "bold"))
        title.pack(pady=10)

        scroll_frame = customtkinter.CTkScrollableFrame(view_window, width=850, height=400)
        scroll_frame.pack(pady=10)

        headers = ["Book ID", "Title", "Genre", "Year", "Price", "Author ID", "Available Copies"]
        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(scroll_frame, text=header, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        try:
            books = view_books()
            for row_index, book in enumerate(books, start=1):
                for col_index, value in enumerate(book):
                    cell = customtkinter.CTkLabel(scroll_frame, text=str(value), font=("Arial", 12))
                    cell.grid(row=row_index, column=col_index, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch books:\n{e}")

    def create_popup(self, title, size="400x300"):
        popup = customtkinter.CTkToplevel(self.window)
        popup.title(title)
        popup.geometry(size)
        popup.transient(self.window)
        popup.grab_set()
        popup.focus_force()
        popup.lift()
        popup.attributes("-topmost", True)
        return popup

    def add_book_copies(self):
        # Create popup window
        copies_window = self.create_popup("Add Book Copies", "400x300")

        # Book ID field
        book_id_label = customtkinter.CTkLabel(copies_window, text="Book ID:")
        book_id_label.pack(pady=(20, 5))
        book_id_entry = customtkinter.CTkEntry(copies_window, width=250)
        book_id_entry.pack()

        # Copies field
        copies_label = customtkinter.CTkLabel(copies_window, text="Number of Copies:")
        copies_label.pack(pady=(20, 5))
        copies_entry = customtkinter.CTkEntry(copies_window, width=250)
        copies_entry.pack()

        # Save function
        def save_copies():
            book_id = book_id_entry.get().strip()
            no_of_copies = copies_entry.get().strip()

            if not book_id.isdigit():
                messagebox.showerror("Input Error", "Book ID must be numeric.")
                return
            if not no_of_copies.isdigit():
                messagebox.showerror("Input Error", "Number of copies must be numeric.")
                return

            try:
                # Call your backend function
                add_book_copies(book_id, no_of_copies)
                messagebox.showinfo("Success", f"Book ID {book_id} updated with {no_of_copies} copies!")
                copies_window.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to update copies:\n{e}")

        # Save button
        save_button = customtkinter.CTkButton(copies_window, text="Update Copies", command=save_copies)
        save_button.pack(pady=30)



    
    

    def add_member(self):
        member_window = customtkinter.CTkToplevel(self.window)
        member_window.title("Add Member")
        member_window.geometry("450x600")

        member_window.transient(self.window)
        member_window.grab_set()
        member_window.focus_force()
        member_window.lift()
        member_window.attributes("-topmost", True)

        def add_field(label_text, show=None):
            label = customtkinter.CTkLabel(member_window, text=label_text)
            label.pack(pady=(15, 5))
            entry = customtkinter.CTkEntry(member_window, width=300, show=show)
            entry.pack()
            return entry

        name_entry = add_field("Name:")
        email_entry = add_field("Email:")
        password_entry = add_field("Password:", show="*")
        confirm_entry = add_field("Confirm Password:", show="*")

        def save_member():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()

            try:
                add_member(name, email, password, confirm)
                messagebox.showinfo("Success", f"Member '{name}' added successfully!")
                member_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add member:\n{e}")

        save_button = customtkinter.CTkButton(member_window, text="Save Member", command=save_member)
        save_button.pack(pady=30)


    

    def view_members(self):
        view_window = customtkinter.CTkToplevel(self.window)
        view_window.title("View Members")
        view_window.geometry("800x500")

        view_window.transient(self.window)
        view_window.grab_set()
        view_window.focus_force()
        view_window.lift()
        view_window.attributes("-topmost", True)

        title = customtkinter.CTkLabel(view_window, text="All Members", font=("Montserrat", 20, "bold"))
        title.pack(pady=10)

        scroll_frame = customtkinter.CTkScrollableFrame(view_window, width=750, height=400)
        scroll_frame.pack(pady=10)

        headers = ["Member ID", "Name", "Email", "Join Date"]
        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(scroll_frame, text=header, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        try:
            members = view_members()
            for row_index, member in enumerate(members, start=1):
                for col_index, value in enumerate(member):
                    cell = customtkinter.CTkLabel(scroll_frame, text=str(value), font=("Arial", 12))
                    cell.grid(row=row_index, column=col_index, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch members:\n{e}")


   

    def borrow_book(self):
        borrow_window = customtkinter.CTkToplevel(self.window)
        borrow_window.title("Borrow Book")
        borrow_window.geometry("450x600")

        borrow_window.transient(self.window)
        borrow_window.grab_set()
        borrow_window.focus_force()
        borrow_window.lift()
        borrow_window.attributes("-topmost", True)

        def add_field(label_text, show=None):
            label = customtkinter.CTkLabel(borrow_window, text=label_text)
            label.pack(pady=(15, 5))
            entry = customtkinter.CTkEntry(borrow_window, width=300, show=show)
            entry.pack()
            return entry

        book_id_entry = add_field("Book ID:")
        member_id_entry = add_field("Member ID:")
        password_entry = add_field("Password:", show="*")
        borrow_date_entry = add_field("Borrow Date (YYYY-MM-DD):")

        def submit_borrow():
            book_id = book_id_entry.get().strip()
            member_id = member_id_entry.get().strip()
            password = password_entry.get().strip()
            borrow_date = borrow_date_entry.get().strip()

            try:
                # You’ll need to refactor your borrow_book() to accept these as parameters
                borrow_book(book_id, member_id, password, borrow_date)
                messagebox.showinfo("Success", "Book borrowed successfully!")
                borrow_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to borrow book:\n{e}")

        submit_button = customtkinter.CTkButton(borrow_window, text="Borrow Book", command=submit_borrow)
        submit_button.pack(pady=30)


    
    def return_book(self):
        return_window = customtkinter.CTkToplevel(self.window)
        return_window.title("Return Book")
        return_window.geometry("450x400")

        return_window.transient(self.window)
        return_window.grab_set()
        return_window.focus_force()
        return_window.lift()
        return_window.attributes("-topmost", True)

        def add_field(label_text):
            label = customtkinter.CTkLabel(return_window, text=label_text)
            label.pack(pady=(15, 5))
            entry = customtkinter.CTkEntry(return_window, width=300)
            entry.pack()
            return entry

        borrow_id_entry = add_field("Borrow ID:")
        return_date_entry = add_field("Return Date (YYYY-MM-DD):")

        def submit_return():
            borrow_id = borrow_id_entry.get().strip()
            return_date = return_date_entry.get().strip()

            try:
                result = return_book(borrow_id, return_date)
                messagebox.showinfo(
                    "Book Returned",
                    f"Book returned successfully!\n\nDays borrowed: {result['days_borrowed']}\nPrice to pay: ₹{result['price_to_pay']}"
                )
                return_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book:\n{e}")

        submit_button = customtkinter.CTkButton(return_window, text="Return Book", command=submit_return)
        submit_button.pack(pady=30)


    

    def view_borrowed_books(self):
        view_window = customtkinter.CTkToplevel(self.window)
        view_window.title("Borrowed Books")
        view_window.geometry("1000x500")

        view_window.transient(self.window)
        view_window.grab_set()
        view_window.focus_force()
        view_window.lift()
        view_window.attributes("-topmost", True)

        title = customtkinter.CTkLabel(view_window, text="Borrowed Books", font=("Montserrat", 20, "bold"))
        title.pack(pady=10)

        scroll_frame = customtkinter.CTkScrollableFrame(view_window, width=950, height=400)
        scroll_frame.pack(pady=10)

        headers = ["Borrow ID", "Book Title", "Member Name", "Borrow Date", "Return Date", "Status"]
        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(scroll_frame, text=header, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        try:
            records = view_borrowed_books()
            for row_index, row in enumerate(records, start=1):
                for col_index, value in enumerate(row):
                    cell = customtkinter.CTkLabel(scroll_frame, text=str(value) if value else "-", font=("Arial", 12))
                    cell.grid(row=row_index, column=col_index, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch borrowed books:\n{e}")



    def check_availability(self):
        popup = customtkinter.CTkToplevel(self.window)
        popup.title("Check Book Availability")
        popup.geometry("400x250")

        popup.transient(self.window)
        popup.grab_set()
        popup.focus_force()
        popup.lift()
        popup.attributes("-topmost", True)

        label = customtkinter.CTkLabel(popup, text="Enter Book ID to check availability:")
        label.pack(pady=(30, 10))

        book_id_entry = customtkinter.CTkEntry(popup, width=250)
        book_id_entry.pack()

        result_label = customtkinter.CTkLabel(popup, text="", font=("Arial", 14))
        result_label.pack(pady=20)

        def check():
            book_id = book_id_entry.get().strip()
            try:
                available = check_book_availability(book_id)
                result_label.configure(text=f"✅ {available} copies available", text_color="green")
            except ValueError as ve:
                result_label.configure(text=f"⚠️ {str(ve)}", text_color="orange")
            except Exception as e:
                result_label.configure(text=f"❌ Error: {e}", text_color="red")

        check_button = customtkinter.CTkButton(popup, text="Check Availability", command=check)
        check_button.pack(pady=10)


LibraryGUI()

