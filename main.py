# main.py

import tkinter as tk
from watermark_gui import WatermarkGUI  # Import the GUI class

# Initialize the Tkinter window

root = tk.Tk()

    # Create an instance of WatermarkGUI, passing the root window
app = WatermarkGUI(root)

    # Run the Tkinter main loop
root.mainloop()
