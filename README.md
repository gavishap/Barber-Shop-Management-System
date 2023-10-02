Barber Shop Management System

This project is a Barber Shop Management System built using Python, Tkinter, and MongoDB. It provides a user-friendly interface for managing appointments, purchasing merchandise, and handling customer support tickets.
Features

1. User Authentication: The system supports user login and validation.
2. Appointment Management: Users can book, view, and cancel appointments.
3. Merchandise Management: Users can view, add to cart, and purchase merchandise.
4. Customer Support: Users can submit support tickets and view responses.
Dependencies

The project requires the following Python libraries:

- Tkinter for GUI
- PyMongo for MongoDB integration

These can be installed using the requirements.txt file:
Running the Application

To run the application, execute the main.py script:
Project Structure

The project is structured into several Python scripts:

- main.py: The entry point of the application.
- gui.py: Contains the GUI logic.
- database.py: Handles all database operations.
- appointment.py: Manages appointment-related operations.
- customer_support.py: Manages customer support ticket operations.
- merchandise.py: Manages merchandise-related operations.
Database

The application uses MongoDB for data storage. The database is structured into several collections:

- Users
- Appointments
- Merchandise
- Barbers
- CustomerSupport
