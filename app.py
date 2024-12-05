import tkinter as tk
from plyer import notification
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import sys

def send_notification():
    title = "Notification Issue"
    message = "This is a template description and will usually be sent when there is something issue with notification settings"

    notification.notify(
        title=title,
        message=message,
        app_name="Notification App",
        timeout=10
    )

def minimize_to_tray():
    root.withdraw()
    threading.Thread(target=create_tray_icon, daemon=True).start()

def reopen_window():
    if not root.winfo_viewable():
        root.deiconify()
    tray_icon.stop()

def quit_app():
    tray_icon.stop()
    root.destroy()
    sys.exit()

def create_tray_icon():
    global tray_icon
    image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill=(0, 128, 255))
    
    menu = Menu(
        MenuItem("Open App", reopen_window),
        MenuItem("Send Notification", send_notification),
        MenuItem("Quit App", quit_app),
    )
    
    tray_icon = Icon("Notification App", image, "Notification App", menu)
    tray_icon.run()



root = tk.Tk()
root.title("Windows Notification Sender")

tk.Label(root, text="Notification Title:").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=10)


tk.Label(root, text="Notification Message:").grid(row=1, column=0, padx=10, pady=10)
message_entry = tk.Entry(root, width=40)
message_entry.grid(row=1, column=1, padx=10, pady=10)


send_button = tk.Button(root, text="Send Notification", command=send_notification)
send_button.grid(row=2, column=0, columnspan=2, pady=20)


root.protocol("WM_DELETE_WINDOW", minimize_to_tray)
root.mainloop()
