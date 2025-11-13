import sqlite3
import datetime
import random
import os
import re
from appjar import gui


#Importing the SQLite3, appJar and datetime libraries so they can be used in the program.

#SQLite3 will be used for database creation and communications.

#Random library will be needed to generate the authentication code sent to the user's email inbox.

#Datetime library for getting the current date and time.

#OS imported to check if the required CSV diles exist before trying to read and populate the database

#RE imported to check if an item meets the set criteria/pattern returning True if it does, False if it does not - I'll use this for checking email validity.



################ INTIALISATION ################


con = sqlite3.connect("bs_systemDB.db")

#Connecting/creating the program to the database we are using.

cur = con.cursor()

#Setting up the cursor for appearance when the program runs and the database appears.

def bs_buildDatabase():

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
    
bs_buildDatabase()












currentUserFirstName = ""
currentUserID = ""



################ FUNCTIONS ################


   
def bs_checkLogin(enteredUser,enteredPass):

    global currentUserFirstName
    global currentUserID

    cur.execute("""SELECT username FROM bs_tblUsers WHERE username = ?""",(enteredUser,))

    userResult = cur.fetchone()

    if userResult is not None:

        correctUser = userResult[0]

        if enteredUser == correctUser:
                     cur.execute("""SELECT password FROM bs_tblUsers WHERE username = ?""",(correctUser,))

                     passResult = cur.fetchone()

                     if passResult is not None:

                         correctPass = passResult[0]

                         if enteredPass == correctPass:

                             cur.execute("""SELECT firstName FROM bs_tblUsers WHERE username = ?""",(correctUser,))

                             firstNameResult = cur.fetchone()
                             currentUserFirstName = firstNameResult[0]

                             cur.execute("""SELECT userID FROM bs_tblUsers WHERE username = ?""",(correctUser,))

                             userIDResult = cur.fetchone()
                             currentUserID = userIDResult[0]

                             print(currentUserID)
                             print(currentUserFirstName)
                             
                             accessGranted = True
                             
                         else:
                             
                             accessGranted = False
                     else:

                         accessGranted = False
    else:
        accessGranted = False
        
    print(accessGranted)
    return accessGranted

def validPassword(password, minLength=8):

    if len(password) >= minLength:
        
        PWuppercase = re.search(r'[A-Z]', password)
        PWlowercase = re.search(r'[a-z]', password)
        PWnumber = re.search(r'\d', password)
        PWspecial = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

        return bool(PWuppercase and PWlowercase and PWnumber and PWspecial)
        
    else:

        return False

def bs_checkRegInfo(firstname, lastname, username, email, password, conpassword):

    checkFN = firstname.isalpha()
    checkLN = lastname.isalpha()
    checkUN = username.isalnum()

    emailCriteria = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    checkEmail = bool(re.match(emailCriteria, email))

    checkPass = validPassword(password)

    if checkFN == True and checkLN == True and checkUN == True and checkEmail == True and checkPass == True and conpassword == password:

        print("All good here")
        return True

    else:

        print("not good here")
        return False



#This function checks which button has been pressed and acts accordingly on the login page, making the current window close and the chosen one to open while also checking
#If the entered credentials are correct.

def bs_loginPress(button):

    if button == "Cancel":
        
        app.show()
        app.hideSubWindow("win_Login")

#The if statement and its condition above ensures that users can return back to the initial page to register instead,
#If they picked login on accident. The else statement below takes and stores the user's inputs and compares them with the database and its existing users
#In the user table and either allows the user through or does not. In addition to validation of username and password
#It also takes wrong inputs and allows for retries after showing an error box.
        
    else:
        
        UserEntered = app.getEntry("Username")
        PassEntered = app.getEntry("Password")

        accessGiven = bs_checkLogin(UserEntered,PassEntered)

        if accessGiven == True:

            app.setLabel("home_title", f"Welcome {currentUserFirstName}!")
            app.hideSubWindow("win_Login")
            app.showSubWindow("win_Home")
        
        else:

            app.warningBox("Error", "Username or Password Incorrect", parent=None)

            



#This function checks which button has been pressed and acts accordingly on the register page, making the current window close and the chosen one to open.

