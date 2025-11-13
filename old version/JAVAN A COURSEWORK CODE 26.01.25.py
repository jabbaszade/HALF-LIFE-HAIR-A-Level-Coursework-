import sqlite3
import datetime
import random
import os
from appjar import gui

#Importing the SQLite3, appJar and datetime libraries so they can be used in the program.

#SQLite3 will be used for database creation and communications.

#Random library will be needed to generate the authentication code sent to the user's email inbox.

#Datetime library for getting the current date and time.

#OS imported to check if the required CSV diles exist before trying to read and populate the database



################ INTIALISATION ################


con = sqlite3.connect("bs_systemDB.db")

#Connecting/creating the program to the database we are using.

cur = con.cursor()

#Setting up the cursor for appearance when the program runs and the database appears.

def buildDatabase():

#Building the database with all the tables needed to function and to build program foundations.

#First table - users

    cur.execute("""CREATE TABLE IF NOT EXISTS 'bs_tblUsers' (
                userID integer NOT NULL PRIMARY KEY,
                email varchar(60) NOT NULL,
                username varchar(20) NOT NULL,
                firstName varchar(20) NOT NULL,
                lastName varchar(30) NOT NULL,
                password varchar(30) NOT NULL,
                isBarber boolean NOT NULL
                )
                """)

#Second table - services

    cur.execute("""CREATE TABLE IF NOT EXISTS 'bs_tblServices' (
                serviceID integer NOT NULL PRIMARY KEY,
                serviceName varchar(35) NOT NULL,
                price float NOT NULL
                )
                """)

#DON'T FORGET TO VALIDATE FLOAT AT LATER POINT TO ENSURE IT IS WITHIN THE CORRECT RANGE


#Third table - barbers

    cur.execute("""CREATE TABLE IF NOT EXISTS 'bs_tblBarbers' (
                barberID integer NOT NULL PRIMARY KEY,
                barberName varchar(20) NOT NULL
                )
                """)


#Fourth table - user bookings, used as linking table

    cur.execute("""CREATE TABLE IF NOT EXISTS 'bs_userBooking' (
                userID integer NOT NULL,
                bookingID integer NOT NULL,
                bookingTime time NOT NULL,
                PRIMARY KEY (userID, bookingID),
                FOREIGN KEY (userID) REFERENCES bs_tblUsers (userID), 
                FOREIGN KEY (bookingID) REFERENCES bs_tblBookings (bookingID)
                )
                """)

#Fifth and final table - bookings table

    cur.execute("""CREATE TABLE IF NOT EXISTS 'bs_tblBookings' (
                bookingID integer NOT NULL,
                serviceID integer NOT NULL,
                userID integer NOT NULL,
                barberName varchar NOT NULL,
                serviceName varchar NOT NULL,
                bookingDate date NOT NULL,
                status integer NOT NULL,
                price float NOT NULL,
                PRIMARY KEY (userID, bookingID),
                FOREIGN KEY (userID) REFERENCES bs_tblUsers (userID), 
                FOREIGN KEY (bookingID) REFERENCES bs_tblBookings (bookingID)
                )
                """)


#Populating database and tables

    def bs_populateTable(file_name, sql, columns):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    values = line.split(",")
                    if len(values) == columns:
                        cur.execute(sql, values)
        else:
            print(f"File {file_name} not found.")

#Function I just created being called - it populates each table respectively while checking that the files exist using the OS library.

    bs_populateTable("bs_Barbers.csv", "INSERT OR IGNORE INTO bs_tblBarbers VALUES (?, ?)", 2)
    bs_populateTable("bs_Services.csv", "INSERT OR IGNORE INTO bs_tblServices VALUES (?, ?, ?)", 3)
    bs_populateTable("bs_Users.csv", "INSERT OR IGNORE INTO bs_tblUsers VALUES (?, ?, ?, ?, ?, ?, ?)", 7)

    con.commit()

#Building the database

buildDatabase()

app = gui("Half-Life Hair Barber Shop")

def bs_createInterface():

    #The code for the main program window
    app.addEntry("ent_Username")
    app.addEntry("ent_Password")

    #The code for the homepage

    app.startSubWindow("win_Main")
    app.addLabel("bs_home", "Homepage")
    app.addSpinBox("Happiness", [1,2,3,4,5,6,7,8,9,10])
    app.stopSubWindow()

    app.startSubWindow("win_Two")
    app.addLabel("bs_settings", "Settings")
    app.addSpinBox("diresituation", [1,2,3,4,5,6,7,8,9,10])
    app.stopSubWindow()

    app.go()

bs_createInterface()
#Main
