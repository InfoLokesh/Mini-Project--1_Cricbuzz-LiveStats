import mysql.connector

def create_connection_to_mysql_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Or the IP address/hostname of your MySQL server
            user="root",
            password="root",
            database="SampleDB"
            # ,autocommit = True
        )

        if conn.is_connected():
            print("Connected to MySQL database successfully!")
            return conn

            # cursor = con.cursor()

            # CREATE DATABASE
            mycursor.execute("CREATE DATABASE IF NOT EXISTS SampleDB")

            con.close()
            print("Connection to MySQL database closed successfully!")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")


def execute_query_with_cursor(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    return cursor
