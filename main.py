import tkinter as tk
from tkinter import messagebox
import csv
import os

# File to store voter IDs and their votes
VOTES_FILE = "votes.csv"

# Initialize the votes file if it doesn't exist
def initialize_votes_file():
    if not os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["VoterID", "Option"])

# Function to check the current vote winner
def get_vote_winner():
    votes = {"Option 1": 0, "Option 2": 0}
    try:
        with open(VOTES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                votes[row["Option"]] += 1
        if votes["Option 1"] > votes["Option 2"]:
            return "Option 1"
        elif votes["Option 1"] < votes["Option 2"]:
            return "Option 2"
        else:
            return "Undecided"
    except Exception:
        return "Undecided"

# Function to handle vote submission
def submit_vote():
    voter_id = voter_id_entry.get().strip()
    selected_option = option_var.get()

    # Validate voter ID (must be 5 digits)
    if not (voter_id.isdigit() and len(voter_id) == 5):
        result_label.config(text="ID Rejected", fg="red")
        return

    # Check if voter ID is already used
    try:
        with open(VOTES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["VoterID"] == voter_id:
                    result_label.config(text="ID Rejected", fg="red")
                    return
    except Exception:
        pass

    # Ensure an option is selected
    if selected_option not in ["Option 1", "Option 2"]:
        result_label.config(text="Please select an option", fg="red")
        return

    # Save the vote
    with open(VOTES_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([voter_id, selected_option])

    # Clear input fields and update result
    voter_id_entry.delete(0, tk.END)
    option_var.set(None)
    result_label.config(text=f"Current Winner: {get_vote_winner()}", fg="green")

# Initialize the GUI window
initialize_votes_file()
root = tk.Tk()
root.title("Voting App")
root.geometry("300x250")

# Voter ID input
voter_id_label = tk.Label(root, text="Enter Voter ID (5 digits):")
voter_id_label.pack(pady=5)
voter_id_entry = tk.Entry(root)
voter_id_entry.pack(pady=5)

# Option selection
option_label = tk.Label(root, text="Select an Option:")
option_label.pack(pady=5)
option_var = tk.StringVar(value=None)
option_1_radio = tk.Radiobutton(root, text="Option 1", variable=option_var, value="Option 1")
option_1_radio.pack()
option_2_radio = tk.Radiobutton(root, text="Option 2", variable=option_var, value="Option 2")
option_2_radio.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_vote)
submit_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Initial winner display
result_label.config(text=f"Current Winner: {get_vote_winner()}", fg="blue")

# Run the application
root.mainloop()
