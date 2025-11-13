import sqlite3
from datetime import datetime,timedelta
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


#Populating database and tables function

    def bs_populateTable(file_name, sql, columns): #The inputs that need to be given in the function
        
        if os.path.exists(file_name): #If the CSV file is present it will then open them
            
            with open(file_name, "r") as file: #Opening and reading the CSV file
                
                for line in file: #Loop to iterate through each line in the CSV file.
                    
                    line = line.strip()  #Whitespace is removed
                    
                    values = line.split(",") #The values are split
                    
                    if len(values) == columns: #If the length of the CSV line and its values are equal to the amount of columbs it will proceed
                        
                        cur.execute(sql, values) #Adding said values to the
                        
        else:

            #If a CSV file is not present, it will return and error as it cannot be read from, meaning it (the table(s)) cannot be populated.
            
            print(f"File {file_name} not found.")

#Function I just created being called - it populates each table respectively while checking that the files exist using the OS library.

    bs_populateTable("bs_Barbers.csv", "INSERT OR IGNORE INTO bs_tblBarbers VALUES (?, ?)", 2) #The numbers at the ends are the number of values
    bs_populateTable("bs_Services.csv", "INSERT OR IGNORE INTO bs_tblServices VALUES (?, ?, ?)", 3)
    bs_populateTable("bs_Users.csv", "INSERT OR IGNORE INTO bs_tblUsers VALUES (?, ?, ?, ?, ?, ?, ?)", 7)

    con.commit()

#Building the database
    
bs_buildDatabase()












currentUserFirstName = ""
currentUserID = ""



################ FUNCTIONS ################

#Function to check the login details given to either allow or disallow access to booking and the account - IF it exists of course.
   
def bs_checkLogin(enteredUser,enteredPass):

    global currentUserFirstName
    global currentUserID

    #Storing my global variables for later - I plan to use the first name on the login screen for a greeting message using their name for a sense of familiarity
    #I plan to use the userID for booking creation, rescheduling and deletion as well as changing passwords.

    cur.execute("""SELECT username FROM bs_tblUsers WHERE username = ?""",(enteredUser,))

    userResult = cur.fetchone()

    #Checking in the database to see if the username exists

    if userResult is not None: #If the username exists;

        correctUser = userResult[0] #Stores the username found or not found as correct username to now compare and then possibly acquire the matching password.

        if enteredUser == correctUser: #If the username given matches the one found;
            
                     cur.execute("""SELECT password FROM bs_tblUsers WHERE username = ?""",(correctUser,))

                     passResult = cur.fetchone()

                     #Getting the matching and correct password

                     if passResult is not None: #If there is a password;

                         correctPass = passResult[0] #The correct password is stored for comparison.

                         if enteredPass == correctPass: #If the password entered matches the correct one;

                             cur.execute("""SELECT firstName FROM bs_tblUsers WHERE username = ?""",(correctUser,))

                             #Getting the user's name for later usage as mentioned before.

                             firstNameResult = cur.fetchone()
                             currentUserFirstName = firstNameResult[0]

                             cur.execute("""SELECT userID FROM bs_tblUsers WHERE username = ?""",(correctUser,))

                             userIDResult = cur.fetchone()
                             currentUserID = userIDResult[0]

                             #Getting the user's userID for later usage as mentioned before.

                             print(currentUserID)
                             print(currentUserFirstName)

                             #Printing the pair to ensure they've been stored and can be used - this is purely for my testing to check and will be removed later.
                             
                             accessGranted = True

                             #User can login, credentials correct.
                             
                         else:
                             
                             accessGranted = False

                             #User cannot login, credentials incorrect.
                             
                     else:

                         accessGranted = False

                         #User cannot login, credentials incorrect.
    else:
        accessGranted = False

        #User cannot login, credentials incorrect.
        
    return accessGranted


#Function to check the password on the register screen is valid/secure enough to be used, being compared to criteria set using the "re" library and its function.

