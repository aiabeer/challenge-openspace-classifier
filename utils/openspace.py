import random
import csv
import json
from typing import List, Optional
from utils.table import Table, Seat

"""
This module defines the Openspace class, 
which represents an open space with multiple tables
and provides methods to organize seating arrangements, 
display the current state, and store the arrangement in a CSV file. 
It also includes functionality to save 
and load the open space configuration using JSON files.
"""
class Openspace:

    
    def __init__(self, number_of_tables: int = 6, capacity_per_table: int = 4):
        """
        Initialize an open space with tables.
        
        :param number_of_tables: Number of tables in the open space
        :param capacity_per_table: Capacity of each table
        """
        self.number_of_tables: int = number_of_tables
        self.capacity_per_table: int = capacity_per_table
        self.tables: List[Table] = [Table(capacity=capacity_per_table) 
                                    for _ in range(number_of_tables)]
    
    def __str__(self) -> str:
        """Return string representation of the open space."""
        total_seats = self.total_seats()
        occupied_seats = self.occupied_seats()
        return (f"OpenSpace: {self.number_of_tables} tables, "
                f"{total_seats} total seats, "
                f"{occupied_seats} occupied, "
                f"{self.total_seats_left()} seats left")
    
    def organize(self, names: List[str]) -> None:
        """
        Randomly assign people to seats in the open space.
        
        :param names: List of people to assign
        """
        # Clear all seats first
        self.clear_all_seats()
        
        # Shuffle names for random assignment
        shuffled_names = names.copy()
        random.shuffle(shuffled_names)
        
        # Assign people to seats
        name_index = 0
        for table in self.tables:
            for seat in table.seats:
                if name_index < len(shuffled_names):
                    seat.set_occupant(shuffled_names[name_index])
                    name_index += 1
    
    def organize_no_alone(self, names: List[str]) -> None:
        """
        Organize people ensuring no one sits alone at a table.
        
        :param names: List of people to assign
        """
        # Clear all seats first
        self.clear_all_seats()
        
        # Shuffle names
        shuffled_names = names.copy()
        random.shuffle(shuffled_names)
        
        # Calculate how many tables we can fill without leaving someone alone
        total_seats = self.total_seats()
        if len(shuffled_names) > total_seats:
            print(f"Warning: Too many people ({len(shuffled_names)}) for available seats ({total_seats})")
            shuffled_names = shuffled_names[:total_seats]
        
        # Try to fill tables evenly
        name_index = 0
        for table in self.tables:
            # Fill each table with at least 2 people if possible
            target_per_table = min(self.capacity_per_table, 
                                  max(2, len(shuffled_names) // self.number_of_tables))
            
            for _ in range(target_per_table):
                if name_index < len(shuffled_names):
                    table.assign_seat(shuffled_names[name_index])
                    name_index += 1
        
        # Assign remaining people
        while name_index < len(shuffled_names):
            # Find table with most free spots
            best_table = max(self.tables, key=lambda t: t.left_capacity())
            if best_table.left_capacity() > 0:
                best_table.assign_seat(shuffled_names[name_index])
                name_index += 1
            else:
                break
    
    def clear_all_seats(self) -> None:
        """Clear all seats in the open space."""
        for table in self.tables:
            for seat in table.seats:
                if not seat.free:
                    seat.remove_occupant()
    
    def display(self) -> None:
        """Display the current seating arrangement in a readable format."""
        print("\n" + "="*50)
        print("OPEN SPACE SEATING ARRANGEMENT")
        print("="*50)
        
        for i, table in enumerate(self.tables):
            occupants = table.get_occupants()
            print(f"\nTable {i+1} (Capacity: {table.capacity}, Free: {table.left_capacity()}):")
            
            if occupants:
                for j, occupant in enumerate(occupants):
                    print(f"  Seat {j+1}: {occupant}")
            else:
                print("  No occupants")
            
            # Add empty seats info
            if table.left_capacity() > 0:
                print(f"  ({table.left_capacity()} empty seat(s))")
        
        print("\n" + "="*50)
        print(f"SUMMARY: {self.occupied_seats()} people seated, {self.total_seats_left()} seats left")
        print("="*50)
    
    def store(self, filename: str) -> None:
        """
        Store the seating arrangement in a CSV file.
        
        :param filename: Name of the file to save to
        """
        # Ensure filename has .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Table Number', 'Seat Number', 'Occupant', 'Status'])
                # Write data
                for i, table in enumerate(self.tables):
                    for j, seat in enumerate(table.seats):
                        status = 'Empty' if seat.free else 'Occupied'
                        occupant = seat.occupant if not seat.free else ''
                        writer.writerow([i+1, j+1, occupant, status])
            print(f"\nSeating arrangement saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def total_seats(self) -> int:
        """
        Calculate total number of seats in the open space.
        
        :return: Total number of seats
        """
        return sum(table.capacity for table in self.tables)
    
    def total_seats_left(self) -> int:
        """
        Calculate total number of free seats.
        
        :return: Number of free seats
        """
        return sum(table.left_capacity() for table in self.tables)
    
    def occupied_seats(self) -> int:
        """
        Calculate number of occupied seats.
        
        :return: Number of occupied seats
        """
        return self.total_seats() - self.total_seats_left()
    
    def add_person(self, name: str) -> bool:
        """
        Add a new person to the open space if there's space.
        
        :param name: Name of the person to add
        :return: True if added successfully, False if no space
        """
        for table in self.tables:
            if table.has_free_spot():
                table.assign_seat(name)
                print(f"Added {name} to the open space")
                return True
        print(f"Cannot add {name}: No free seats available")
        return False
    
    def add_table(self) -> None:
        """Add a new table to the open space."""
        new_table = Table(capacity=self.capacity_per_table)
        self.tables.append(new_table)
        self.number_of_tables += 1
        print(f"Added new table. Total tables now: {self.number_of_tables}")
    
    def save_config(self, filename: str = "config.json") -> None:
        """
        Save the current open space configuration to a JSON file.
        
        :param filename: Name of the config file
        """
        config = {
            'number_of_tables': self.number_of_tables,
            'capacity_per_table': self.capacity_per_table
        }
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"Configuration saved to {filename}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    @classmethod
    def load_config(cls, filename: str = "config.json"):
        """
        Load open space configuration from a JSON file.
        
        :param filename: Name of the config file
        :return: Openspace instance with loaded configuration
        """
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            return cls(
                number_of_tables=config.get('number_of_tables', 6),
                capacity_per_table=config.get('capacity_per_table', 4)
            )
        except FileNotFoundError:
            print(f"Config file {filename} not found. Using default configuration.")
            return cls()
        except Exception as e:
            print(f"Error loading config: {e}")
            return cls()