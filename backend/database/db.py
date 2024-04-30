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
                file_extension TEXT NOT NULL,
                ratings REAL NOT NULL DEFAULT 0,
                n_ratings INTEGER NOT NULL DEFAULT 0
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

    def add_ratings(self, book_id, rating):
        try:
            cursor = self.conn.cursor()
            # Get the current ratings and number of ratings for the book
            cursor.execute("SELECT ratings, n_ratings FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                current_ratings, n_ratings = row
                # Calculate the new average rating and increment the number of ratings
                new_ratings = (current_ratings * n_ratings + rating) / (n_ratings + 1)
                n_ratings += 1
                # Update the ratings and n_ratings columns for the book
                cursor.execute("UPDATE books SET ratings = ?, n_ratings = ? WHERE id = ?", (new_ratings, n_ratings, book_id))
                self.conn.commit()
                return True
            else:
                print("Book not found")
                return False
        except sqlite3.Error as e:
            print("Error adding ratings:", e)
            return False

    def sort_by_ratings(self, min_rating, max_rating, ascending=True):
        try:
            # Specify the order for sorting based on the ascending parameter
            order = "ASC" if ascending else "DESC"
            cursor = self.conn.execute("SELECT * FROM books WHERE ratings >= ? AND ratings <= ? ORDER BY ratings " + order, (min_rating, max_rating))
            filtered_books = cursor.fetchall()
            return filtered_books
        except sqlite3.Error as e:
            print("Error sorting by ratings:", e)
            return []

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
