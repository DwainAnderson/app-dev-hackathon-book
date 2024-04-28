import os
import sqlite3
from hashlib import md5

def init_db(db_filename, init_sql_filename):
    if not os.path.exists(init_sql_filename):
        raise Exception("No such file: " + init_sql_filename)

    with open(init_sql_filename, 'r') as init_sql_file:
        init_sql = init_sql_file.read()
    init_checksum = md5(init_sql.encode()).hexdigest()
    init_checksum_filename = init_sql_filename + ".checksum"

    if not os.path.exists(db_filename) and os.path.exists(init_checksum_filename):
        os.unlink(init_checksum_filename)

    if os.path.exists(db_filename) and not os.path.exists(init_checksum_filename):
        raise Exception("No checksum for existing database. Please regenerate your database (delete .sqlite file).")

    if os.path.exists(init_checksum_filename):
        with open(init_checksum_filename, 'r') as init_checksum_file:
            current_checksum = init_checksum_file.read()

        if init_checksum != current_checksum:
            raise Exception("Database initialization script has changed. Please regenerate your database (delete " + db_filename + ").")

    if not os.path.exists(db_filename):
        print("Creating database " + db_filename + " from " + init_sql_filename)
        conn = sqlite3.connect(db_filename)
        conn.row_factory = sqlite3.Row

        try:
            with open(init_sql_filename, 'r') as init_sql_file:
                conn.executescript(init_sql_file.read())

            with open(init_checksum_filename, 'w') as init_checksum_file:
                init_checksum_file.write(init_checksum)

            return conn
        except sqlite3.Error as e:
            os.unlink(db_filename)
            print("Failed to initialize database " + db_filename + ". Check your initialization SQL: " + init_sql_filename)
            raise e
    else:
        print("Opening database " + db_filename)
        conn = sqlite3.connect(db_filename)
        conn.row_factory = sqlite3.Row
        return conn

def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

    
class DatabaseDriver(object):
    def __init__(self, db_filename, init_sql_filename):
        self.conn = init_db(db_filename, init_sql_filename)
        self.conn.execute("PRAGMA foreign_keys = 1")

    def exec_sql_query(self, sql, params=()):
        print("Executing SQL:", sql)

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor
        except sqlite3.Error as e:
            print("SQL execution error:", e)
            return None
  

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
