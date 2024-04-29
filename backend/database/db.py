import sqlite3
import os

def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance

class DatabaseDriver(object):
    def __init__(self, db_filename):
        db_filename_abs = os.path.abspath(db_filename)
        self.conn = sqlite3.connect(db_filename_abs)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.create_users_table()
        self.create_sessions_table()
        self.create_user_favorites_table()
        self.create_books_table()
        self.create_genres_table()
        self.create_book_genres_table()

    def exec_sql_query(self, sql, params=()):
        print("Executing SQL:", sql)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor
        except sqlite3.Error as e:
            print("SQL execution error:", e)
            return None

    def create_users_table(self):
        try:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """)
        except Exception as e:
            print(e)

    def create_sessions_table(self):
        try:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session TEXT NOT NULL UNIQUE,
                last_login TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """)
        except Exception as e:
            print(e)

    def create_books_table(self):
        try:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name TEXT NOT NULL,
                author_name TEXT NOT NULL,
                publication_date TEXT NOT NULL,
                file_extension TEXT NOT NULL
            )
            """)
        except Exception as e:
            print(e)

    def create_genres_table(self):
        try:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_name TEXT NOT NULL
            )
            """)
        except Exception as e:
            print(e)

    def create_book_genres_table(self):
        try:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS book_genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                genre_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id)
            )
            """)
        except Exception as e:
            print(e)

    def create_user_favorites_table(self):
        try:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
            """)
        except Exception as e:
            print(e)

    def add_book(self, name, author_name, publication_date, file_extension, genre_names):
        try:
            cursor = self.conn.cursor()
            # Insert the book into the books table
            cursor.execute("INSERT INTO books (book_name, author_name, publication_date, file_extension) VALUES (?, ?, ?, ?)",
                        (name, author_name, publication_date, file_extension))
            book_id = cursor.lastrowid
            # Insert genres into the genres table if they don't exist, and link them to the book in the book_genre table
            for genre_name in genre_names:
                cursor.execute("INSERT OR IGNORE INTO genres (genre_name) VALUES (?)", (genre_name,))
                cursor.execute("SELECT id FROM genres WHERE genre_name = ?", (genre_name,))
                genre_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO book_genre (book_id, genre_id) VALUES (?, ?)", (book_id, genre_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Error adding book:", e)
            return False

    def delete_book(self, book_id):
        try:
            cursor = self.conn.cursor()
            # Delete the book from the books table
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            # Delete the entries from the book_genre table associated with the book
            cursor.execute("DELETE FROM book_genre WHERE book_id = ?", (book_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Error deleting book:", e)
            return False

        ##CRUD Opperations (read and writes to the database go here)
    def get_all_books(self):
        cursor = self.conn.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return books

    def get_book_by_id(self, book_id):
        cursor = self.conn.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        return book

    def get_all_favorites(self):
        cursor = self.conn.execute("SELECT * FROM favorites")
        favorites = cursor.fetchall()
        return favorites

    def favorite_book(self, user_id, book_id):
        try:
            self.conn.execute("INSERT INTO favorites (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Error favoriting book:", e)
            return False

    def unfavorite_book(self, user_id, book_id):
        try:
            self.conn.execute("DELETE FROM favorites WHERE user_id = ? AND book_id = ?", (user_id, book_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Error unfavoriting book:", e)
            return False

    def filter_by_genre(self, genre_name):
        cursor = self.conn.execute("""
            SELECT b.*
            FROM books b
            JOIN book_genre bg ON b.id = bg.book_id
            JOIN genres g ON bg.genre_id = g.id
            WHERE g.genre_name = ?
        """, (genre_name,))
        filtered_books = cursor.fetchall()
        return filtered_books

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
