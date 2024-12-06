import os
import customtkinter
from PIL import Image
import tkinter as tk


class CloudBackupApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.folder_list = []

        self.title("Cloud Backup by TwistyLime")
        self.geometry("700x450")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.resizable(False, False)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20)
        )
        self.settings_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "settings_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "settings_light.png")), size=(20, 20)
        )

        self.generate_navigations_section()
        self.generate_home_page()
        self.generate_configurations_page()

        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.select_frame_by_name("home")

    def generate_navigations_section(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  Cloud Backup",
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            image=self.logo_image
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Home",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.home_button_event,
            image=self.home_image
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.configurations_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Configurations",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.configurations_button_event,
            image=self.settings_image
        )
        self.configurations_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Frame 3",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_3_button_event
        )
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
    
    def generate_home_page(self):
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self.home_frame,
            text="  Cloud Backup Home",
            compound="left",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(
            self.home_frame,
            text="Auto Backup",
            command=self.switch_event,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off"
        )
        self.switch.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    def generate_configurations_page(self):
        self.configurations_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.configurations_frame.grid_columnconfigure(0, weight=1)

        self.folder_config_label = customtkinter.CTkLabel(
            self.configurations_frame,
            text="  Folder Configurations",
            compound="left",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.folder_config_label.grid(row=0, column=0, padx=20, pady=20)


        self.folder_ignore_list_label = customtkinter.CTkLabel(
            self.configurations_frame,
            text="Folders to Ignore: ",
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.folder_ignore_list_label.grid(row=1, column=0, padx=20, sticky="w")

        self.folders_ignore_list = customtkinter.CTkTextbox(
            self.configurations_frame,
            width=250,
            height=100,
            corner_radius=5,
            activate_scrollbars=False
        )
        self.folders_ignore_list.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
        self.folders_ignore_list.configure(state="disabled")

        self.folders_ignore_list.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_selected_line)

        self.folder_ignore_entry = customtkinter.CTkEntry(
            self.configurations_frame,
            placeholder_text="Enter folder names to ignore...",
            width=250,
            corner_radius=5
        )
        self.folder_ignore_entry.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="w")
        self.folder_ignore_entry.bind("<Return>", self.add_to_ignore_list)

        self.ignore_list_add_button = customtkinter.CTkButton(
            self.configurations_frame,
            text="Add",
            command=self.add_to_ignore_list,
            corner_radius=5
        )
        self.ignore_list_add_button.grid(row=3, column=1, padx=(0, 75), pady=(20, 0), sticky="w")
    
    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.configurations_button.configure(fg_color=("gray75", "gray25") if name == "configurations" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "configurations":
            self.configurations_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.configurations_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def configurations_button_event(self):
        self.select_frame_by_name("configurations")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def add_to_ignore_list(self, event=None):
        folder = self.folder_ignore_entry.get()
        self.folder_ignore_entry.delete(0, "end")
        if not folder.strip():
            return
        existing_folders = self.folders_ignore_list.get("1.0", "end").splitlines()
        if folder in existing_folders:
            return
        self.folders_ignore_list.configure(state="normal")
        self.folders_ignore_list.insert("0.0",f"{folder.strip()}\n")
        self.folders_ignore_list.configure(state="disabled")
        self.folder_list.append(folder.strip())
    
    def show_context_menu(self, event):
        selected_text = self.folders_ignore_list.get("sel.first", "sel.last") if self.folders_ignore_list.tag_ranges("sel") else ""
        if selected_text.strip():
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected_line(self):
        selected_text = self.folders_ignore_list.get("sel.first", "sel.last") if self.folders_ignore_list.tag_ranges("sel") else ""
        selected_text = selected_text.strip()
        if selected_text:
            if selected_text in self.folder_list:
                self.folder_list.remove(selected_text)

                self.folders_ignore_list.configure(state="normal")
                self.folders_ignore_list.delete("1.0", "end")

                for folder in self.folder_list:
                    self.folders_ignore_list.insert("0.0", f"{folder}\n")
                self.folders_ignore_list.configure(state="disabled")

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())
    


if __name__ == "__main__":
    app = CloudBackupApp()
    app.mainloop()
