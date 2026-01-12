from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
import os

BOOKINGS_FILE = "bookings.txt"


# ----------------------------- OOP: Passenger ----------------------------- #

@dataclass
class Passenger:
    """Represents a passenger booking record."""
    name: str
    seat_number: str
    flight_code: str

    def to_line(self) -> str:
        """Serialize passenger to a CSV-like line for file storage."""
        # Keep it simple: name,seat,flight
        return f"{self.name},{self.seat_number},{self.flight_code}"

    @staticmethod
    def from_line(line: str) -> Optional["Passenger"]:
        """Deserialize a line into Passenger. Return None if invalid."""
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) != 3:
            return None
        name, seat, flight = parts
        if not name or not seat or not flight:
            return None
        return Passenger(name=name, seat_number=seat, flight_code=flight)


# ----------------------------- Seat Utilities ----------------------------- #

def init_seats(rows: int = 5, cols: int = 6) -> List[List[str]]:
    """Initialize 2D seat map: 'O' = available, 'X' = booked."""
    return [["O" for _ in range(cols)] for _ in range(rows)]


def seat_to_index(seat: str) -> Optional[Tuple[int, int]]:
    """
    Convert seat label like '1A' to (row_index, col_index).
    Row starts at 1, Column starts at A.
    Returns None if invalid format.
    """
    seat = seat.strip().upper()
    if len(seat) < 2:
        return None

    # row number can be 1 or more digits, last char should be a letter
    row_part = seat[:-1]
    col_part = seat[-1]

    if not row_part.isdigit():
        return None
    if not col_part.isalpha() or len(col_part) != 1:
        return None

    row = int(row_part) - 1
    col = ord(col_part) - ord("A")
    return row, col


def index_to_seat(row: int, col: int) -> str:
    """Convert (row_index, col_index) to label like '1A'."""
    return f"{row + 1}{chr(ord('A') + col)}"


def is_valid_index(seats: List[List[str]], row: int, col: int) -> bool:
    """Check if (row, col) within seat map boundaries."""
    return 0 <= row < len(seats) and 0 <= col < len(seats[0])


def display_seat_map(seats: List[List[str]]) -> None:
    """Print a formatted seat map with row/column labels."""
    cols = len(seats[0])
    header = "    " + "  ".join(chr(ord("A") + i) for i in range(cols))
    print(header)
    print("   " + "-" * (len(header) - 3))
    for r, row in enumerate(seats):
        print(f"{r + 1:>2} | " + "  ".join(row))
    print("\nLegend: O = Available, X = Booked\n")


# ----------------------------- Recursion (Optional) ----------------------------- #

def recursive_count_available(seats: List[List[str]], r: int = 0, c: int = 0) -> int:
    """
    Recursively count available seats ('O').
    This is optional advanced task, used for quick availability checks.
    """
    if r >= len(seats):
        return 0
    if c >= len(seats[0]):
        return recursive_count_available(seats, r + 1, 0)

    current = 1 if seats[r][c] == "O" else 0
    return current + recursive_count_available(seats, r, c + 1)


def recursive_find_first_available(seats: List[List[str]], r: int = 0, c: int = 0) -> Optional[Tuple[int, int]]:
    """
    Recursively find first available seat index (row, col).
    Returns None if no seats are available.
    """
    if r >= len(seats):
        return None
    if c >= len(seats[0]):
        return recursive_find_first_available(seats, r + 1, 0)

    if seats[r][c] == "O":
        return (r, c)
    return recursive_find_first_available(seats, r, c + 1)


# ----------------------------- Booking Operations ----------------------------- #

def find_passenger_by_exact_name(passengers: List[Passenger], name: str) -> List[int]:
    """Return indices of passengers whose name matches exactly (case-insensitive)."""
    key = name.strip().lower()
    return [i for i, p in enumerate(passengers) if p.name.strip().lower() == key]


def search_passengers(passengers: List[Passenger], keyword: str) -> List[Passenger]:
    """Return passengers whose name contains keyword (case-insensitive)."""
    key = keyword.strip().lower()
    if not key:
        return []
    return [p for p in passengers if key in p.name.strip().lower()]


def is_seat_taken(passengers: List[Passenger], seat_number: str) -> bool:
    """Check if seat is already in passengers list (safety check)."""
    s = seat_number.strip().upper()
    return any(p.seat_number.strip().upper() == s for p in passengers)


