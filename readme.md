# Airline Ticket Reservation System

## Project Overview
This project is a Python-based **Airline Ticket Reservation System** developed as part of **Basic Programming – Assignment 3**.  
The system simulates a simplified airline ticket booking process using fundamental programming concepts such as arrays, object-oriented programming (OOP), recursion, string manipulation, and file handling.

The application operates through a **menu-based text interface** and focuses on logical accuracy, data validation, and structured program design.

---

## System Features

### 1. Book a Ticket
- Allows users to enter passenger details (name and flight code).
- Enables manual or automatic seat assignment.
- Ensures seats cannot be double-booked.
- Updates the seat availability upon successful booking.

### 2. View Available Seats
- Displays the aircraft seating layout using a **2D array (5 × 6)**.
- Shows seat availability status:
  - `O` = Available
  - `X` = Booked
- Displays the total number of available seats.

### 3. Cancel a Booking
- Cancels an existing booking by passenger name.
- Frees the assigned seat and updates the seating layout accordingly.
- Handles cases where multiple passengers share the same name.

### 4. Search Passenger
- Searches passenger records using **string-based comparison**.
- Supports partial and case-insensitive name matching.
- Displays passenger name, seat number, and flight code.

### 5. Save Bookings
- Saves all booking records into a text file (`bookings.txt`).
- Ensures data persistence for future sessions.

### 6. Load Bookings
- Loads booking data from `bookings.txt`.
- Reconstructs passenger records and seat availability.
- Automatically resets and updates the seat layout.

### 7. Exit
- Safely terminates the program.

---

## Programming Concepts Applied

- **Arrays (2D List)**: Used to manage aircraft seat layout.
- **Object-Oriented Programming (OOP)**: Passenger data is represented using a `Passenger` class.
- **Recursion**: Applied to traverse and count seat availability.
- **String Manipulation**: Used for passenger search and data validation.
- **File Handling**: Booking data is saved and loaded using text files.
- **Control Structures**: Utilizes sequence, selection, and repetition logic.

---

## How to Run the Program

1. Ensure Python is installed on your system.
2. Place `airline_reservation.py` in a folder.
3. Open a terminal or command prompt in that folder.
4. Run the program using:

5. Follow the on-screen menu instructions.

---

## Notes
- The system uses a text-based interface as required.
- The code includes comments and function-level documentation (docstrings).
- The program runs without syntax errors and meets all assignment requirements.

---

## Author
Yong Ting En 
Basic Programming – Assignment 3

## Link
https://github.com/tingen1031/Airline-Ticket-Reservation-System
