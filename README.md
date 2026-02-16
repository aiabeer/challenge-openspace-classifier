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

## 🛎️ Usage

1. Clone the repository to your local machine.

2 .To run the script, you can execute the `main.py` file from your command line:

    ```
    python main.py
    ```

3. The script reads your input file, and organizes your colleagues to random seat assignments. The resulting seating plan is displayed in your console and also saved to an "output.csv" file in your root directory. 

```python
input_filepath = "new_colleagues.csv"
output_filename = "output.csv"

# Creates a list that contains all the colleagues names
names = utils.read_names_from_csv(input_filepath)

# create an OpenSpace()
open_space = OpenSpace()

# assign a colleague randomly to a table
open_space.organize(names)

# save the seat assigments to a new file
open_space.store(output_filename)

# display assignments in the terminal
open_space.display()
```
## ⏱️ Timeline

This project took two days for completion.

## 📌 Personal Situation
This project was done as part of the AI Boocamp at BeCode.org. 

Connect with me on [LinkedIn](https://www.linkedin.com/in/vriveraq/).

