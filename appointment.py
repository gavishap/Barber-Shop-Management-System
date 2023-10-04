import tkinter as tk
from datetime import datetime
from tkinter import simpledialog
from datetime import datetime, timedelta
import uuid
from tkinter import ttk
   
class Appointment:
    def __init__(self, root, db, user, dashboard, barber=None, add=False):
        self.root = root
        self.db = db
        self.user = user
        self.barber = barber
        self.dashboard = dashboard
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        if add:
            self.create_add_widgets()
        else:
            self.create_widgets()

    def create_add_widgets(self):
        tk.Label(self.frame, text="Start Time").pack()
        self.start_var = tk.StringVar(self.frame)
        times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 30)]
        self.start_menu = tk.OptionMenu(self.frame, self.start_var, *times)
        self.start_menu.pack()

        tk.Label(self.frame, text="End Time").pack()
        self.end_var = tk.StringVar(self.frame)
        self.end_menu = tk.OptionMenu(self.frame, self.end_var, *times)
        self.end_menu.pack()

        tk.Label(self.frame, text="Date (YYYY-MM-DD)").pack()
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.pack()

        tk.Button(self.frame, text='Add Appointments', command=self.add_appointments).pack()
        tk.Button(self.frame, text='Back', command=self.back).pack()
        

    #suck me

    def add_appointments(self):
        start_time = datetime.strptime(self.start_var.get(), "%H:%M")
        end_time = datetime.strptime(self.end_var.get(), "%H:%M")
        date = self.date_entry.get()
        while start_time < end_time:
            appointment = {
                "appointmentID": str(uuid.uuid4()),
                "barberID": self.barber,
                "date": date,
                "time": start_time.strftime("%H:%M")
            }
            self.db.add_appointment(appointment)
            start_time += timedelta(minutes=30)
        self.back()

    def create_widgets(self):
        self.appointment_list = list(self.db.get_appointments())
        self.appointment_list.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))  # Sort appointments by date

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days_of_week:
            day_appointments = [appt for appt in self.appointment_list if datetime.strptime(appt['date'], "%Y-%m-%d").weekday() == days_of_week.index(day)]
            day_appointments.sort(key=lambda x: datetime.strptime(x['time'], "%H:%M"))  # Sort appointments by time within each day
            if day_appointments:
                tk.Label(self.frame, text=day).grid(row=0, column=days_of_week.index(day))  # Display the day of the week
                for appointment in day_appointments:
                    button_text = appointment['time']
                    button_command = lambda appt=appointment: self.book(appt) if 'userID' not in appt else self.cancel(appt)
                    button_color = "light green" if 'userID' not in appointment else "red"
                    tk.Button(self.frame, text=button_text, command=button_command, bg=button_color).grid(row=day_appointments.index(appointment) + 1, column=days_of_week.index(day))
        tk.Button(self.frame, text='Back', command=self.back).grid(row=len(self.appointment_list) + 1, column=0, columnspan=len(days_of_week))

    def cancel(self, appointment):
        self.db.cancel_appointment(appointment)
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.db.clean_appointments()

    

    def book(self, appointment):
        if 'userID' in appointment:
            print("This appointment is already booked.")
            return

        # If the user is None or a barber, prompt for a username
        if self.user is None or self.barber is not None:
            user_names = [user['username'] for user in self.db.get_users()]  # Get all user names from the db.Users collection
            self.user_var = tk.StringVar()
            self.user_combobox = ttk.Combobox(self.frame, textvariable=self.user_var, values=user_names)
            self.user_combobox.grid()  # Use grid instead of pack
            self.user_combobox.bind("<<ComboboxSelected>>", lambda _: self.book_appointment(appointment))  # Book the appointment when a user is selected
        else:
            user = self.user
            self.book_appointment(appointment, user)

    def book_appointment(self, appointment, user=None):
        if user is None:  # If the user is not provided, fetch the selected user from the database
            username = self.user_var.get()  # Get the selected user name from the Combobox widget
            user = self.db.db.Users.find_one({'username': username})

        if user is None:
            print("User not found.")
            return

        self.db.db.Users.update_one(
            {'userID': user['userID']},
            {'$push': {'appointments': appointment['appointmentID']}}
        )

        self.db.db.Appointments.update_one(
            {'appointmentID': appointment['appointmentID']},
            {'$set': {'userID': user['userID']}}
        )

        # Refresh the display
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.db.clean_appointments()

    def back(self):
        # Destroy the current frame and display the main dashboard
        self.frame.destroy()
        self.dashboard.display_dashboard()