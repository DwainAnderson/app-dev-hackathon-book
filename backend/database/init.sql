-- database: ../test.sqlite

-- Sessions table
CREATE TABLE sessions IF NOT EXISTS  (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  session TEXT NOT NULL UNIQUE,
  last_login TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Users table
CREATE TABLE user IF NOT EXISTS  (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);


--password: monkey
INSERT INTO users (name, username, password) VALUES
    ('John Doe', 'johndoe', '$2y$10$QtCybkpkzh7x5VN11APHned4J8fu78.eFXlyAMmahuAaNcbwZ7FH.'),
    ('Jane Smith', 'janesmith','$2y$10$QtCybkpkzh7x5VN11APHned4J8fu78.eFXlyAMmahuAaNcbwZ7FH.');

-- User favorites --
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Creating books table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author_name TEXT NOT NULL,
    publication_date TEXT NOT NULL,
    file_extension TEXT NOT NULL
);

-- Creating genre (Tag) table
CREATE TABLE genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT NOT NULL
);

-- Creating Book Genre (Linking Table) table
CREATE TABLE book_genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);


-- Sample data for books table
INSERT INTO books (book_name, author_name, publication_date, file_extension)
VALUES
    ('The Great Gatsby', 'F. Scott Fitzgerald', '1925-04-10', 'pdf'),
    ('To Kill a Mockingbird', 'Harper Lee', '1960-07-11', 'epub'),
    ('1984', 'George Orwell', '1949-06-08', 'txt');

-- Sample data for genres table
INSERT INTO genres (genre_name)
VALUES
    ('Fiction'),
    ('Classic'),
    ('Dystopian');

-- Sample data for book_genre table (linking table)
INSERT INTO book_genre (book_id, genre_id)
VALUES
    (1, 1), -- The Great Gatsby is Fiction
    (1, 2), -- The Great Gatsby is also a Classic
    (2, 1), -- To Kill a Mockingbird is Fiction
    (2, 2), -- To Kill a Mockingbird is also a Classic
    (3, 1), -- 1984 is Fiction
    (3, 3); -- 1984 is Dystopian
