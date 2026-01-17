import bcrypt
from db_config import get_connection
from datetime import datetime, date
from decimal import Decimal

# ---------- Utility Functions ----------

def book_exists(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM book WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def member_exists(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM member WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_available_copies(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT available_copies FROM book WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

# ---------- Borrow Book ----------

def borrow_book(book_id, member_id, password, borrow_date_input):
    if not book_id.isdigit() or not member_id.isdigit():
        raise ValueError("Book ID and Member ID must be numeric.")

    book_id = int(book_id)
    member_id = int(member_id)

    if not book_exists(book_id):
        raise ValueError("Book ID does not exist.")
    if not member_exists(member_id):
        raise ValueError("Member ID does not exist.")

    # Authenticate password
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hash_pw FROM member WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result or not bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        raise ValueError("Incorrect password.")

    # Parse borrow date
    try:
        borrow_date = datetime.strptime(borrow_date_input, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    # Check availability
    available = get_available_copies(book_id)
    if available <= 0:
        raise ValueError("No copies available for this book.")

    # Borrow the book
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO borrow (book_id, member_id, borrow_date, status) VALUES (%s, %s, %s, %s)",
            (book_id, member_id, borrow_date, 'Not Returned')
        )
        cursor.execute("UPDATE book SET available_copies = available_copies - 1 WHERE book_id = %s", (book_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# ---------- Return Book ----------

def return_book(borrow_id, return_date_input):
    if not borrow_id.isdigit():
        raise ValueError("Borrow ID must be numeric.")

    borrow_id = int(borrow_id)

    try:
        return_date = datetime.strptime(return_date_input, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid return date format. Use YYYY-MM-DD.")

    if return_date > date.today():
        raise ValueError("Return date cannot be in the future.")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Get borrow date and book ID
        cursor.execute("SELECT borrow_date, book_id FROM borrow WHERE borrow_id = %s", (borrow_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError("Borrow ID not found.")

        borrow_date, book_id = result
        no_of_days = (return_date - borrow_date).days
        if no_of_days < 0:
            raise ValueError("Return date cannot be before borrow date.")

        # Get book price
        cursor.execute("SELECT price FROM book WHERE book_id = %s", (book_id,))
        price_result = cursor.fetchone()
        if not price_result:
            raise ValueError("Book not found.")

        book_price = price_result[0]
        price_to_pay = round(no_of_days * (book_price * Decimal('0.02')), 2)

        # Update borrow record
        cursor.execute("""
            UPDATE borrow
            SET return_date = %s, no_of_days = %s, price_to_pay = %s, status = 'Returned'
            WHERE borrow_id = %s
        """, (return_date, no_of_days, price_to_pay, borrow_id))

        # Increment available copies
        cursor.execute("UPDATE book SET available_copies = available_copies + 1 WHERE book_id = %s", (book_id,))
        conn.commit()

        return {
            "days_borrowed": no_of_days,
            "price_to_pay": float(price_to_pay)
        }

    finally:
        cursor.close()
        conn.close()

# ---------- View Borrowed Books ----------

def view_borrowed_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT br.borrow_id, b.title, m.name, br.borrow_date, br.return_date, br.status
        FROM borrow br
        JOIN book b ON br.book_id = b.book_id
        JOIN member m ON br.member_id = m.member_id
        ORDER BY br.borrow_id
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
    
    
    
def check_book_availability(book_id):
    if not str(book_id).isdigit():
        raise ValueError("Invalid book ID. Please enter a numeric value.")

    book_id = int(book_id)

    if not book_exists(book_id):
        raise ValueError("Book ID does not exist.")

    available = get_available_copies(book_id)
    return available

