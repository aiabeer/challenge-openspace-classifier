import streamlit as st
import pandas as pd
import json
import random
from io import StringIO
from typing import List, Optional, Dict, Any

# ---------------------- Core Classes ----------------------
class Table:
    """Represents a table with a fixed number of seats."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.seats: List[Optional[str]] = [None] * capacity

    def __repr__(self):
        return f"Table(capacity={self.capacity}, seats={self.seats})"


class Openspace:
    """Manages a collection of tables and seating assignments."""
    def __init__(self, num_tables: int = 6, capacity_per_table: int = 4):
        self.tables: List[Table] = [Table(capacity_per_table) for _ in range(num_tables)]
        self.capacity_per_table = capacity_per_table
        self.number_of_tables = num_tables

    def total_seats(self) -> int:
        return sum(t.capacity for t in self.tables)

    def occupied_seats(self) -> int:
        return sum(1 for t in self.tables for s in t.seats if s is not None)

    def total_seats_left(self) -> int:
        return self.total_seats() - self.occupied_seats()

    def organize(self, names: List[str]) -> None:
        """Randomly assign people to empty seats."""
        # Flatten all seats and collect empty ones
        empty_seats = []
        for i, table in enumerate(self.tables):
            for j, seat in enumerate(table.seats):
                if seat is None:
                    empty_seats.append((i, j))

        # Shuffle names and assign to empty seats
        shuffled_names = names.copy()
        random.shuffle(shuffled_names)
        for (i, j), name in zip(empty_seats, shuffled_names):
            self.tables[i].seats[j] = name

        # Clear any remaining seats (not used)
        for (i, j) in empty_seats[len(shuffled_names):]:
            self.tables[i].seats[j] = None

    def organize_no_alone(self, names: List[str]) -> None:
        """Randomly assign people, then try to eliminate tables with exactly one person."""
        self.organize(names)  # start with random assignment

        # Move people from tables with exactly 1 person to tables with ≥2 and an empty seat
        changed = True
        while changed:
            changed = False
            alone_table_idx = None
            alone_seat_idx = None
            target_table_idx = None
            target_seat_idx = None

            # Find a table with exactly 1 person and a table with ≥2 people and an empty seat
            for i, table in enumerate(self.tables):
                occupied = [j for j, s in enumerate(table.seats) if s is not None]
                if len(occupied) == 1 and alone_table_idx is None:
                    alone_table_idx = i
                    alone_seat_idx = occupied[0]
                elif len(occupied) >= 2:
                    empty = [j for j, s in enumerate(table.seats) if s is None]
                    if empty:
                        target_table_idx = i
                        target_seat_idx = empty[0]

            if alone_table_idx is not None and target_table_idx is not None:
                # Move the person from the alone table to the target table
                person = self.tables[alone_table_idx].seats[alone_seat_idx]
                self.tables[alone_table_idx].seats[alone_seat_idx] = None
                self.tables[target_table_idx].seats[target_seat_idx] = person
                changed = True

    def add_person(self, name: str) -> bool:
        """Add a person to the first empty seat. Returns True if successful."""
        for table in self.tables:
            for i, seat in enumerate(table.seats):
                if seat is None:
                    table.seats[i] = name
                    return True
        return False

    def add_table(self, capacity: Optional[int] = None) -> None:
        """Add a new table with given capacity (defaults to current capacity)."""
        cap = capacity if capacity is not None else self.capacity_per_table
        self.tables.append(Table(cap))
        self.number_of_tables += 1

    def store(self, filename: str) -> None:
        """Save seating arrangement to a CSV file."""
        data = []
        for i, table in enumerate(self.tables):
            for j, seat in enumerate(table.seats):
                data.append({
                    "table_number": i + 1,
                    "seat_number": j + 1,
                    "occupant": seat if seat is not None else ""
                })
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def save_config(self, filename: str = "config.json") -> None:
        """Save configuration (number of tables and capacity per table) to a JSON file."""
        config = {
            "num_tables": self.number_of_tables,
            "capacity_per_table": self.capacity_per_table
        }
        with open(filename, "w") as f:
            json.dump(config, f)

    @classmethod
    def load_config(cls, filename: str = "config.json") -> "Openspace":
        """Load configuration from a JSON file and return a new Openspace instance."""
        with open(filename, "r") as f:
            config = json.load(f)
        return cls(config["num_tables"], config["capacity_per_table"])

    def assign_manual(self, table_idx: int, seat_idx: int, person: Optional[str]) -> None:
        """Manually assign a person to a specific seat. If person is None, clear the seat."""
        # Remove the person from any other seat if they are already seated
        if person is not None:
            for ti, table in enumerate(self.tables):
                for si, seat in enumerate(table.seats):
                    if seat == person and (ti != table_idx or si != seat_idx):
                        table.seats[si] = None

        # Assign to the target seat
        self.tables[table_idx].seats[seat_idx] = person


# ---------------------- Streamlit App ----------------------
st.set_page_config(page_title="Open Space Organizer", layout="wide")
st.title("🪑 Open Space Organizer")

# Initialize session state
if "openspace" not in st.session_state:
    st.session_state.openspace = Openspace()
if "names" not in st.session_state:
    st.session_state.names = []
if "csv_file" not in st.session_state:
    st.session_state.csv_file = None

# Helper function to update display after changes
def refresh():
    """Trigger a rerun to refresh the UI."""
    st.rerun()


# ---------------------- Sidebar: Configuration & Actions ----------------------
with st.sidebar:
    st.header("📂 Load Colleagues")
    uploaded_file = st.file_uploader("Upload CSV (with a 'name' column)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "name" in df.columns:
            st.session_state.names = df["name"].tolist()
            st.success(f"Loaded {len(st.session_state.names)} names.")
        else:
            st.error("CSV must contain a 'name' column.")

    # Manual name input
    new_name = st.text_input("Or add a new person manually")
    if st.button("➕ Add Person") and new_name.strip():
        st.session_state.names.append(new_name.strip())
        # Try to automatically seat them
        if not st.session_state.openspace.add_person(new_name.strip()):
            st.warning("No empty seat available – person added to list but not seated.")
        refresh()

    st.divider()

    st.header("⚙️ Open Space Configuration")
    num_tables = st.number_input("Number of tables", min_value=1, value=st.session_state.openspace.number_of_tables, step=1)
    capacity = st.number_input("Capacity per table", min_value=1, value=st.session_state.openspace.capacity_per_table, step=1)
    if st.button("Apply Configuration"):
        # Create new Openspace with new config
        st.session_state.openspace = Openspace(num_tables, capacity)
        st.success("Configuration applied. Seating reset.")
        refresh()

    st.divider()

    st.header("🎲 Seating Algorithms")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Random Assign"):
            if st.session_state.names:
                st.session_state.openspace.organize(st.session_state.names)
                st.success("Random assignment done.")
                refresh()
            else:
                st.warning("No colleagues loaded.")
    with col2:
        if st.button("No Alone People"):
            if st.session_state.names:
                st.session_state.openspace.organize_no_alone(st.session_state.names)
                st.success("Seating adjusted to avoid alone people.")
                refresh()
            else:
                st.warning("No colleagues loaded.")

    st.divider()

    st.header("➕ Add a Table")
    if st.button("Add Table (capacity = current capacity)"):
        st.session_state.openspace.add_table()
        st.success("New table added.")
        refresh()

    st.divider()

    st.header("📊 Statistics")
    total_seats = st.session_state.openspace.total_seats()
    occupied = st.session_state.openspace.occupied_seats()
    st.metric("People loaded", len(st.session_state.names))
    st.metric("Total seats", total_seats)
    st.metric("Seated", occupied)
    st.metric("Empty seats", total_seats - occupied)
    if len(st.session_state.names) > total_seats:
        st.error(f"⚠️ Warning: {len(st.session_state.names) - total_seats} people cannot be seated!")
    elif len(st.session_state.names) < total_seats:
        st.info(f"ℹ️ {total_seats - len(st.session_state.names)} empty seats available")

    st.divider()

    st.header("💾 Save & Load")
    if st.button("Save Seating to CSV"):
        if st.session_state.openspace.occupied_seats() > 0:
            # Save to a temporary file and provide download button
            csv_buffer = StringIO()
            data = []
            for i, table in enumerate(st.session_state.openspace.tables):
                for j, seat in enumerate(table.seats):
                    data.append({
                        "table_number": i + 1,
                        "seat_number": j + 1,
                        "occupant": seat if seat is not None else ""
                    })
            pd.DataFrame(data).to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download seating.csv",
                data=csv_buffer.getvalue(),
                file_name="seating.csv",
                mime="text/csv"
            )
        else:
            st.warning("No seating arrangement to save.")

    # Save/Load configuration
    config_save = st.button("Save Current Configuration")
    if config_save:
        # Provide download for config.json
        config = {
            "num_tables": st.session_state.openspace.number_of_tables,
            "capacity_per_table": st.session_state.openspace.capacity_per_table
        }
        st.download_button(
            label="Download config.json",
            data=json.dumps(config, indent=2),
            file_name="config.json",
            mime="application/json"
        )

    config_file = st.file_uploader("Load configuration from JSON", type=["json"], key="config_upload")
    if config_file is not None:
        config = json.load(config_file)
        st.session_state.openspace = Openspace(config["num_tables"], config["capacity_per_table"])
        st.success("Configuration loaded. Seating reset.")
        refresh()


# ---------------------- Main Area: Seating Display ----------------------
st.header("🪑 Current Seating Arrangement")

# Show each table as a column (or expander if many tables)
num_tables = len(st.session_state.openspace.tables)
cols = st.columns(min(num_tables, 3))  # up to 3 tables per row
for idx, table in enumerate(st.session_state.openspace.tables):
    col = cols[idx % 3]
    with col:
        with st.expander(f"Table {idx+1} (capacity {table.capacity})", expanded=True):
            for seat_idx, occupant in enumerate(table.seats):
                # Prepare options for dropdown
                options = ["(empty)"] + st.session_state.names
                current = occupant if occupant is not None else "(empty)"
                selected = st.selectbox(
                    f"Seat {seat_idx+1}",
                    options,
                    index=options.index(current) if current in options else 0,
                    key=f"table_{idx}_seat_{seat_idx}"
                )
                # If selection changed, update the seating
                if selected != current:
                    new_occupant = None if selected == "(empty)" else selected
                    st.session_state.openspace.assign_manual(idx, seat_idx, new_occupant)
                    refresh()

st.markdown("---")
st.caption("Tip: Use the dropdowns to manually assign people to seats. Each person can only sit in one seat.")