from db_config import get_connection
import re
import bcrypt
from datetime import date

def email_exists(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM member WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.(com|co\.in)$'
    return re.match(pattern, email)

def add_member(name, email, password, confirm_password):
    if not name or not email or not password or not confirm_password:
        raise ValueError("All fields are required.")

    if not is_valid_email(email):
        raise ValueError("Invalid email format. Must contain @ and end with .com or .co.in")

    if email_exists(email):
        raise ValueError("This email is already registered. Please use a different email.")

    if password != confirm_password:
        raise ValueError("Passwords do not match.")

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    join_date = date.today()

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO member (name, email, password, hash_pw, join_date) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, password, hashed_pw, join_date))
    conn.commit()
    cursor.close()
    conn.close()

    
    

def view_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT member_id, name, email, join_date
        FROM member
        ORDER BY member_id
    """)
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return members
