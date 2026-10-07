from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Global variables to store the uploaded image path and loaded image object
current_image_path = None
img_tk = None


def upload_image():
    global current_image_path, img_tk

    # Bring the main window to the front
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

    # Open the file dialog for image selection
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )

    if file_path:
        current_image_path = file_path
        try:
            img = Image.open(current_image_path)
            img.thumbnail((480, 300))

            img_tk = ImageTk.PhotoImage(img)

            preview_label.config(image=img_tk, text="")
            preview_label.image = img_tk  # Prevent garbage collection
        except Exception as e:
            print("Error loading image:", e)
            preview_label.config(text="Error loading image!", image="")


def save_watermarked_image():
    if not current_image_path:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    watermark_text = watermark_entry.get().strip()
    if not watermark_text:
        messagebox.showerror("Error", "Please enter watermark text!")
        return

    try:
        # Open original high-resolution image
        original_image = Image.open(current_image_path).convert("RGBA")

        # Create a transparent overlay for the watermark
        txt_overlay = Image.new("RGBA", original_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_overlay)

        # Calculate dynamic font size based on image dimensions
        font_size = int(original_image.width / 20)
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Get text bounding box coordinates
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position the watermark at the bottom-right corner with padding
        margin = 20
        x = original_image.width - text_width - margin
        y = original_image.height - text_height - margin

        # Draw the text with black color and slight transparency (RGBA)
        draw.text((x, y), watermark_text, font=font, fill=(0, 0, 0, 180))

        # Combine the original image with the watermark overlay
        watermarked = Image.alpha_composite(original_image, txt_overlay)
        watermarked = watermarked.convert("RGB")  # Convert back to RGB for saving as JPEG/PNG

        # Ask user where to save the file
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
        )

        if save_path:
            watermarked.save(save_path)
            messagebox.showinfo("Success", f"Watermarked image saved successfully at:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")


# 1. Main Window Setup
root = Tk()
root.title("Image Watermarking Desktop App")
root.geometry("800x600")
root.config(padx=20, pady=20, bg="#f4f4f4")

# App Title
title_label = Label(
    root,
    text="Python Image Watermark Studio",
    font=("Arial", 18, "bold"),
    bg="#f4f4f4",
    fg="#333333"
)
title_label.pack(pady=10)

# 2. Image Preview Area (Frame + Label)
canvas_frame = Frame(root, width=500, height=320, bg="white", relief=SOLID, bd=1)
canvas_frame.pack(pady=10)
canvas_frame.pack_propagate(False)

preview_label = Label(
    canvas_frame,
    text="No Image Uploaded Yet\n(Preview will appear here)",
    font=("Arial", 11),
    bg="white",
    fg="#888888"
)
preview_label.pack(expand=True)

# 3. Controls Layout (Buttons & Inputs Frame)
control_frame = Frame(root, bg="#f4f4f4")
control_frame.pack(pady=20)

# Upload Image Button (removed custom bg/fg for macOS compatibility)
upload_btn = Button(
    control_frame,
    text="📁 Upload Image",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5,
    command=upload_image
)
upload_btn.grid(row=0, column=0, padx=10)

# Watermark Text Input Label & Field
watermark_label = Label(
    control_frame,
    text="Watermark Text:",
    font=("Arial", 11, "bold"),
    bg="#f4f4f4",
    fg="#333333"
)
watermark_label.grid(row=0, column=1, padx=5)

watermark_entry = Entry(control_frame, font=("Arial", 11), width=18)
watermark_entry.grid(row=0, column=2, padx=5)

# Save Watermarked Image Button (removed custom bg/fg for macOS compatibility)
save_btn = Button(
    control_frame,
    text="💾 Save Watermarked Image",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5,
    command=save_watermarked_image
)
save_btn.grid(row=0, column=3, padx=10)

# Main Application Loop
root.mainloop()