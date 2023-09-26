from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['BarberShopDB'] 
    
    # Users collection methods
    def get_users(self):
        return self.db.Users.find()
    def add_user(self, user):
        self.db.Users.insert_one(user)
    
    # Appointments collection methods
    def get_appointments(self):
        return self.db.Appointments.find()
    def add_appointment(self, appointment):
        self.db.Appointments.insert_one(appointment)
    def cancel_appointment(self, appointment):
        self.db.Appointments.update_one({'appointmentID': appointment['appointmentID']}, {'$unset': {'userID': ""}})

    # Merchandise collection methods
    def get_merchandise(self):
        return self.db.Merchandise.find()
    def add_merchandise(self, item):
        self.db.Merchandise.insert_one(item)
    def get_item_by_name(self, name):
        return self.db.Merchandise.find_one({'name': name})
    
    # Barbers collection methods
    def get_barbers(self):
        return self.db.Barbers.find()
    def add_barber(self, barber):
        self.db.Barbers.insert_one(barber)
    
    # CustomerSupport collection methods
    def get_tickets(self):
        return self.db.CustomerSupport.find()
    def get_tickets_by_user(self, user_id):
        return self.db.CustomerSupport.find({'userID': user_id})

    def add_ticket(self, ticket):
        self.db.CustomerSupport.insert_one(ticket)
    def update_ticket(self, ticket_id, response):
        self.db.CustomerSupport.update_one({'ticketID': ticket_id}, {'$set': {'status': 'Resolved', 'response': response}})


    def update_user_purchases(self, user, purchases):
        self.db.Users.update_one({'_id': user['_id']}, {'$push': {'purchases': purchases}})
    

    def validate_user(self, name, password):
        user = self.db.Users.find_one({"username": name})
        barber = self.db.Barbers.find_one({"name": name})

        if user is not None:
            if user["password"] == password:
                return "valid", user
            else:
                return "invalid_password", None
        elif barber is not None:
            if password == "Password":
                return "barber", None
            else:
                return "invalid_password", None
        else:
            return "no_user", None
    
    def clean_appointments(self):
        for user in self.db.Users.find():
            for appointment_id in user['appointments']:
                appointment = self.db.Appointments.find_one({'appointmentID': appointment_id})
                if appointment is None or 'userID' not in appointment:
                    self.db.Users.update_one({'userID': user['userID']}, {'$pull': {'appointments': appointment_id}})