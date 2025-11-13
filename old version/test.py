import sqlite3
import datetime
import random
from appjar import gui
import os

# Database connection
con = sqlite3.connect("bs_systemDB.db")
cur = con.cursor()

# Build database schema and populate data
def buildDatabase():
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bs_tblUsers (
            userID INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            username TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            password TEXT NOT NULL,
            isBarber BOOLEAN NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bs_tblServices (
            serviceID INTEGER PRIMARY KEY,
            serviceName TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bs_tblBarbers (
            barberID INTEGER PRIMARY KEY,
            barberName TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bs_userBooking (
            userID INTEGER NOT NULL,
            bookingID INTEGER NOT NULL,
            bookingTime TIME NOT NULL,
            PRIMARY KEY (userID, bookingID),
            FOREIGN KEY (userID) REFERENCES bs_tblUsers (userID)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bs_tblBookings (
            bookingID INTEGER PRIMARY KEY,
            serviceID INTEGER NOT NULL,
            userID INTEGER NOT NULL,
            barberName TEXT NOT NULL,
            serviceName TEXT NOT NULL,
            bookingDate DATE NOT NULL,
            status INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (userID) REFERENCES bs_tblUsers (userID),
            FOREIGN KEY (serviceID) REFERENCES bs_tblServices (serviceID)
        )
    """)

    # Populate tables from CSV files
    def populateTable(file_name, query, column_count):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    values = line.split(",")
                    if len(values) == column_count:
                        cur.execute(query, values)
        else:
            print(f"File {file_name} not found.")

    populateTable("bs_Barbers.csv", "INSERT OR IGNORE INTO bs_tblBarbers VALUES (?, ?)", 2)
    populateTable("bs_Services.csv", "INSERT OR IGNORE INTO bs_tblServices VALUES (?, ?, ?)", 3)
    populateTable("bs_Users.csv", "INSERT OR IGNORE INTO bs_tblUsers VALUES (?, ?, ?, ?, ?, ?, ?)", 7)

    con.commit()

# GUI interface
def bs_createInterface():
    app = gui("Half-Life Hair Barber Shop", "400x300")
    app.addLabel("title", "Welcome to Half-Life Hair Barber Shop")
    app.setLabelBg("title", "blue")
    app.setLabelFg("title", "white")
    app.addButton("Exit", app.stop)
    app.go()

# Build the database and run the app
buildDatabase()
bs_createInterface()
