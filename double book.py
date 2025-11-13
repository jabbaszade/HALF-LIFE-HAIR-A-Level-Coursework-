import sqlite3
from appJar import gui

# Connect to the database
def fetch_todays_bookings():
    conn = sqlite3.connect("bs_systemDB.db")
    cursor = conn.cursor()

    # Change this line depending on how your system stores booking dates
    # Here we assume today's bookingDate is 1 (based on your test data)
    today = 1

    cursor.execute("""
        SELECT 
            b.bookingID,
            b.barberName,
            b.serviceName,
            b.price,
            u.bookingTime,
            us.firstName || ' ' || us.lastName as fullName
        FROM bs_tblBookings b
        JOIN bs_userBooking u ON b.bookingID = u.bookingID
        JOIN bs_tblUsers us ON b.userID = us.userID
        WHERE b.bookingDate = ?
    """, (today,))

    bookings = cursor.fetchall()
    conn.close()
    return bookings

# Build the appJar window
def create_gui():
    app = gui("Today's Bookings", "700x400")
    app.setFont(14)

    bookings = fetch_todays_bookings()

    if bookings:
        app.addLabel("l1", "Bookings for Today", 0, 0, 2)
        app.setLabelAlign("l1", "center")

        headers = ["Booking ID", "Barber", "Service", "Price (£)", "Time", "Customer Name"]
        app.addTable("bookings", [headers] + bookings)
    else:
        app.addLabel("noBookings", "No bookings found for today.")

    app.go()

create_gui()