def validPassword(password, minLength=8):

    if len(password) >= minLength: #If the length of the password is greater than the minimum length;
        
        PWuppercase = re.search(r'[A-Z]', password) #Linear searches the password for uppercase letters. Returns true if present, false if not.
        PWlowercase = re.search(r'[a-z]', password) #Linear searches the password for lowercase letters. Returns true if present, false if not.
        PWnumber = re.search(r'\d', password) #Linear searches the password for numbers. Returns true if present, false if not.
        PWspecial = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) #Linear searches the password for special characters/symbols. Returns true if present, false if not.

        return bool(PWuppercase and PWlowercase and PWnumber and PWspecial) #Collective returns for true if present, false if not.
        
    else:

        return False #If any criteria not met, returns false to make user comply/meet set password criteria.


#Function that checks all registration details entered by user.

def bs_checkRegInfo(firstname, lastname, username, email, password, conpassword):

    #Using Python's built-in functions for validation

    checkFN = firstname.isalpha() #Makes sure the first name only contains letters from the alphabet, no numbers or symbols - returns true if only alphabetical, false if not.
    checkLN = lastname.isalpha() #Makes sure the last name only contains letters from the alphabet, no numbers or symbols - returns true if only alphabetical, false if not.
    checkUN = username.isalnum() #Makes sure the username only contains letters from the alphabet and/or numbers but NO symbols - returns true if it has numbers and/or is alphabetical, false if it uses symbols.

    emailCriteria = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' #The format in which the given email should be in - must contain "@" and "." to be true - if not it returns false.
    checkEmail = bool(re.match(emailCriteria, email)) #Checks if the email matches the given criteria using the re.match function from the "re" library

    checkPass = validPassword(password) #Calls the function which checks the password's validity (compared to criteria also).

    if checkFN == True and checkLN == True and checkUN == True and checkEmail == True and checkPass == True and conpassword == password: #If all are true, meaning they are all valid;

        print("All good here") #Continue.
        return True #Function returns the boolean to allow user to progress.

    else:

        print("not good here") #Cannot continue.
        return False #Function returns the boolean to prevent user from progressing.



#This function checks which button has been pressed and acts accordingly on the login page, making the current window close and the chosen one to open while also checking
#If the entered credentials are correct.

#def validPassword()

#def bs_checkRegInfo()

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

        #Gets the inputted data from the entry boxes in appJar
        
        accessGiven = bs_checkLogin(UserEntered,PassEntered)

        if accessGiven == True:

            app.setLabel("home_title", f"Welcome {currentUserFirstName}!")
            app.hideSubWindow("win_Login")
            app.showSubWindow("win_Home")
        
        else:

            app.warningBox("Error", "Username or Password Incorrect", parent=None)

            



#This function checks which button has been pressed and acts accordingly on the register page, making the current window close and the chosen one to open.

def bs_registerPress(button):


    #Storing my global variables for later - I plan to use the first name on the login screen for a greeting message using their name for a sense of familiarity
    #I plan to use the userID for booking creation, rescheduling and deletion as well as changing passwords.
    
    global currentUserFirstName
    global currentUserID
    
    if button == "Return":

        app.show() #Returns user to initial screen.
        app.hideSubWindow("win_Reg")#Closes registration window.

#The if statement and its condition above ensures that users can return back to the initial page to login instead,
#If they picked register on accident. The else statement below takes and stores the user's inputs and eventually, once I have coded it, will add this information
#To the database and henceforth allow the user to login using their credentials. However, I will also prevent any incorrect information being allowed - examples:
#Email input HAS to have "@", password must be > 8 chars with a number and symbol, no numbers in first + last names, etc etc.
#Additionally, I've added some lines which print the stored values/variables to ensure it stores and takes the information given for some testing.


    else:

        #Getting and storing all data/info from the entry boxes.

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

        #Printing all values to ensure they've been stored - I'll remove this later as it's only for me and testing.
        
        #Checking the validity of the entered information

        EInfoValidity = bs_checkRegInfo(regFName,regLName,regUser,regEmail,regPass,regCPass) #Calling the function for registration information checking.

        if EInfoValidity == True:
            
            currentID=cur.execute("Select max(userID) from bs_tblUsers")
            resultID=cur.fetchone()
            newID=int(resultID[0])+1

            userBarber = False

            #Creating a new userID for the new user.

            cur.execute(""" INSERT INTO bs_tblUsers VALUES(?,?,?,?,?,?,?)""",[newID,regEmail,regUser,regFName,regLName,regPass,userBarber])
            con.commit()

            #Adding the user to the database with all their details.

            currentUserFirstName == regFName
            currentUserID == newID

            #The global variables now have their values
            
            print(currentUserID,"yeah it works") #Ignore this, this is just for me to check it has worked.
            
            app.warningBox("Account Created", "Your account has been created successfully!", parent=None)
            app.setLabel("home_title", f"Welcome {regFName}!")
            app.hideSubWindow("win_Reg")
            app.showSubWindow("win_Home")

            #Telling the user they've successfully created their account using a warning box, now taking them to the home screen (showSubWindow), hiding the registration screen (hideSubWindow) and making the welcome message read their name (setLabel).

        else:

            #If the details were invalid, a warning box opens up to tell the user.

            app.warningBox("Error", "The details you have entered are not valid.\nPlease remember that your password must be greater than 8 characters, contain an uppercase letter, a lowercase letter, a number a symbol and both must match.", parent=None)

        

