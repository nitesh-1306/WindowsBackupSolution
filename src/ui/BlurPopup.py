import time
import tkinter as tk
from tkinter import Toplevel
import customtkinter as ctk
from PIL import ImageGrab, ImageTk, ImageFilter

# Function to blur the main window
def blur_main_window(window):
    window.update_idletasks()
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()
    image = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    blurred_image = image.filter(ImageFilter.GaussianBlur(10))

    # Convert the image to a PhotoImage
    photo = ImageTk.PhotoImage(blurred_image)

    # Display the blurred image
    global blur_label  # Use a global variable to keep reference
    blur_label = tk.Label(window, image=photo)
    blur_label.image = photo
    blur_label.place(x=0, y=0, relwidth=1, relheight=1)

    show_popup()

# Function to display the popup window
def show_popup():
    popup = Toplevel(main)
    popup.title("Popup")
    popup.geometry("300x150")
    popup.configure(bg="white")

    # Center the popup
    main_x = main.winfo_rootx()
    main_y = main.winfo_rooty()
    main_width = main.winfo_width()
    main_height = main.winfo_height()
    popup_width = 300
    popup_height = 150

    popup_x = main_x + (main_width - popup_width) // 2
    popup_y = main_y + (main_height - popup_height) // 2
    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

    # Add content to the popup
    label = ctk.CTkLabel(popup, text="This is a popup window.")
    label.pack(pady=20)
    close_button = ctk.CTkButton(popup, text="Close", command=lambda: close_popup(popup))
    close_button.pack(pady=10)

    popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

    # Block interactions with the main window
    popup.transient(main)
    popup.grab_set()

# Function to close the popup and remove the blur
def close_popup(popup):
    popup.destroy()
    time.sleep(0.15)
    blur_label.destroy()  # Remove the blur effect




main = ctk.CTk()
main.title("Blur and Popup Example")
main.geometry("500x300")

button = ctk.CTkButton(main, text="Show Popup", command=blur_main_window)
button.pack(pady=20)

main.mainloop()
