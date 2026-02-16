# utils/file_utils.py
import csv
from typing import List, Optional
import os

def read_names_from_csv(filename: str) -> List[str]:
    """
    Read names from a CSV file.
    
    :param filename: Path to the CSV file
    :return: List of names
    """
    names_list = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():  # Check if row exists and first element is not empty
                    names_list.append(row[0].strip())
        print(f"Loaded {len(names_list)} names from {filename}")
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return names_list

def write_names_to_csv(filename: str, names: List[str]) -> None:
    """
    Write a list of names to a CSV file.
    
    :param filename: Path to the CSV file
    :param names: List of names to write
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name in names:
                writer.writerow([name])
        print(f"Saved {len(names)} names to {filename}")
    except Exception as e:
        print(f"Error writing file: {e}")