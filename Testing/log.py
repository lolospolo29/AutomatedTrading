import sys
import tkinter as tk
from tkinter import scrolledtext


class ConsolePopup:
    def __init__(self):
        # Create the root window for the popup
        self.root = tk.Tk()
        self.root.title("Console Output")

        # Set the size of the popup window
        self.root.geometry("500x300")

        # Create a scrolled text widget to display the console output
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 10))
        self.text_area.pack(expand=True, fill="both")

        # Redirect sys.stdout to this popup window
        sys.stdout = self

    def write(self, message):
        # Insert message in the text area
        self.text_area.insert(tk.END, message)

        # Scroll to the end of the text area
        self.text_area.see(tk.END)

    def flush(self):
        # This method is required for file-like object compatibility
        pass

    def start(self):
        # Run the tkinter main loop
        self.root.mainloop()


# Create and start the console popup window
console_popup = ConsolePopup()

# Example of usage
print("This will appear in the popup window instead of the console.")
print("You can continue to print messages here.")
console_popup.start()