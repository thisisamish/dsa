import sqlite3
from sqlite3 import Error
import json


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite version {sqlite3.sqlite_version}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    
    return conn


def exec_sql(conn, sql, msg):
    try:
        cursor = conn.cursor()
        cursor.executescript(sql)
        print(msg)
    except Error as e:
        print(f"Error executing SQL: {e}")


def query(conn, sql, params=()):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    except Error as e:
        print(f"Error in quering: {e}")


def main():
    database = r"database.sqlite"
    
    with open("schema.sql", "r") as file:
        schema_sql = file.read()
    
    with open("data.sql", "r") as file:
        data_sql = file.read()

    with open("tests.json", "r") as file:
        queries = json.load(file)

    conn = create_connection(database)
    
    if conn is not None:
        exec_sql(conn, schema_sql, "Created the schema")
        exec_sql(conn, data_sql, "Added the data")

        print(query(conn, queries["count_problem_sheets"]))
        print(query(conn, queries["count_problems_in_problem_sheets"]))
        
        conn.close()
    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()