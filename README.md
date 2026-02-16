# OpenSpace Organizer


## 🏢 Description

Your company moved to a new office. Its an openspace with 6 tables of 4 seats. As many of you are new colleagues, you come up with the idea of changing seats everyday and get to know each other better by working side by side with your new colleagues. 

This script runs everyday to re-assign everybody to a new seat.

[![monkey-in-office](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDlsMHU4YnpnbGIyYzlyNGM2NDUyZ3B0MHZnMHZlMzV5cGt5bTlwbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RETg1tippXtNm/giphy.gif)](https://giphy.com/gifs/RETg1tippXtNm)

## ✨ Features
### Must-have Features
✅ Load colleagues from Excel/CSV file
✅ Randomly assign people to tables (6 tables of 4 seats by default)
✅ Display seating arrangement
✅ Save seating to CSV file
✅ Handle overflow when too many people

###
✅ Interactive menu system
✅ Configurable room setup via JSON file
✅ Add new people dynamically
✅ Add new tables when room is full
✅ "No alone people" algorithm
✅ Statistics display (seats, people, available spots)
✅ Clear and formatted output


## 📦 Repo structure

```
.
├── utils/
│   ├── openspace.py      # Openspace class with main logic
│   ├── table.py          # Table and Seat classes
│   └── file_utils.py     # File handling utilities
├── main.py               # Main program, interactive menu
├── config.json           # Configuration file for room setup
├── new_colleagues.csv    # Sample input file with colleague names
├── output.csv            # Generated seating arrangement
└── README.md
```

## 🗺️ Class Diagram
```
┌────────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│    Openspace       │──────▶│      Table      │──────▶│      Seat        │
├────────────────────┤       ├─────────────────┤       ├──────────────────┤
│ tables             │       │ capacity        │       │ free (boolean)   │
│ number_of_tables   │       │ seats (list)    │       │ occupant (str)   │
│ capacity_per_table │       │                 │       │                  │
├────────────────────┤       ├─────────────────┤       ├──────────────────┤
│ organize()         │       │ has_free_spot() │       │ set_occupant()   │
│ organize_no_alone()│       │ assign_seat()   │       │ remove_occupant()│
│ display()          │       │ left_capacity() │       └──────────────────┘
│ store()            │       │ get_occupants() │
│ add_person()       │       └─────────────────┘
│ add_table()        │
│ total_seats()      │
│ occupied_seats()   │
│ save_config()      │
│ load_config()      │
└────────────────────┘
```

## 🛎️ Usage

### Basic Usage

1. Clone the repository to your local machine.
```
git clone https://github.com/aiabeer/challenge-openspace-classifier.git
cd challenge-openspace-classifier

```

2. Prepare a CSV file with colleague names (one name per line):
```
John Doe
Jane Smith
Bob Johnson
Alice Brown
...
```

3. Run the script:
```
python main.py
```

## Interactive Menu
When you run the program, you'll be greeted with an interactive menu:

```
==================================================
OPEN SPACE ORGANIZER
==================================================
1. Load colleagues from CSV file
2. Configure open space
3. Organize seating (random)
4. Organize seating (no alone people)
5. Display current seating
6. Save seating to file
7. Add a new person
8. Add a new table
9. Show statistics
10. Save/Load configuration
0. Exit
==================================================
Enter your choice:
```
## Configuration File
You can customize the room setup by creating a *config.json* file:
```
{
    "number_of_tables": 8,
    "capacity_per_table": 4
}
```
## 📊 Sample Output

```
==================================================
OPEN SPACE SEATING ARRANGEMENT
==================================================

Table 1 (Capacity: 4, Free: 1):
  Seat 1: John Doe
  Seat 2: Jane Smith
  Seat 3: Bob Johnson
  (1 empty seat(s))

Table 2 (Capacity: 4, Free: 0):
  Seat 1: Alice Brown
  Seat 2: Charlie Davis
  Seat 3: Eva Green
  Seat 4: Frank White

...

==================================================
SUMMARY: 18 people seated, 6 seats left
==================================================
```
## 🚀 Future Improvements

1. Add GUI interface

2. Implement preference-based seating (wishlists/blacklists)

3. Create web interface with HTML/JavaScript

4. Add email notifications with seating assignments

5. Historical tracking of seating arrangements


## ⏱️ Timeline
This project took two days for completion as part of a consolidation challenge.

## 📌 Personal Situation
This project was done as part of the AI Bootcamp at BeCode.org. It demonstrates object-oriented programming principles in Python, file handling, and creating interactive command-line applications.

🔗 **Connect with me on [LinkedIn](https://www.linkedin.com/in/abeer-shalizi-890270379/)**


[![monkey-and-laptop](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2ZjenJpejdmbnlwNjhkNWkyZnA3ODd0Y2g3bmluYWs1YzFrbzQwaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l41lQpaXZo7GGWD0k/giphy.gif)](https://giphy.com/gifs/mashable-l41lQpaXZo7GGWD0k)