#This function checks which button has been pressed and acts accordingly on the initial page, making the current window close and the chosen one to open.
        
def bs_initialPress(button):

    if button == "Login":
        
        app.hide()
        app.showSubWindow("win_Login")

        #Hides the initial screen, opens the login window.
        
    else:
        app.hide()
        app.showSubWindow("win_Reg")

        #Hides the initial screen, opens the registration window.
        

#This function allows me to skip logging in on the login page temporarily as I continue to create the other interfaces and build the core before functionality - I won't comment this as it is only temporary and will be gone eventually.

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

        #Hides the home screen and opens the haircut booking screen

    elif button == "Cancel Haircut":

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_cancelHaircut_1")

        #Hides the home screen and opens the booking cancellation screen

    elif button == "Reschedule Haircut":

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_rescheduleHaircut_1")

        #Hides the home screen and opens the reschedule booking screen

    else:

        app.hideSubWindow("win_Home")
        app.showSubWindow("win_userSettings")

        #Hides the home screen and opens the settings screen

def bookingSubmit():

    #Getting and storing all data/info from the entry boxes.

    serviceSelection = app.getOptionBox("serviceSelect")
    barberSelection = app.getOptionBox("barberSelect")
    dateSelection = app.getOptionBox("dateSelect")
    timeSelection = app.getOptionBox("timeSelect")
    thisMonth = datetime.now().strftime("%B")

    #Turning the user's chosen time into a time object using the datetime libraries
    #In order to block off/correctly book their appointment and prevent any bookings under 45 mins after.

    timeObject = datetime.strptime(timeSelection, "%H:%M") #Formatted to hours + minutes.

    #Adding 15 minutes to the booking time and then each result to reach a total of 45 minutes after the booking.
    #E.g. chosen time is 12:00pm, so 12:15, 12:30 and 12:40 are also stored.

    #Need to make sure double bookings still cannot occur by adding a check to see if there is already a booking - with that barber, on that day, at that time.

    resultObject_1 = timeObject + timedelta(minutes=15)
    resultObject_2 = resultObject_1 + timedelta(minutes=15)
    resultObject_3 = resultObject_2 + timedelta(minutes=15)

    #Turning the resulting time objects in their increments of 15 back into strings.

    resultObject_1 = resultObject_1.strftime("%H:%M")
    resultObject_2 = resultObject_2.strftime("%H:%M")
    resultObject_3 = resultObject_3.strftime("%H:%M")

    #Small check for me to see how the program is progressing.

    print(resultObject_1,resultObject_2,resultObject_3)

    #Storing the incremented objects in an array so they can be iterated through later.

    objectArray = [resultObject_1,resultObject_2,resultObject_3]

    for x in range(0,len(objectArray)): #Loop to iterate through the array.

        appendTo = objectArray[x]
        if appendTo >= "12:00":

            resultAppend = appendTo + "pm"

        else:

            resultAppend = appendTo + "am"

        objectArray[x] = resultAppend #Changing the original value to the new one with its new suffix

        print(resultAppend)
        print(objectArray)
    

    if timeSelection >= "12:00":

        timeSelection = timeSelection + "pm"

        #Adding the corrent suffix for the time.

    else:

        timeSelection = timeSelection + "am"

        #Adding the corrent suffix for the time.
    

    if serviceSelection == "Select a service":

        app.warningBox("Error", "Please choose a service.")

        #Ensuring the user does not and cannot proceed without choosing a service

    else:

        app.warningBox("Booking made", f"You booked: {serviceSelection} at {timeSelection} on {dateSelection} {thisMonth} with {barberSelection}.\n \nYou will receive an email confirmation and will be sent a reminder before your appointment by email.")

        #Lets user know their booking has been made

        currentBID = cur.execute("SELECT max(bookingID) FROM bs_tblBookings") 
        resultBID = cur.fetchone()

        #Getting the current bookingID to increment it as a new booking has been made. // For the insertion of the booking into the database.

        if resultBID and resultBID[0] is not None: #If resultBID exists and isn't equal to "None";

            newBID = int(resultBID[0])+1 #Incrementing the bookingID for this booking. // For the insertion of the booking into the database.

        else:

            #Means this is the first booking, so it takes 1 as its booking number

            newBID = 1

        bookingStatus = "Booked"

        #Setting the current status of the booking - I'll need to possibly find a way to make it so bookings are either cleared after the date + time of the booking or maybe the barbers can possibly press a button in their interface (as it's different to a customer's interface)
        #Which will drop it from all relevant tables in the database - This will be for Prototype 2, as I'm currently working on 1 which is focused on core functionality and primarily user experience.

        getServiceID = cur.execute("SELECT serviceID FROM bs_tblServices WHERE serviceName = ?", (serviceSelection,)) #Searching for the corresponding serviceID using the serviceName for insertion into the database.
        serviceIDArray = cur.fetchone()

        resultServiceID = serviceIDArray[0] #Storing the result

        getServicePrice = cur.execute("SELECT price FROM bs_tblServices WHERE serviceName = ?", (serviceSelection,)) #Searching for the corresponding service's price using the serviceName for insertion into the database.
        servicePriceArray = cur.fetchone()
        
        resultServicePrice = float(servicePriceArray[0]) #Storing the result
        
        cur.execute(""" INSERT INTO bs_userBooking VALUES(?,?,?)""",[currentUserID,newBID,timeSelection])
        con.commit()

        for y in range(0,len(objectArray)):

            curValue = objectArray[y]

            cur.execute(""" INSERT INTO bs_userBooking VALUES (?,?,?) """,[currentUserID,newBID,curValue])
            con.commit()

        cur.execute(""" INSERT INTO bs_tblBookings VALUES(?,?,?,?,?,?,?,?)""",[newBID,resultServiceID,currentUserID,barberSelection,serviceSelection,dateSelection,bookingStatus, resultServicePrice]) #Inserting all booking details into the bookings table.
        con.commit() #Adds the booking into the database and their tables
        
        app.hideSubWindow("win_bookHaircut")
        app.showSubWindow("win_Home")

        #Returns user to the home screen after they've made their booking and have closed the warning box/window.

