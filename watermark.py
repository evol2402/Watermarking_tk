from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import platform
import os


class WatermarkApp:
    def __init__(self):
        self.image_path = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        if file_path:
            self.image_path = file_path
            return os.path.basename(file_path)
        else:
            return None

    def get_system_font_path(self, font_name):
        system = platform.system()
        if system == "Windows":
            return os.path.join("C:\\Windows\\Fonts", font_name + ".ttf")
        elif system == "Darwin":  # macOS
            return os.path.join("/Library/Fonts", font_name + ".ttf")
        elif system == "Linux":
            return os.path.join("/usr/share/fonts/truetype", font_name + ".ttf")
        return None
    def add_watermark(self, watermark_text, font_name, font_size, opacity, position, text_color):
        if self.image_path and watermark_text:
            # Open the image
            img = Image.open(self.image_path).convert("RGBA")  # Ensure RGBA mode for transparency
            width, height = img.size

            # Create a new layer for the watermark with the same size as the image
            watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_layer)

            try:
                font_path = self.get_system_font_path(font_name)
                if font_path:
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.truetype(font_name, font_size)
            except IOError:
                messagebox.showerror("Font Error", f"Font '{font_name}' not found. Falling back to default.")
                font = ImageFont.load_default()  # Fallback if font is not found
            # Calculate the size of the watermark text
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Determine position based on user selection
            if position == "Top Left":
                x, y = 10, 10
            elif position == "Top Right":
                x, y = width - text_width - 10, 10
            elif position == "Bottom Left":
                x, y = 10, height - text_height - 10
            else:  # "Bottom Right"
                x, y = width - text_width - 10, height - text_height - 10

            # Define text color and opacity
            # Convert hex color to RGB
            r, g, b = [int(text_color[i:i + 2], 16) for i in (1, 3, 5)]  # Assuming text_color is in hex format
            a = int(255 * opacity)  # Calculate alpha value based on opacity

            # Add the text to the watermark layer
            draw.text((x, y), watermark_text, font=font, fill=(r, g, b, a))

            # Combine the watermark layer with the image
            watermarked_img = Image.alpha_composite(img, watermark_layer)

            # Ask for save location and save the image
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                watermarked_img = watermarked_img.convert("RGB")  # Convert back to RGB if needed
                watermarked_img.save(save_path)
                messagebox.showinfo("Success", "Watermark added and image saved successfully!")
            else:
                messagebox.showwarning("Save Error", "No file selected for saving the watermarked image.")
        else:
            messagebox.showwarning("Input Error", "Please select an image and enter watermark text!")
