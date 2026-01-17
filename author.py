from db_config import get_connection

def add_author(name, country, birth_year):
    if not name or not birth_year.isdigit():
        raise ValueError("Invalid input. Name and birth year are required.")

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO author (name, country, birth_year) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, country, int(birth_year)))
    conn.commit()
    cursor.close()
    conn.close()





def view_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author_id, name, country, birth_year FROM author ORDER BY author_id")
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    return authors