def bs_registerPress(button):

    global currentUserFirstName
    global currentUserID
    
    if button == "Return":

        app.show()
        app.hideSubWindow("win_Reg")

#The if statement and its condition above ensures that users can return back to the initial page to register instead,
#If they picked login on accident. The else statement below takes and stores the user's inputs and eventually, once I have coded it, will add this information
#To the database and henceforth allow the user to login using their credentials. However, I will also prevent any incorrect information being allowed - examples:
#Email input HAS to have "@", password must be > 8 chars with a number and symbol, no numbers in first + last names, etc etc.
#Additionally, I've added some lines which print the stored values/variables to ensure it stores and takes the information given for some testing.


    else:

        regFName = app.getEntry("First name:")
        regLName = app.getEntry("Last name:")
        regUser = app.getEntry("Username:")
        regEmail = app.getEntry("       Email:")
        regPass = app.getEntry("Password:")
        regCPass = app.getEntry("Confirm Password:")
        print(regFName)
        print(regLName)
        print(regUser)
        print(regEmail)
        print(regPass)
        print(regCPass)

        EInfoValidity = bs_checkRegInfo(regFName,regLName,regUser,regEmail,regPass,regCPass)

        if EInfoValidity == True:
            currentID=cur.execute("Select max(userID) from bs_tblUsers")
            resultID=cur.fetchone()
            newID=int(resultID[0])+1

            cur.execute(""" INSERT INTO bs_tblUsers VALUES(?,?,?,?,?,?,?)""",[newID,regEmail,regUser,regFName,regLName,regPass,regCPass])
            con.commit()

            currentUserFirstName == regFName
            currentUserID == newID
            
            print(currentUserID,"yeah it works")
            
            app.warningBox("Account Created", "Your account has been created successfully!", parent=None)
            app.setLabel("home_title", f"Welcome {regFName}!")
            app.hideSubWindow("win_Reg")
            app.showSubWindow("win_Home")

        else:

            app.warningBox("Error", "The details you have entered are not valid.\nPlease remember that your password must be greater than 8 characters, contain an uppercase letter, a lowercase letter, a number a symbol and both must match.", parent=None)

        

#This function checks which button has been pressed and acts accordingly on the initial page, making the current window close and the chosen one to open.
        
def bs_initialPress(button):

    if button == "Login":
        app.hide()
        app.showSubWindow("win_Login")
    else:
        app.hide()
        app.showSubWindow("win_Reg")
        

#This function allows me to skip logging in on the login page temporarily as I continue to create the other interfaces and build the core before functionality.

def bs_homePress(button):

    if button == "test":

        app.hideSubWindow("win_Login")
        app.showSubWindow("win_Home")

    else:

        while button != "test":
            wait()


#This function checks which button has been pressed and acts accordingly on the main menu page after login, making the current window close and the chosen one to open.

def bs_menuPress(button):

    if button == "Book Haircut":

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_bookHaircut")

    elif button == "Cancel Haircut":

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_cancelHaircut")

    elif button == "Reschedule Haircut":

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_rescheduleHaircut")

    else:

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_userSettings")










################ INTERFACE ################




#Creating the interface

#Sets the initial window name and its resolution

app = gui("Half-Life Hair", "900x600")

def bs_createInterface():

######## Initial Page ########


#This code is for the first screen the user will see, asking them to login or sign up.

    app.setBg("#152b6d")
    app.addLabel("title", "Welcome!")
    app.setLabelFg("title","#ff8039")
    app.setFont(20)
    
    app.addButtons(["Login", "Register"], bs_initialPress)
    app.setButtonBg("Login", "#ff8039")
    app.setButtonBg("Register", "#ff8039")
    app.setButtonFg("Login", "#152b6d")
    app.setButtonFg("Register", "#152b6d")

######## Register Page ########


