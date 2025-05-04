import tkinter as tk
from tkinter import filedialog

def browse_file():
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All files", "*.*"), ("Text files", "*.txt")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    browse_file()