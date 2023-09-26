import tkinter as tk
import uuid
from tkinter import simpledialog

class CustomerSupport:
    def __init__(self, root, db,dashboard, user, barber=None):
        self.root = root
        self.db = db
        self.barber = barber
        self.dashboard = dashboard
        self.user = user 
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.create_widgets()

    def create_widgets(self):
        if self.barber:
            tickets = self.db.get_tickets()
            for ticket in tickets:
                if 'status' in ticket and ticket['status'] == 'Open':
                    tk.Button(self.frame, text=ticket['ticket'], command=lambda t=ticket: self.respond_ticket(t)).pack()
        else:
            self.ticket_entry = tk.Entry(self.frame)
            self.ticket_entry.pack()
            tk.Button(self.frame, text='Submit Ticket', command=self.submit_ticket).pack()

            tickets = self.db.get_tickets_by_user(self.user['userID'])
            for ticket in tickets:
                tk.Label(self.frame, text=f"Ticket: {ticket['ticket']}").pack()
                if 'response' in ticket:
                    tk.Label(self.frame, text=f"Response: {ticket['response']}").pack()
                else:
                    tk.Label(self.frame, text="No response yet").pack()
                tk.Label(self.frame, text="-----------------------------").pack()
        tk.Button(self.frame, text='Back', command=self.back).pack()

    def respond_ticket(self, ticket):
        self.frame.pack_forget()
        response = simpledialog.askstring("Input", "Enter your response", parent=self.root)
        self.db.update_ticket(ticket['ticketID'], response)
        self.dashboard.display_dashboard()

    def submit_ticket(self):
        ticket = self.ticket_entry.get()
        ticket_id = str(uuid.uuid4())
        user_id = self.user['userID']  
        self.db.add_ticket({
            "ticketID": ticket_id,
            "userID": user_id,
            "status": "Open",
            "response": "",
            "ticket": ticket
        })
        self.frame.pack_forget()  
        self.dashboard.display_dashboard()

    def back(self):
        self.frame.destroy()
        self.dashboard.display_dashboard()
        