#This function checks the booking number given by the user to see if the booking exists, either preventing them from progressing them or allowing them to progress

def cancel_bookingNumberCheck():

    app.hideSubWindow("win_cancelHaircut_1")
    app.showSubWindow("win_cancelHaircut_2")

#This function checks the password given by the user for additional security - if it's correct they can progress and cancel but if it's incorrect they cannot.

def cancel_passwordCheck():

    app.hideSubWindow("win_cancelHaircut_2")
    app.showSubWindow("win_cancelHaircut_3")

#This function checks the booking number given by the user to see if the booking exists, either preventing them from progressing them or allowing them to progress

def reschedule_bookingNumberCheck():

    app.hideSubWindow("win_rescheduleHaircut_1")
    app.showSubWindow("win_rescheduleHaircut_2")

#This function checks the password given by the user for additional security - if it's correct they can progress and cancel but if it's incorrect they cannot.
    
def reschedule_passwordCheck():

    app.hideSubWindow("win_rescheduleHaircut_2")
    app.showSubWindow("win_rescheduleHaircut_3")

#This function checks which button has been pressed on the final cancellation screen, to either cancel or not cancel the booking.

def cancelPress(button):

    if button == "Cancel Booking":

        app.warningBox("Booking Cancelled","Your booking has been cancelled successfully.")

        app.hideSubWindow("win_cancelHaircut_3")
        app.showSubWindow("win_Home")

    else:

        app.warningBox("Warning","Your booking has not been cancelled")

        app.hideSubWindow("win_cancelHaircut_3")
        app.showSubWindow("win_Home")

