import tkinter as tk
from tkinter import messagebox
from database import *
from appointment import *
from merchandise import *
from customer_support import *
from tkinter import simpledialog
import uuid

class BarberDashboard:
    def __init__(self, root, db, barber):
        self.root = root
        self.db = db
        self.barber = barber
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Welcome to BarberShop App!").pack(pady=10)
        
        tk.Button(self.frame, text='Add Customer', command=self.add_customer).pack(pady=5)
        tk.Button(self.frame, text='Add Appointments', command=self.open_appointments).pack(pady=5)
        tk.Button(self.frame, text='Add Merchandise', command=self.open_merchandise).pack(pady=5)
        tk.Button(self.frame, text='Book Appointments', command=self.book_appointments).pack(pady=5)
        tk.Button(self.frame, text='Customer Support Tickets', command=self.open_customer_support_tickets).pack(pady=5)
        tk.Button(self.frame, text='Logout', command=self.logout).pack(pady=5)
        
    
    def add_customer(self):
        username = simpledialog.askstring("Input", "Enter the username", parent=self.root)
        password = simpledialog.askstring("Input", "Enter the password", parent=self.root)
        email = simpledialog.askstring("Input", "Enter the email", parent=self.root)
        # Add more fields as needed

        # Generate a unique userID
        userID = str(uuid.uuid4())

        # Add the new customer to the database
        self.db.add_user({
            'userID': userID,
            'username': username,
            'password': password,
            'email': email,
            'appointments': [],
            'purchases': []
        })
        
    def open_appointments(self):
        self.frame.pack_forget()  # Hide the dashboard
        Appointment(self.root, self.db, None, self, self.barber, True)

    def open_merchandise(self):
        self.frame.pack_forget()  # Hide the dashboard
        Merchandise(self.root, self.db, self, None, None, self.barber)

    def book_appointments(self):
        self.frame.pack_forget()  # Hide the dashboard
        Appointment(self.root, self.db, None, self, self.barber)

    def open_customer_support_tickets(self):
        self.frame.pack_forget()  # Hide the dashboard
        CustomerSupport(self.root, self.db, self, None,self.barber)  # Open the support tickets screen

    def display_dashboard(self):
        self.frame.pack()
    
    def logout(self):
            self.frame.destroy()
            Login(self.root, self.db)

class Login:
    def __init__(self, root, db, user=None):
        self.root = root
        self.db = db
        self.user = user
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.frame.config(bg='lightblue')  # Set the background color of the frame

        tk.Label(self.frame, text="Username:", bg='lightblue', fg='black', font=('Helvetica', 14)).pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=('Helvetica', 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg='lightblue', fg='black', font=('Helvetica', 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", font=('Helvetica', 12))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.frame, text="Login", command=self.check_credentials)
        login_button.config(font=('Helvetica', 14), bg='blue', fg='white', relief=tk.RAISED, bd=5)
        login_button.pack(pady=20)

    def check_credentials(self):
        name = self.username_entry.get()
        password = self.password_entry.get()

        validation_status, user = self.db.validate_user(name, password)

        if validation_status == "valid":
            self.frame.pack_forget()  # Hide the login frame
            Dashboard(self.root, self.db, user)
        elif validation_status == "barber":
            self.frame.pack_forget()  # Hide the login frame
            BarberDashboard(self.root, self.db, name)
        elif validation_status == "no_user":
            messagebox.showerror("Error", "No user or barber by that name!")
        else:
            messagebox.showerror("Error", "Invalid password!")

    


class Dashboard:
    def __init__(self, root, db, user):
        self.root = root
        self.db = db
        self.user = user
        self.cart = Cart(db, user, root)
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.create_widgets()

    def create_widgets(self):
        self.frame.config(bg='lightblue')  # Set the background color of the frame

        # Removed the username and password fields and login button
        my_appointments= tk.Button(self.frame, text='My Appointments', command=self.view_appointments)
        my_appointments.pack(pady=20)

        appointments_button = tk.Button(self.frame, text="Book Appointments", command=self.open_appointments)
        appointments_button.pack(pady=20)

        merchandise_button = tk.Button(self.frame, text="Merchandise", command=self.open_merchandise)
        merchandise_button.pack(pady=20)

        support_button = tk.Button(self.frame, text="Customer Support", command=self.open_customer_support)
        support_button.pack(pady=20)

        logout_button = tk.Button(self.frame, text="Logout", command=self.logout)
        logout_button.pack(pady=20)


    def view_appointments(self):
    # Clear the current frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Fetch the user's appointments
        user_appointments = [appt for appt in self.db.get_appointments() if 'userID' in appt and appt['userID'] == self.user['userID']]

        # Display the user's appointments
        for i, appointment in enumerate(user_appointments):
            tk.Label(self.frame, text=f"Appointment {i+1}:").pack()
            tk.Label(self.frame, text=f"Date: {appointment['date']}").pack()
            tk.Label(self.frame, text=f"Time: {appointment['time']}").pack()

        # Add a 'Back' button
        back_button = tk.Button(self.frame, text="Back", command=self.display_dashboard)
        back_button.pack(pady=20)

        
    def open_appointments(self):
        self.frame.pack_forget()  # Hide the dashboard
        Appointment(self.root, self.db, self.user, self)

    def open_merchandise(self):
        self.frame.pack_forget()  # Hide the dashboard
        Merchandise(self.root, self.db, self, self.cart, self.user)

    def open_customer_support(self):
        self.frame.pack_forget()  # Hide the dashboard
        CustomerSupport(self.root, self.db, self, self.user)  

    def display_dashboard(self):
        # Clear the current frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Recreate the dashboard widgets
        self.create_widgets()

        # Pack the frame again
        self.frame.pack()

    def logout(self):
        self.frame.destroy()
        Login(self.root, self.db)

def run():
    root = tk.Tk()
    root.configure(bg='lightblue')  # Set the background color of the entire window
    root.geometry("600x500")  # Set initial window size to 800x600 pixels
    db = Database()
    Login(root, db)  # Start with the login page
    root.mainloop()