import tkinter as tk
from tkinter import font, colorchooser
from watermark import WatermarkApp  # Import the WatermarkApp class

class WatermarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")
        self.root.geometry("500x600")

        # Create an instance of WatermarkApp
        self.watermark_app = WatermarkApp()

        # Variables
        self.watermark_text = tk.StringVar()
        self.font_name = tk.StringVar(value="Arial")
        self.font_size = tk.IntVar(value=40)
        self.opacity = tk.DoubleVar(value=0.5)  # Opacity from 0 to 1
        self.position = tk.StringVar(value="Bottom Right")  # Default position
        self.text_color = "#FFFFFF"  # Default color (red)

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="Watermark Application", font=("Arial", 18, "bold"), bg="#f0f0f0")
        header.pack(pady=10)

        # Create a frame for the watermark text entry and font selection
        frame_text_font = tk.Frame(self.root, bg="#f0f0f0")
        frame_text_font.pack(pady=10)

        tk.Label(frame_text_font, text="Watermark Text:", bg="#f0f0f0").pack(side=tk.TOP)
        self.text_entry = tk.Entry(frame_text_font, textvariable=self.watermark_text, font=('Arial', 12), width=30)
        self.text_entry.pack(pady=2)

        tk.Label(frame_text_font, text="Font:", bg="#f0f0f0").pack(side=tk.TOP)
        self.font_dropdown = tk.OptionMenu(frame_text_font, self.font_name, *font.families())
        self.font_dropdown.pack(pady=2)

        # Create a frame for font size and opacity adjustment
        frame_size_opacity = tk.Frame(self.root, bg="#f0f0f0")
        frame_size_opacity.pack(pady=10)

        tk.Label(frame_size_opacity, text="Font Size:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.font_size_spinbox = tk.Spinbox(frame_size_opacity, from_=10, to=100, textvariable=self.font_size, width=5)
        self.font_size_spinbox.pack(side=tk.LEFT, padx=5)

        # Create a frame for opacity adjustment
        frame_opacity = tk.Frame(self.root, bg="#f0f0f0")
        frame_opacity.pack(pady=10)

        tk.Label(frame_opacity, text="Opacity (0.0 - 1.0):", bg="#f0f0f0").pack(side=tk.TOP)
        self.opacity_scale = tk.Scale(frame_opacity, from_=0.0, to=1.0, resolution=0.1,
                                      orient=tk.HORIZONTAL, variable=self.opacity, length=200)
        self.opacity_scale.pack(pady=5)

        # Color selection button
        frame_color = tk.Frame(self.root, bg="#f0f0f0")
        frame_color.pack(pady=10)


        tk.Label(frame_color, text="Text Color", bg="#f0f0f0").pack(side=tk.TOP)
        # Button to choose color
        color_frame = tk.Frame(frame_color, bg="#f0f0f0")
        color_frame.pack(pady=5)

        self.color_button = tk.Button(color_frame, text="Choose Color", command=self.choose_color, bg="#4CAF50",
                                      fg="white")
        self.color_button.pack(side=tk.LEFT)

        # Color preview label next to the button
        self.color_preview = tk.Label(color_frame, text="   ", bg=self.text_color, width=2, height=1)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Create a frame for watermark position selection
        frame_position = tk.Frame(self.root, bg="#f0f0f0")
        frame_position.pack(pady=10)

        tk.Label(frame_position, text="Watermark Position:", bg="#f0f0f0").pack(side=tk.TOP)
        position_frame = tk.Frame(frame_position, bg="#f0f0f0")
        position_frame.pack(pady=5)

        positions = ["Top Left", "Top Right", "Bottom Left", "Bottom Right"]
        for pos in positions:
            tk.Radiobutton(position_frame, text=pos, variable=self.position, value=pos, bg="#f0f0f0").pack(side=tk.LEFT)

        # Image label
        self.img_label = tk.Label(self.root, text="No image selected.", bg="#f0f0f0")
        self.img_label.pack(pady=10)

        # Create a frame for buttons
        frame_buttons = tk.Frame(self.root, bg="#f0f0f0")
        frame_buttons.pack(pady=20)

        tk.Button(frame_buttons, text="Select Image", command=self.select_image, bg="#4CAF50", fg="white",
                  font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Add Watermark", command=self.add_watermark, bg="#2196F3", fg="white",
                  font=('Arial', 12)).pack(side=tk.LEFT, padx=5)

    def choose_color(self):
        # Open a color chooser dialog and update the text color variable
        color_code = colorchooser.askcolor(title="Choose Text Color")
        if color_code[1]:  # Check if a color was selected
            self.text_color = color_code[1]
            self.color_preview.config(bg=self.text_color) # Get the hex code for the selected color

    def select_image(self):
        # Call the logic from WatermarkApp
        image_name = self.watermark_app.open_image()
        if image_name:
            self.img_label.config(text="Selected Image: " + image_name)
        else:
            self.img_label.config(text="No image selected.")

    def add_watermark(self):
        # Pass the watermark text and other settings to the WatermarkApp logic
        text = self.watermark_text.get()
        font_name = self.font_name.get()
        font_size = self.font_size.get()
        opacity = self.opacity.get()
        position = self.position.get()
        print(f"Font Size: {font_size}")  # Debugging: print the font size
        print(f"Font Name: {font_name}")
        print(f"Text: {text}")
        print(f"Text Color: {self.text_color}")  # Debugging: print the text color

        # Update the WatermarkApp with additional parameters, including text color
        self.watermark_app.add_watermark(text, font_name, font_size, opacity, position, self.text_color)