#This function checks which button has been pressed on the final rescheduling screen, to either reschedule or not reschedule the booking.

def reschedulePress(button):

    if button == "Reschedule Booking":

        app.warningBox("Booking Rescheduled","Your booking has been rescheduled successfully.")

        app.hideSubWindow("win_rescheduleHaircut_3")
        app.showSubWindow("win_Home")

    else:

        app.warningBox("Warning","Your booking has not been rescheduled")

        app.hideSubWindow("win_rescheduleHaircut_3")
        app.showSubWindow("win_Home")
        
#This function checks which button has been pressed on the user settings page in order to determine which window to open for the user.

def settingsPress(button):

    if button == "Change Password":

        app.hideSubWindow("win_userSettings")
        app.showSubWindow("win_changePassword")

    else:

        app.hideSubWindow("win_userSettings")
        app.showSubWindow("win_editDetails")

#This function changes the user's password while also checking the validity of the old password and the new password with the secondary entry box.

def changePasswordPress(button):

    if button == "Confirm Change":

        app.hideSubWindow("win_changePassword")
        app.showSubWindow("win_Home")

        app.warningBox("Warning","Your password has been changed successfully.")

    else:

        app.hideSubWindow("win_changePassword")
        app.showSubWindow("win_Home")

        app.warningBox("Warning","Your password has not been changed")

#This function edits the user's details while also checking the validity of the details to ensure they're valid.

def editDetailsPress(button):

    if button == "Confirm Edits":

        app.hideSubWindow("win_editDetails")
        app.showSubWindow("win_Home")

        app.warningBox("Warning","Your details have been edited successfully.")

    else:

        app.hideSubWindow("win_editDetails")
        app.showSubWindow("win_Home")

        app.warningBox("Warning","Your details have not been edited.")

################ INTERFACE ################




#Creating the interface

#Sets the initial window name and its resolution

app = gui("Half-Life Hair", "900x600")

def bs_createInterface():

######## Initial Page ########


#This code is for the first screen the user will see, asking them to login or sign up.

    #The visuals are set here - background and text colours.

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

    #The visuals are set here - background and resolution.

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

    #Button colours are changed here to fit the standard colour scheme of the barber shop branding as well as the window's font size.

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

    #The visuals are set here - background colour and resolution, label colours and font size.
    
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

    #Button colours are changed here to fit the standard colour scheme of the barber shop branding as well as the window's font size.
    
    app.setButtonBg("Submit", "#ff8039")
    app.setButtonBg("Cancel", "#ff8039")
    app.setButtonBg("Forgot Password", "#ff8039")
    app.setButtonFg("Submit", "#152b6d")
    app.setButtonFg("Cancel", "#152b6d")
    app.setButtonFg("Forgot Password", "#152b6d")
    
    app.stopSubWindow()

######## Homepage ########

    #Able to reuse some of my previous code such as for setting the window size, background colour and font size/colouring.

    #The visuals are set here - background colour and resolution, label colours and font size.

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

    #Button colours are changed here to fit the standard colour scheme of the barber shop branding as well as the window's font size.

    app.setButtonBg("Book Haircut", "#ff8039")
    app.setButtonBg("Cancel Haircut", "#ff8039")
    app.setButtonBg("Reschedule Haircut", "#ff8039")
    app.setButtonBg("Settings", "#ff8039")
    app.setButtonFg("Book Haircut", "#152b6d")
    app.setButtonFg("Cancel Haircut", "#152b6d")
    app.setButtonFg("Reschedule Haircut", "#152b6d")
    app.setButtonFg("Settings", "#152b6d")


    app.stopSubWindow()


