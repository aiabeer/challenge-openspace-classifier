# main.py
import sys
import os
from typing import List, Optional

from utils.openspace import Openspace
from utils.file_utils import read_names_from_csv, write_names_to_csv

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("OPEN SPACE ORGANIZER")
    print("="*50)
    print("1. Load colleagues from CSV file")
    print("2. Configure open space")
    print("3. Organize seating (random)")
    print("4. Organize seating (no alone people)")
    print("5. Display current seating")
    print("6. Save seating to file")
    print("7. Add a new person")
    print("8. Add a new table")
    print("9. Show statistics")
    print("10. Save/Load configuration")
    print("0. Exit")
    print("="*50)

def configure_openspace() -> Openspace:
    """Configure the open space interactively."""
    print("\n--- Open Space Configuration ---")
    try:
        num_tables = int(input("Number of tables (default 6): ") or "6")
        capacity = int(input("Capacity per table (default 4): ") or "4")
        return Openspace(num_tables, capacity)
    except ValueError:
        print("Invalid input. Using default configuration.")
        return Openspace()

def get_positive_input(prompt: str) -> int:
    """
    Get positive integer input from user.
    
    :param prompt: Input prompt to display
    :return: Positive integer
    """
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def show_statistics(openspace: Openspace, names: List[str]):
    """Display statistics about the open space."""
    print("\n--- Open Space Statistics ---")
    print(f"Number of tables: {openspace.number_of_tables}")
    print(f"Capacity per table: {openspace.capacity_per_table}")
    print(f"Total seats: {openspace.total_seats()}")
    print(f"People in room: {len(names)}")
    print(f"People seated: {openspace.occupied_seats()}")
    print(f"Seats left: {openspace.total_seats_left()}")
    
    if len(names) > openspace.total_seats():
        print(f"⚠️  Warning: {len(names) - openspace.total_seats()} people cannot be seated!")
    elif len(names) < openspace.total_seats():
        print(f"ℹ️  {openspace.total_seats() - len(names)} empty seats available")

def main():
    """Main program function."""
    # Initialize variables
    openspace = Openspace()
    names: List[str] = []
    current_file: Optional[str] = None
    
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            # Load colleagues from CSV
            filename = input("Enter CSV filename (default: colleagues.csv): ") or "colleagues.csv"
            if not os.path.exists(filename):
                print(f"File {filename} not found in current directory.")
                filename = input("Enter full path to CSV file: ")
            
            names = read_names_from_csv(filename)
            if names:
                current_file = filename
                print(f"\nLoaded {len(names)} colleagues:")
                for i, name in enumerate(names[:5], 1):
                    print(f"  {i}. {name}")
                if len(names) > 5:
                    print(f"  ... and {len(names) - 5} more")
        
        elif choice == '2':
            # Configure open space
            openspace = configure_openspace()
            print("\nOpen space configured successfully!")
            print(openspace)
        
        elif choice == '3':
            # Organize seating (random)
            if not names:
                print("Please load colleagues first (option 1)")
                continue
            
            openspace.organize(names)
            print("\nSeating organized randomly!")
            openspace.display()
        
        elif choice == '4':
            # Organize seating (no alone people)
            if not names:
                print("Please load colleagues first (option 1)")
                continue
            
            openspace.organize_no_alone(names)
            print("\nSeating organized with no alone people!")
            openspace.display()
        
        elif choice == '5':
            # Display current seating
            openspace.display()
        
        elif choice == '6':
            # Save seating to file
            if openspace.occupied_seats() == 0:
                print("No seating arrangement to save. Organize seating first.")
                continue
            
            filename = input("Enter output filename (default: seating.csv): ") or "seating.csv"
            openspace.store(filename)
        
        elif choice == '7':
            # Add a new person
            if not openspace.tables:
                print("Please configure open space first (option 2)")
                continue
            
            name = input("Enter name of new person: ").strip()
            if name:
                if openspace.add_person(name):
                    names.append(name)
            else:
                print("Invalid name")
        
        elif choice == '8':
            # Add a new table
            openspace.add_table()
            print(openspace)
        
        elif choice == '9':
            # Show statistics
            show_statistics(openspace, names)
        
        elif choice == '10':
            # Save/Load configuration
            print("\n1. Save current configuration")
            print("2. Load configuration")
            subchoice = input("Choose: ").strip()
            
            if subchoice == '1':
                openspace.save_config()
            elif subchoice == '2':
                openspace = Openspace.load_config()
                print("Configuration loaded!")
                print(openspace)
        
        elif choice == '0':
            # Exit
            print("\nThank you for using Open Space Organizer!")
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    main()