def book_ticket(seats: List[List[str]], passengers: List[Passenger]) -> None:
    """Handle booking logic: input details, validate, assign seat."""
    print("\n--- Book a Ticket ---")
    name = input("Enter passenger name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    flight_code = input("Enter flight code (e.g., MH123): ").strip()
    if not flight_code:
        print("Error: Flight code cannot be empty.")
        return

    # Quick check of available seats
    available = recursive_count_available(seats)
    if available == 0:
        print("No available seats. Booking cannot be made.")
        return

    display_seat_map(seats)
    print(f"Available seats: {available}")

    seat_input = input("Choose seat (e.g., 1A). Type 'AUTO' to assign automatically: ").strip().upper()
    if seat_input == "AUTO":
        found = recursive_find_first_available(seats)
        if not found:
            print("No available seats for auto assignment.")
            return
        row, col = found
        seat_input = index_to_seat(row, col)
        print(f"Auto assigned seat: {seat_input}")

    idx = seat_to_index(seat_input)
    if idx is None:
        print("Error: Invalid seat format. Example valid: 1A, 2C, 5F.")
        return

    row, col = idx
    if not is_valid_index(seats, row, col):
        print("Error: Seat is out of range for this aircraft layout.")
        return

    if seats[row][col] == "X" or is_seat_taken(passengers, seat_input):
        print("Error: Seat is already booked. Please choose another seat.")
        return

    # Mark seat booked
    seats[row][col] = "X"
    passenger = Passenger(name=name, seat_number=seat_input, flight_code=flight_code)
    passengers.append(passenger)

    print(f"Booking successful: {passenger.name} -> Seat {passenger.seat_number}, Flight {passenger.flight_code}")


def cancel_booking(seats: List[List[str]], passengers: List[Passenger]) -> None:
    """Cancel booking by passenger name (exact match), free seat."""
    print("\n--- Cancel a Booking ---")
    name = input("Enter passenger name to cancel: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    matches = find_passenger_by_exact_name(passengers, name)
    if not matches:
        print("No booking found for that name (exact match).")
        print("Tip: Use 'Search Passenger' for partial search.")
        return

    # If multiple, let user choose
    if len(matches) > 1:
        print("Multiple bookings found with the same name. Choose one to cancel:")
        for k, idx in enumerate(matches, start=1):
            p = passengers[idx]
            print(f"{k}. {p.name} | Seat {p.seat_number} | Flight {p.flight_code}")
        try:
            choice = int(input("Select number: ").strip())
            if choice < 1 or choice > len(matches):
                print("Invalid selection.")
                return
            target_index = matches[choice - 1]
        except ValueError:
            print("Invalid input. Cancellation aborted.")
            return
    else:
        target_index = matches[0]

    target = passengers[target_index]
    seat_idx = seat_to_index(target.seat_number)
    if seat_idx:
        r, c = seat_idx
        if is_valid_index(seats, r, c):
            seats[r][c] = "O"  # free seat

    passengers.pop(target_index)
    print(f"Cancelled booking for {target.name}. Seat {target.seat_number} is now available.")


def view_available_seats(seats: List[List[str]]) -> None:
    """Display seat map and available seat count."""
    print("\n--- View Available Seats ---")
    display_seat_map(seats)
    print(f"Available seats (recursion count): {recursive_count_available(seats)}")


def search_passenger_ui(passengers: List[Passenger]) -> None:
    """Search passengers by name keyword."""
    print("\n--- Search Passenger ---")
    keyword = input("Enter name keyword: ").strip()
    results = search_passengers(passengers, keyword)
    if not results:
        print("No matching passengers found.")
        return

    print(f"Found {len(results)} record(s):")
    for p in results:
        print(f"- {p.name} | Seat {p.seat_number} | Flight {p.flight_code}")


# ----------------------------- File Handling ----------------------------- #

def save_bookings(passengers: List[Passenger], filename: str = BOOKINGS_FILE) -> None:
    """Save passenger list to text file."""
    print("\n--- Save Bookings ---")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for p in passengers:
                f.write(p.to_line() + "\n")
        print(f"Bookings saved to '{filename}'. Total records: {len(passengers)}")
    except OSError as e:
        print(f"Error saving file: {e}")


def load_bookings(seats: List[List[str]], filename: str = BOOKINGS_FILE) -> List[Passenger]:
    """
    Load passengers from file and reconstruct seat map.
    If file does not exist, return empty list.
    """
    print("\n--- Load Bookings ---")
    if not os.path.exists(filename):
        print(f"No file found: '{filename}'. Nothing loaded.")
        return []

    loaded: List[Passenger] = []
    # Reset seats first (so reloading is consistent)
    for r in range(len(seats)):
        for c in range(len(seats[0])):
            seats[r][c] = "O"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                p = Passenger.from_line(line)
                if p is None:
                    continue
                # Validate seat exists in seat map
                idx = seat_to_index(p.seat_number)
                if idx is None:
                    continue
                r, c = idx
                if not is_valid_index(seats, r, c):
                    continue
                # Mark seat booked
                seats[r][c] = "X"
                loaded.append(p)

        print(f"Bookings loaded from '{filename}'. Total records: {len(loaded)}")
        return loaded
    except OSError as e:
        print(f"Error loading file: {e}")
        return []


# ----------------------------- Menu Interface ----------------------------- #

def print_menu() -> None:
    """Print the system main menu."""
    print("\n" + "-" * 45)
    print("AIRLINE TICKET RESERVATION SYSTEM")
    print("-" * 45)
    print("1. Book a Ticket")
    print("2. View Available Seats")
    print("3. Cancel a Booking")
    print("4. Search Passenger")
    print("5. Save Bookings")
    print("6. Load Bookings")
    print("7. Exit")
    print("-" * 45)


def main() -> None:
    """Main loop for the reservation system."""
    seats = init_seats(5, 6)  # 5 rows x 6 columns
    passengers: List[Passenger] = []

    # Inline comment block explaining main logic (as required)
    # Main logic:
    # - seats is a 2D list representing availability (O/X)
    # - passengers is a list storing Passenger objects
    # - menu loop executes booking/view/cancel/search/save/load operations

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            book_ticket(seats, passengers)
        elif choice == "2":
            view_available_seats(seats)
        elif choice == "3":
            cancel_booking(seats, passengers)
        elif choice == "4":
            search_passenger_ui(passengers)
        elif choice == "5":
            save_bookings(passengers)
        elif choice == "6":
            passengers = load_bookings(seats)
        elif choice == "7":
            print("Exiting system. Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1 - 7.")


if __name__ == "__main__":
    main()