# -*- coding: utf-8 -*-
"""
Creating TalTech diners database using SQLite3.

Created on Mon Mar  6 15:00:30 2023

@author: aloansberg

There are 8 diners in different buildings of TalTech that will be added to database diners.db, table canteen.
There are 4 service providers in total: Rahva Toit, Baltic Restaurants Estonia AS, TTÜ Sport and Kohvik
that will be added to database diners.db, table provider.
"""

import sqlite3

tables = ["""
CREATE TABLE IF NOT EXISTS canteen
(id INTEGER PRIMARY KEY,
provider_id      INTEGER,
name            TEXT    NOT NULL, 
location        TEXT    NOT NULL, 
time_open       INTEGER     NOT NULL, 
time_closed     INTEGER     NOT NULL,
FOREIGN KEY (provider_id) REFERENCES provider (id)
);""",

          """
CREATE TABLE IF NOT EXISTS provider 
(id INTEGER PRIMARY KEY,
provider_name    TEXT    NOT NULL)
;"""]

records_canteen = [(1, "Economics- and social science building canteen", "Akadeemia tee 3 SOC- building", 830, 1830),
                   (1, "Library canteen", "Akadeemia tee 1/Ehitajate tee 7", 830, 1900),
                   (2, "Main building Deli cafe", "Ehitajate tee 5 U01 building", 900, 1630),
                   (2, "Main building Daily lunch restaurant", "Ehitajate tee 5 U01 building", 900, 1600),
                   (1, "U06 building canteen", "U06 building canteen", 900, 1600),
                   (2, "Natural Science building canteen", "Akadeemia tee 15 SCI building", 900, 1600),
                   (2, "ICT building canteen", "Raja 15/Mäepealse 1", 900, 1600),
                   (4, "Sports building canteen", "Männiliiva 7 S01 building", 1100, 2000)]

records_providers = ["Rahva Toit", "Baltic Restaurants Estonia AS",
                     "Kohvik", "TTÜ Sport OÜ"]


def open_db():
    """Open SQLite database.

    Database called diners.db will be created after executing this function.
    """
    global connection
    global cursor
    connection = sqlite3.connect("diners.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    print("Opened database successfully\n")


def create_table():
    """Create tables canteen and provider."""

    count = 0
    for i in tables:
        count += 1
        connection.execute(i)

    if count > 0:
        print(f"{count} table(s) created successfully\n")
    else:
        print("No tables were created\n")


def create_records():
    """Create some records to the canteen and provider tables."""

    count = 0
    try:
        for p in records_providers:
            format_str = """INSERT INTO provider (provider_name)
            VALUES ("{provider_name}");"""

            sql_command = format_str.format(provider_name=p)
            connection.execute(sql_command)
            count += 1

        for p in records_canteen:
            format_str = """INSERT INTO canteen (provider_id, name, location, time_open, time_closed)
            VALUES ("{provider_id}", "{name}", "{location}", "{time_open}", "{time_closed}");"""

            sql_command = format_str.format(provider_id=p[0], name=p[1], location=p[2], time_open=p[3],
                                            time_closed=p[4])
            connection.execute(sql_command)
            count += 1

        # Adding bitStop KOHVIK separately:
        sql_command = """INSERT INTO canteen (provider_id, name, location, time_open, time_closed)
            VALUES (3,"bitStop KOHVIK", "IT College, Raja 4c", 930, 1600);"""
        connection.execute(sql_command)
        count += 1

        connection.commit()
        print(f"{count} record(s) created successfully\n")
    except:
        print("No records were created\n")


def format_time(row: int) -> str:
    """Convert time as int to (string) more readable form."""

    str_row = str(row)
    if row > 999:
        return str_row[0] + str_row[1] + "." + str_row[2:]
    else:
        return str_row[0] + "." + str_row[1:]


def query1():
    """Query for canteens which are open 16.15-18.00."""

    print("Query for canteens which are open 16.15-18.00:\n")
    cursor.execute("SELECT id, provider_id, name, location, time_open, time_closed from canteen")
    count = 0
    for row in cursor:
        if row[4] <= 1615 and row[5] >= 1800:
            print("id = ", row[0])
            print("provider_id = ", row[1])
            print("name = ", row[2])
            print("location = ", row[3])
            print("time_open = ", format_time(row[4]))
            print("time_closed = ", format_time(row[5]), "\n")
            count += 1

    if count > 0:
        print(f"Operation done successfully. Found {count} canteen(s) which are open 16.15-18.00\n")
    else:
        print("Nothing was found\n")


def query2():
    """Query for canteens which are serviced by Rahva Toit."""

    print("Query for canteens which are serviced by Rahva Toit:\n")
    cursor.execute(
        "SELECT * FROM canteen WHERE provider_id IN (SELECT id from provider WHERE provider_name LIKE 'Rahva Toit');")
    count = 0
    for row in cursor:
        print("id = ", row[0])
        print("provider_id = ", row[1])
        print("name = ", row[2])
        print("location = ", row[3])
        print("time_open = ", format_time(row[4]))
        print("time_closed = ", format_time(row[5]), "\n")
        count += 1

    if count > 0:
        print(f"Operation done successfully. Found {count} canteens which are serviced by Rahva Toit\n")
    else:
        print("Nothing was found\n")


def close_connection():
    """Close connection."""

    connection.close()
    print("Connection closed")


if __name__ == "__main__":
    open_db()
    create_table()
    create_records()
    query1()
    query2()
    close_connection()