#This code is for the register screen, with buttons to cancel (taking them back
#to the initial screen or lets them register with register)

    app.startSubWindow("win_Reg")
    app.setSize("900x600")
    app.setBg("#152b6d")
    
    app.addLabel("reg_title", "Register")
    app.setLabelSticky("reg_title","new")
    app.setLabelFg("reg_title","#ff8039")
    
    app.addLabelEntry("First name:")
    app.addLabelEntry("Last name:")
    app.addLabelEntry("Username:")
    app.addLabelEntry("       Email:")
    app.addLabelEntry("Password:")
    app.addLabelEntry("Confirm Password:")
    
    app.addButtons(["Register!", "Return"],bs_registerPress)

    app.setButtonBg("Register!", "#ff8039")
    app.setButtonBg("Return", "#ff8039")
    app.setButtonFg("Register!", "#152b6d")
    app.setButtonFg("Return", "#152b6d")
    app.setLabelFg("First name:","#ff8039")
    app.setLabelFg("Last name:","#ff8039")
    app.setLabelFg("Username:","#ff8039")
    app.setLabelFg("       Email:","#ff8039")
    app.setLabelFg("Password:","#ff8039")
    app.setLabelFg("Confirm Password:","#ff8039")
    app.setFont(18)
    
    app.stopSubWindow()

######## Login Page ########


#This code is for the login screen, with buttons to cancel (taking them back to the initial screen), to reset their password
#Or to login, taking their entries to login
    
    app.startSubWindow("win_Login")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.addLabel("wel_title", "Welcome!")
    app.setLabelFg("wel_title","#ff8039")
    app.setFont(20)

    app.addLabelEntry("Username")
    app.addLabelEntry("Password")
    app.setLabelFg("Username","#ff8039")
    app.setLabelFg("Password","#ff8039")

    app.addButtons(["Submit", "Forgot Password", "Cancel"],bs_loginPress)
    app.addButtons(["test"],bs_homePress)
    
    app.setButtonBg("Submit", "#ff8039")
    app.setButtonBg("Cancel", "#ff8039")
    app.setButtonBg("Forgot Password", "#ff8039")
    app.setButtonFg("Submit", "#152b6d")
    app.setButtonFg("Cancel", "#152b6d")
    app.setButtonFg("Forgot Password", "#152b6d")
    
    app.stopSubWindow()

######## Homepage ########

    #Able to reuse some of my previous code such as for setting the window size, background colour and font size/colouring.

    app.startSubWindow("win_Home")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.addLabel("home_title", "Welcome!", 0, 0)
    app.setLabelFg("home_title","#ff8039")
    app.setFont(20)

    app.addButtons(["Book Haircut"],bs_menuPress)
    app.addButtons(["Cancel Haircut"],bs_menuPress)
    app.addButtons(["Reschedule Haircut"],bs_menuPress)
    app.addButtons(["Settings"],bs_menuPress)

    app.setButtonBg("Book Haircut", "#ff8039")
    app.setButtonBg("Cancel Haircut", "#ff8039")
    app.setButtonBg("Reschedule Haircut", "#ff8039")
    app.setButtonBg("Settings", "#ff8039")
    app.setButtonFg("Book Haircut", "#152b6d")
    app.setButtonFg("Cancel Haircut", "#152b6d")
    app.setButtonFg("Reschedule Haircut", "#152b6d")
    app.setButtonFg("Settings", "#152b6d")


    app.stopSubWindow()


    #'username' is only temporary, I plan to incorporate the user's actual username or first name in the next prototypes to add some sense of familiarity and friendliness.


######## Create Booking Page ########

    app.startSubWindow("win_bookHaircut")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.addLabel("booking_title","Book Haircut")
    app.setLabelFg("booking_title","#ff8039")

    app.stopSubWindow()

######## Cancel Booking Page ########

    app.startSubWindow("win_cancelHaircut")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.addLabel("cancel_title","Cancel Haircut")
    app.setLabelFg("cancel_title","#ff8039")
    
    app.stopSubWindow()

######## Reschedule Booking Page ########

    app.startSubWindow("win_rescheduleHaircut")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.addLabel("reschedule_title","Reschedule Haircut")
    app.setLabelFg("reschedule_title","#ff8039")

    app.stopSubWindow()

######## Settings / Change details + password Page ########

    app.startSubWindow("win_userSettings")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.addLabel("settings_title","Settings")
    app.setLabelFg("settings_title","#ff8039")

    app.stopSubWindow()

    
    app.go()

bs_createInterface()

#Main