######## Create Booking Page ########

    #The visuals are set here - background colour and resolution, label colours and font size.

    app.startSubWindow("win_bookHaircut")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)

    app.addLabel("booking_title","Book Haircut")

    #Getting all the services from the database to put into the selection box so users can choose their service.

    cur.execute("SELECT serviceName FROM bs_tblServices")
    services = [row[0] for row in cur.fetchall()]
    services.insert(0, "Select a service")

    timeSlots = [
        "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", 
        "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", 
        "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", 
        "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", 
        "17:00", "17:15", "17:30", "17:45", "18:00"
    ]
    #All timeslots for the user to choose from when the shop is open - added to the option box so they can choose.
    currentMonth = datetime.now().month

    dates = []
    
    if currentMonth == 2: #This if/else statement decides how many days are to be listed depending on what month it is, which can then be put into the option box so the user can choose.
        
        for i in range(1, 29):  # February typically has 28 or 29 days - so the days available only go so far.
            
            dates.append(f"{i}")
            
    elif currentMonth in [4, 6, 9, 11]:
        
        for i in range(1, 31):  # April, June, September, November have 30 days- so the days available only go so far.
            
            dates.append(f"{i}")
            
    else:
        
        for i in range(1, 32):  # Other months have 31 days- so the days available only go so far.

            dates.append(f"{i}")


    #This array stores all the barbers, I could have taken the barberNames from the database though.

    barbers = ["Alex Vance","Barney Calhoun","Gordon Freigh-Mann","Francis Mesa"]
    
    
    app.addOptionBox("serviceSelect",services)
    app.addOptionBox("barberSelect", barbers)
    app.addOptionBox("dateSelect",dates)
    app.addOptionBox("timeSelect",timeSlots)
    
    app.addButton("Make booking",bookingSubmit)
    

    #Setting the colours of the label and options boxes.
    
    app.setLabelFg("booking_title","#ff8039")
    
    app.setOptionBoxFg("serviceSelect", "#ff8039")
    app.setOptionBoxFg("barberSelect", "#ff8039")
    app.setOptionBoxFg("dateSelect", "#ff8039")
    app.setOptionBoxFg("timeSelect", "#ff8039")
    app.setOptionBoxBg("serviceSelect", "white")
    app.setOptionBoxBg("barberSelect", "white")
    app.setOptionBoxBg("dateSelect", "white")
    app.setOptionBoxBg("timeSelect", "white")
    

    app.stopSubWindow()

######## Cancel Booking Page Part 1 ########

    app.startSubWindow("win_cancelHaircut_1")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)
    
    app.addLabel("cancel_title_1","Cancel Haircut")
    app.setLabelFg("cancel_title_1","#ff8039")

    app.addLabel("cancel_guide_1","Please enter the booking number from the\n booking confirmation sent to your email")
    app.setLabelFont("cancel_guide_1", size = 14)

    app.addLabelEntry("Enter Booking Number:")

    app.addButton("Submit Number",cancel_bookingNumberCheck)
    
    
    app.stopSubWindow()

#Forgot to add button to return if they made a mistake and came here on accident

######## Cancel Booking Page Part 2 ########

    app.startSubWindow("win_cancelHaircut_2")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)
    
    app.addLabel("cancel_title_2","Cancel Haircut")
    app.setLabelFg("cancel_title_2","#ff8039")

    app.addLabel("cancel_guide_2","Please enter your password for additional security")
    app.setLabelFont("cancel_guide_2", size = 14)

    app.addLabelEntry("Enter your Password:")

    app.addButton("Submit Password",cancel_passwordCheck)
    

    app.stopSubWindow()
    

######## Cancel Booking Page Part 3 ########

    app.startSubWindow("win_cancelHaircut_3")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)
    
    app.addLabel("cancel_title_3","Cancel Haircut")
    app.setLabelFg("cancel_title_3","#ff8039")

    app.addLabel("cancel_guide_3","Are you sure you want to cancel your booking? You can always reschedule it instead!")
    app.setLabelFont("cancel_guide_3", size = 14)

    app.addButtons(["Cancel Booking", "Don't Cancel"],cancelPress)

    app.stopSubWindow()

######## Reschedule Booking Page Part 1 ########

    app.startSubWindow("win_rescheduleHaircut_1")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)

    app.addLabel("reschedule_title_1","Reschedule Haircut")
    app.setLabelFg("reschedule_title_1","#ff8039")

    app.addLabel("reschedule_guide_1","Please enter the booking number from the\n booking confirmation sent to your email")
    app.setLabelFont("reschedule_guide_1", size = 14)

    app.addLabelEntry("Booking Number Entry:")

    app.addButton("Submit Booking Number",reschedule_bookingNumberCheck)

    app.stopSubWindow()

