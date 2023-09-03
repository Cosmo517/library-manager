import os
import sqlite3


def create_database_connection():
    """
    :returns: connection, file name
    """
    index = 1
    for x in os.listdir():
        if x.endswith(".db"):
            print(str(index) + ". " + x[0:-3])
            index += 1
    print()
    database_name = input("Enter name to select a database, or enter a new name to create a new database: ")

    for x in os.listdir():
        if x == (database_name + ".db"):
            return sqlite3.connect(database_name.rstrip() + ".db"), database_name
    database_creation_confirmation = input("Are you sure you want to create a new database? (Y/N): ").lower()
    if database_creation_confirmation == "y":

        return sqlite3.connect(database_name.rstrip() + ".db"), database_name
    else:
        create_database_connection()


def delete_database(filename):
    """
    deletes the database with the corresponding filename
    :param filename:
    """
    os.remove(filename)


def database_setup(connection):
    cursor = connection.cursor()
    sql_books_table = """CREATE TABLE IF NOT EXISTS books (
                        book_name text PRIMARY KEY,
                        volume integer,
                        author_name text,
                        page_count integer,
                        rating integer,
                        own text NOT NULL,
                        read text NOT NULL,
                        genre text,
                        cover_type text
                        );
                        """
    cursor.execute(sql_books_table)
    cursor.close()


def get_all_tables_in_library(con):
    sql_query = """SELECT name FROM sqlite_master  
                    WHERE type='table';"""
    cursor = con.cursor()
    cursor.execute(sql_query)
    return cursor.fetchall()


def insert_into_table(connection, book_name, volume, author_name, page_count, rating, own, read, genre, cover_type):
    try:
        insert_query = """
        INSERT INTO books (book_name, volume, author_name, page_count, rating, own, read, genre, cover_type)
        VALUES
        ('{}', {}, '{}', {}, {}, '{}', '{}', '{}', '{}');
        """.format(book_name, volume, author_name, page_count, rating, own, read, genre, cover_type)
        cursor = connection.cursor()
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print('Failed to insert data into sqlite table, ', error)


def get_all_rows(connection):
    sql_query = "SELECT * FROM books"
    cursor = connection.cursor()
    cursor.execute(sql_query)
    return cursor.fetchall()