import sqlite3

from appjar import gui

#Importing the SQLite3 libraries so they can be used in the program.

con = sqlite3.connect("bs_systemDB.db")

#Connecting/creating the program to the database we are using.

cur = con.cursor()

#Setting up the cursor for appearance when the program runs and the database appears.

def buildDatabase():

#Building the database with all the tables needed to function and to build program foundations.

#First table - users

    cur.execute("""CREATE TABLE 'bs_tblUsers' (
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

    cur.execute("""CREATE TABLE 'bs_tblServices' (
                serviceID integer NOT NULL PRIMARY KEY,
                serviceName varchar(35) NOT NULL,
                price float NOT NULL
                )
                """)

#DON'T FORGET TO VALIDATE FLOAT AT LATER POINT TO ENSURE IT IS WITHIN THE CORRECT RANGE


#Third table - barbers

    cur.execute("""CREATE TABLE 'bs_tblBarbers' (
                barberID integer NOT NULL PRIMARY KEY,
                barberName varchar(20) NOT NULL
                )
                """)


#Fourth table - user bookings, used as linking table

    cur.execute("""CREATE TABLE 'bs_userBooking' (
                userID integer NOT NULL,
                bookingID integer NOT NULL,
                bookingTime time NOT NULL,
                PRIMARY KEY (userID, bookingID),
                FOREIGN KEY (userID) REFERENCES bs_tblUsers (userID), 
                FOREIGN KEY (bookingID) REFERENCES bs_tblBookings (bookingID)
                )
                """)

#Fifth and final table - bookings table

    cur.execute("""CREATE TABLE 'bs_tblBookings' (
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

#Barbers table

    barbersFile=open("bs_Barbers.csv", "r")
    for line in barbersFile:
        line = line.strip()
        barberID,barberName = line.split(",")
        cur.execute("INSERT INTO bs_tblBarbers VALUES(?,?)", [barberID, barberName])

#Services table

    servicesFile=open("bs_Services.csv", "r")
    for line in servicesFile:
        line = line.strip()
        serviceID,serviceName,price = line.split(",")
        cur.execute("INSERT INTO bs_tblServices VALUES(?,?,?)", [serviceID, serviceName, price])

#Users table

    usersFile=open("bs_Users.csv", "r")
    for line in usersFile:
        line = line.strip()
        userID,email,username,firstName,lastName,password,isBarber = line.split(",")
        cur.execute("INSERT INTO bs_tblUsers VALUES(?,?,?,?,?,?,?)", [userID, email, username, firstName, lastName, password, isBarber])

        con.commit()

#Populating database



#Build database

buildDatabase()

#Main