#Forgot to add button to return if they made a mistake and came here on accident


######## Reschedule Booking Page Part 2 ########

    app.startSubWindow("win_rescheduleHaircut_2")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)

    app.addLabel("reschedule_title_2","Reschedule Haircut")
    app.setLabelFg("reschedule_title_2","#ff8039")

    app.addLabel("reschedule_guide_2","Please enter your password for additional security")
    app.setLabelFont("reschedule_guide_2", size = 14)

    app.addLabelEntry("Password Entry:")

    app.addButton("Submit Your Password",reschedule_passwordCheck)

    app.stopSubWindow()
    

######## Reschedule Booking Page Part 3 ########

    app.startSubWindow("win_rescheduleHaircut_3")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)

    app.addLabel("reschedule_title_3","Reschedule Haircut")
    app.setLabelFg("reschedule_title_3","#ff8039")

    timeSlots = [
        "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", 
        "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", 
        "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", 
        "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", 
        "17:00", "17:15", "17:30", "17:45", "18:00"
    ]

    currentMonth = datetime.now().month

    dates = []
    
    if currentMonth == 2:
        
        for i in range(1, 29):  # February typically has 28 or 29 days - so the days available only go so far.
            
            dates.append(f"{i}")
            
    elif currentMonth in [4, 6, 9, 11]:
        
        for i in range(1, 31):  # April, June, September, November have 30 days- so the days available only go so far.
            
            dates.append(f"{i}")
            
    else:
        
        for i in range(1, 32):  # Other months have 31 days- so the days available only go so far.

            dates.append(f"{i}")


    #This array stores all the barbers, I could have taken the barberNames from the database though.

    barbers = ["Alex Vance","Barney Calhoun","Gordon Freigh-Mann","Francis Mesa"]
    
    app.addOptionBox("barberReschedule", barbers)
    app.addOptionBox("dateReschedule",dates)
    app.addOptionBox("timeReschedule",timeSlots)
    

    #Setting the colours of the label and options boxes.
    
    app.setLabelFg("booking_title","#ff8039")
    
    app.setOptionBoxFg("barberReschedule", "#ff8039")
    app.setOptionBoxFg("dateReschedule", "#ff8039")
    app.setOptionBoxFg("timeReschedule", "#ff8039")
    app.setOptionBoxBg("barberReschedule", "white")
    app.setOptionBoxBg("dateReschedule", "white")
    app.setOptionBoxBg("timeReschedule", "white")

    app.addButtons(["Reschedule Booking", "Don't Reschedule"],reschedulePress)

    app.stopSubWindow()


######## Settings Page ########

    app.startSubWindow("win_userSettings")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)
    
    app.addLabel("settings_title","Settings")

    app.addButtons(["Change Password","Edit Details"],settingsPress)
    
    app.setLabelFg("settings_title","#ff8039")

    app.stopSubWindow()

######## Change Password Page ########

    app.startSubWindow("win_changePassword")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)
    
    app.addLabel("changePassword_title","Change Password")

    app.addLabelEntry("Old Password:")
    app.addLabelEntry("New Password:")
    app.addLabelEntry("Confirm New Password:")

    app.addButtons(["Confirm Change","Cancel Change"],changePasswordPress)
    
    app.setLabelFg("changePassword_title","#ff8039")

    app.stopSubWindow()

######## Edit Details Page ########

    app.startSubWindow("win_editDetails")
    app.setSize("900x600")
    app.setBg("#152b6d")
    app.setFont(20)
    
    app.addLabel("editDetails_title","Edit Details")
    
    app.addLabelEntry("Change First name:")
    app.addLabelEntry("Change Last name:")
    app.addLabelEntry("       Change Email:")

    app.addButtons(["Confirm Edits","Cancel Edits"],editDetailsPress)
    
    app.setLabelFg("editDetails_title","#ff8039")

    app.stopSubWindow()
    
    app.go()

bs_createInterface()

#Main
