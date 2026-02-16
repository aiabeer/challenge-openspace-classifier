# utils/table.py
from typing import Optional

class Seat:
    """
    Represents a single seat in a table.
    """
    
    def __init__(self):
        """Initialize a seat as free with no occupant."""
        self.free: bool = True
        self.occupant: str = ""
    
    def __str__(self) -> str:
        """Return string representation of the seat."""
        return f"Seat: {'Free' if self.free else f'Occupied by {self.occupant}'}"
    
    def set_occupant(self, name: str) -> bool:
        """
        Assign a person to the seat if it's free.
        
        :param name: Name of the person to assign
        :return: True if assignment was successful, False otherwise
        """
        if self.free:
            self.occupant = name
            self.free = False
            return True
        return False
    
    def remove_occupant(self) -> str:
        """
        Remove the occupant from the seat.
        
        :return: Name of the person who was occupying the seat
        """
        occupant_name = self.occupant
        self.occupant = ""
        self.free = True
        return occupant_name


class Table:
    """
    Represents a table with multiple seats.
    """
    
    def __init__(self, capacity: int = 4):
        """
        Initialize a table with a given capacity.
        
        :param capacity: Number of seats at the table
        """
        self.capacity: int = capacity
        self.seats: list[Seat] = [Seat() for _ in range(capacity)]
    
    def __str__(self) -> str:
        """Return string representation of the table."""
        occupied = sum(1 for seat in self.seats if not seat.free)
        return f"Table ({occupied}/{self.capacity} occupied)"
    
    def has_free_spot(self) -> bool:
        """
        Check if the table has any free seats.
        
        :return: True if at least one seat is free, False otherwise
        """
        return any(seat.free for seat in self.seats)
    
    def assign_seat(self, name: str) -> bool:
        """
        Assign a person to the first available seat at the table.
        
        :param name: Name of the person to assign
        :return: True if assignment was successful, False if table is full
        """
        for seat in self.seats:
            if seat.free:
                seat.set_occupant(name)
                return True
        return False
    
    def left_capacity(self) -> int:
        """
        Calculate the number of free seats at the table.
        
        :return: Number of free seats
        """
        return sum(1 for seat in self.seats if seat.free)
    
    def get_occupants(self) -> list[str]:
        """
        Get list of all occupants at the table.
        
        :return: List of occupant names
        """
        return [seat.occupant for seat in self.seats if not seat.free]