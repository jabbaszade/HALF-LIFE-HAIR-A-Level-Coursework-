import sqlite3

con = sqlite3.connect("bs_systemDB.db")
cur = con.cursor()

userTest = input("username:")
passTest = input("password:")

cur.execute("""SELECT username FROM bs_tblUsers WHERE username = ?""",(userTest,))

RESULT = cur.fetchone()

if RESULT is not None:

    username = RESULT[0]

    if username == userTest:
                     cur.execute("""SELECT password FROM bs_tblUsers WHERE username = ?""",(userTest,))

                     RESULT2 = cur.fetchone()

                     if RESULT2 is not None:

                         password = RESULT2[0]

                         if passTest == password:
                             print("password correct")
                         else:
                            print("password incorrect")
                     else: print("password incorrect")
                                      
else:
    print("username incorrect/doesnt exist")
    
