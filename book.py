from db_config import get_connection
import tkinter as tk
from tkinter import messagebox



def author_exists(author_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("Select 1 from author where author_id = %s",(author_id,))
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None






def add_book(title, genre, published_year, price, author_id, available_copies):
    if not title or not published_year.isdigit() or not price.replace('.', '', 1).isdigit() or not available_copies.isdigit():
        raise ValueError("Title, Published Year, Price, and Available Copies must be valid.")

    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO book (title, genre, published_year, price, author_id, available_copies)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        title,
        genre,
        int(published_year),
        float(price),
        int(author_id),
        int(available_copies)
    ))
    conn.commit()
    cursor.close()
    conn.close()

    

def view_books():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            b.book_id,
            b.title,
            a.name AS author,
            b.genre,
            b.published_year,
            b.price,
            b.available_copies AS book_quantity
        FROM book b
        JOIN author a ON b.author_id = a.author_id
        ORDER BY b.book_id
    """
    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books






    

