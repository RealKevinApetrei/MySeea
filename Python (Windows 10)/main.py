import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk

import os

import sqlite3
import mysql.connector

import config
import Files.help_data as help_data

"""
TODO:
1. Add more Keybinds
2. Add more help/documentation
"""

class Application(tk.Tk): # Application Class Object
    def __init__(self):
        super().__init__() # Superclass (tk.Tk)

        self.title(config.PROGRAM_NAME + " | " + config.BUILD_VERSION + " | By " + config.AUTHOR) # Window Title
        self.geometry("500x500") # Window Size (Template)
        self.resizable(0, 0) # not Resizable

        self.protocol("WM_DELETE_WINDOW", self.close)

        # Fonts
        self.hel15b = font.Font(family="Helvetica", size=15, weight="bold") # Font (Helvetica, 15, Bold)
        self.hel30b = font.Font(family="Helvetica", size=30, weight="bold") # Font (Helvetica, 30, Bold)
        self.sys20bu = font.Font(family="system", size=20, weight="bold", underline=1) # Font (system, 20, Bold, Underline)
        self.hel10 = font.Font(family="Helvetica", size=10) # Font (Helvetica, 10)
        self.hel10b = font.Font(family="Helvetica", size=10, weight="bold") # Font (Helvetica, 10, Bold)
        self.hel15bi = font.Font(family="Helvetica", size=15, weight="bold", slant="italic") # Font (Helvetica, 15, Bold, Italic)
        self.hel12bi = font.Font(family="Helvetica", size=12, weight="bold", slant="italic") # Font (Helvetica, 12, Bold, Italic)

    def __repr__(self):
        __name = self.__class__
        __type = type(self)
        __module = type.__module__
        __qualname = type.__qualname__

        return f"""\
        Class Name: {__name}
        Class Details: {config.PROGRAM_NAME}

        Build Version: {config.BUILD_VERSION}
        Author: {config.AUTHOR}

        Class Type: {__type}
        Class Module: {__module}
        Class Qualname: {__qualname}
        """

    def close(self): # If program is closed...
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()


class SearchableTreeview(ttk.Treeview): # Searchable Treeview
    def __init__(self, master, *args, **kwargs):
        ttk.Treeview.__init__(self, *args, **kwargs)

        # Fonts
        self.hel12bi = font.Font(family="Helvetica", size=12, weight="bold", slant="italic") # Font (Helvetica, 12, Bold, Italic)
        self.hel10 = font.Font(family="Helvetica", size=10) # Font (Helvetica, 10)
        self.hel10b = font.Font(family="Helvetica", size=10, weight="bold") # Font (Helvetica, 10, Bold)
        self.hel15b = font.Font(family="Helvetica", size=15, weight="bold") # Font (Helvetica, 15, Bold)

        self.master = master
        self.info_shown = False
        self.info_frame = None

        self._to_search = tk.StringVar()
        self.search_entry = tk.Entry(self, textvariable=self._to_search, bg="gray", relief="sunken", bd=3)

        self.bind("<Control-f>", self._find_action)

        self._to_search.trace_variable("w", self._search)

        self.search_entry.bind("<Return>", self._hide_entry)
        self.search_entry.bind("<Escape>", self._hide_entry)

        self.bind("<KeyRelease>", self._callback)
        self.bind("<ButtonRelease-1>", self._callback)

    def _callback(self, event): # Key Callback
        selected_item = self.master.help_treeview.item(self.master.help_treeview.focus())["text"]#
        selected_item_location = self.master.help_treeview.item(self.master.help_treeview.focus())["values"][0]

        if self.info_shown == True:
            self.info_frame.place_forget()
            self.info_shown = False

        self.info_frame = tk.Frame(self.master, bg="gray85", height=450, width=325, relief="raised", bd=3)
        self.info_frame.place(x=745, y=235, anchor="e")
        self.info_frame.propagate(0)

        # Get Info
            # Main Nodes
        try:
            if selected_item_location == "main_node": # If Main node...
                data = help_data.main_node_data[selected_item]

                # Children Nodes
            elif selected_item_location == "usage_node": # If Main > Usage node...
                data = help_data.usage_node_data[selected_item]

            elif selected_item_location == "keybinds_node": # If Main > Keybinds node...
                data = help_data.keybinds_node_data[selected_item]

                # Grandchildren Nodes
            elif selected_item_location == "general_usage_node": # If Main > Usage > General node...
                data = help_data.general_usage_node_data[selected_item]

            elif selected_item_location == "settings_keybinds_node": # If Main > Keybinds > Settings node...
                data = help_data.settings_keybinds_node_data[selected_item]

                # Not found?
            else:
                data = {"name": "Help not Found!",
                        "type": "???",
                        "description": "It looks like we can't help you with this one.\nThere has been a bug or this feature may come soon in the future!\nStay tuned!\n(Node not Found)"
                    }
        except KeyError:
            data = {"name": "Help not Found!",
                        "type": "???",
                        "description": "It looks like we can't help you with this one.\nThere has been a bug or this feature may come soon in the future!\nStay tuned!\n(KeyError)"
                    }
        except Exception as error:
            data = {"name": "Error has Occurred!",
                    "type": "???",
                    "description": "Error: {}\nPlease contact admin/developer.".format(error)}


        tk.Label(self.info_frame, text=data["name"], bg="gray90", relief="sunken", bd=2, font=self.hel12bi, width=30, anchor="w").place(x=5, y=5)
        tk.Label(self.info_frame, text=data["type"], bg="gray90", relief="sunken", bd=2, font=self.hel10b, width=30, anchor="w").place(x=5, y=40)
        tk.Message(self.info_frame, text=data["description"], bg="gray90", relief="sunken", bd=2, font=self.hel10, width=300).place(x=5, y=75)

        self.info_shown = True

    def _find_action(self, event): # When key is pressed on treeview
        self.search_entry.place(relx=1, anchor=tk.NE)

        if event.char.isalpha():
            self.search_entry.insert(tk.END, event.char)
        self.search_entry.focus_set()

    def _hide_entry(self, event): # Hide entry on treeview
        self.search_entry.delete(0, tk.END)
        self.search_entry.place_forget()
        self.focus_set()

    def _search(self, *args): # Search on treeview (1)
        pattern = self._to_search.get()

        if len(pattern) > 0: # If not empty
            self.search(pattern)

    def search(self, pattern, item=""): # Search on treeview (2)
        children = self.get_children(item)

        for child in children:
            text = self.item(child, "text")

            if text.lower().startswith(pattern.lower()) or text.lower() in pattern.lower() or pattern.lower() in text.lower():
                self.selection_set(child)
                self.see(child)
                return True
            else:
                result = self.search(pattern, child)
                if result:
                    return True


class HelpWindow(Application): # Help Window Make Help Window
    def __init__(self, previous_master):
        super().__init__() # Superclass (Application)

        self.previous_master = previous_master

        self.title("Help | " + config.BUILD_VERSION + " | By " + config.AUTHOR) # Window Title
        self.geometry("750x500") # Window Size

        # Window Contents

            # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.back, width=10, relief="raised", bd=3, bg="gray85")
        self.back_button.place(x=660, y=465)

            # Help Treeview
        treeview_style = ttk.Style(self)
        treeview_style.theme_use("clam")
        treeview_style.configure("Treeview", background="gray80", relief="sunken", fieldbackground="gray80")

        self.help_treeview = SearchableTreeview(self, self, height=22)
        self.help_treeview.place(x=10, y=10)

        self.help_treeview.heading("#0", text="Help Tree", anchor=tk.W)
        self.help_treeview.column("#0", minwidth=400, width=400, stretch=True)

                # Usage Help
        self.usage_help_node = self.help_treeview.insert("", "end", text="Usage", values=("main_node")) # Main

                # GENERAL USAGE HELP
        self.general_usage_node = self.help_treeview.insert(self.usage_help_node, "end", text="General", values=("usage_node")) # General (Node)

        self.help_treeview.insert(self.general_usage_node , "end", text='How to connect to database?', values=("general_usage_node")) # How to connect to database?

                # Keybinds Help
        self.keybinds_help_node = self.help_treeview.insert("", "end", text="Keybinds", values=("main_node")) # Main

                # SETTINGS KEYBINDS HELP
        self.settings_keybinds_node = self.help_treeview.insert(self.keybinds_help_node, "end", text="Settings", values=("keybinds_node")) # Settings (Node)

        self.help_treeview.insert(self.settings_keybinds_node, "end", text="Quick Save", values=("settings_keybinds_node")) # Quick Save (SETTINGS)
        self.help_treeview.insert(self.settings_keybinds_node, "end", text="Test Connection", values=("settings_keybinds_node")) # Test Connection (SETTINGS)

    def back(self): # Back to Main
        self.destroy()
        if self.previous_master == "main":
            setup()
        elif self.previous_master == "settings":
            self.settings = Settings()
            self.settings.mainloop()


class Settings(Application): # Settings Window
    def __init__(self):
        super().__init__() # Superclass (Application)

        self.title("Settings | " + config.BUILD_VERSION + " | By " + config.AUTHOR) # Window Title
        self.geometry("500x500") # Window Size

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.saved = False

        # Window Contents
            # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save, width=10, relief="raised", bd=3, bg="gray85")
        self.save_button.place(x=410, y=465)

            # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.back, width=10, relief="raised", bd=3, bg="gray85")
        self.back_button.place(x=320, y=465)

            # Reset Settings Button
        self.reset_settings_button = tk.Button(self, text="Reset settings", command=self.reset_settings, width=10, relief="raised", bd=3, bg="gray85")
        self.reset_settings_button.place(x=230, y=465)

            # Test Connection Button
        self.test_connection_button = tk.Button(self, text="Test Connection", command=self.test_connection, width=12, relief="raised", bd=3, bg="gray85")
        self.test_connection_button.place(x=125, y=465)

            # General Settings Setup
        self.general_settings_labelframe = tk.LabelFrame(self, text="General")
        self.general_settings_labelframe.grid(row=2, columnspan=2, sticky="WE", padx=5, pady=5, ipadx=5 , ipady=5)
        self.general_settings_labelframe.place(x=10, y=5)

            # MenuBar
        self.menubar = tk.Menu(self)

            # Help Menu
        self.menubar.add_command(label="Help", command=self.launch_help_window)

                # URL Settings (GENERAL)
        self.url_setting_label = tk.Label(self.general_settings_labelframe, text="Host URL:", font=self.hel10)
        self.url_setting_label.grid(row=0, column=0, sticky=tk.W)

        self.url_setting_entry = tk.Entry(self.general_settings_labelframe, width=50, relief="sunken", bd=2, font=self.hel10)
        self.url_setting_entry.grid(row=0, column=1, sticky=tk.W)

                # User Settings (GENERAL)
        self.user_setting_label = tk.Label(self.general_settings_labelframe, text="User:", font=self.hel10)
        self.user_setting_label.grid(row=1, column=0, sticky=tk.W)

        self.user_setting_entry = tk.Entry(self.general_settings_labelframe, width=25, relief="sunken", bd=2, font=self.hel10)
        self.user_setting_entry.grid(row=1, column=1, sticky=tk.W)

                # Password Settings (GENERAL)
        self.password_setting_label = tk.Label(self.general_settings_labelframe, text="Password:", font=self.hel10)
        self.password_setting_label.grid(row=2, column=0, sticky=tk.W)

        self.password_setting_entry = tk.Entry(self.general_settings_labelframe, width=25, relief="sunken", bd=2, font=self.hel10, show="•",)
        self.password_setting_entry.grid(row=2, column=1, sticky=tk.W)

                # Database Settings (GENERAL)
        self.database_setting_label = tk.Label(self.general_settings_labelframe, text="Database:", font=self.hel10)
        self.database_setting_label.grid(row=3, column=0, sticky=tk.W)

        self.database_setting_entry = tk.Entry(self.general_settings_labelframe, width=25, relief="sunken", bd=2, font=self.hel10)
        self.database_setting_entry.grid(row=3, column=1, sticky=tk.W)

            # Security Settings Setup
        self.security_settings_labelframe = tk.LabelFrame(self, text="Security")
        self.security_settings_labelframe.grid(row=2, columnspan=4, sticky="WE", padx=5, pady=5, ipadx=5, ipady=5)
        self.security_settings_labelframe.place(x=10, y=120)

                # Allowed tables Settings (SECURITY)
        self.allowed_tables_setting_label = tk.Label(self.security_settings_labelframe, text="Allowed tables: ↴", font=self.hel10b)
        self.allowed_tables_setting_label.grid(row=0, column=0, sticky=tk.W)

        self.allowed_tables_setting_add_label = tk.Label(self.security_settings_labelframe, text="Table name:", font=self.hel10)
        self.allowed_tables_setting_add_label.grid(row=1, column=0, sticky=tk.W)

        self.allowed_tables_setting_add_entry = tk.Entry(self.security_settings_labelframe, width=15, relief="sunken", bd=2, font=self.hel10)
        self.allowed_tables_setting_add_entry.grid(row=1, column=1, sticky=tk.W)

        self.allowed_tables_setting_add_button = tk.Button(self.security_settings_labelframe, text="Allow table", width=10, relief="raised", bd=3, bg="gray95", command=self.allow_table)
        self.allowed_tables_setting_add_button.place(x=125, y=65)

        self.allowed_tables_setting_delete_button = tk.Button(self.security_settings_labelframe, text="Remove table", width=10, relief="raised", bd=3, bg="gray95", command=self.remove_table)
        self.allowed_tables_setting_delete_button.place(x=125, y=100)

        self.allowed_tables_setting_added_list = tk.Listbox(self.security_settings_labelframe, relief="sunken", width=15, height=10, bd=3, bg="gray80")
        self.allowed_tables_setting_added_list.grid(row=2, column=0, sticky=tk.W)

            # Developer Settings Setup
        self.developer_settings_labelframe = tk.LabelFrame(self, text="Developer")
        self.developer_settings_labelframe.grid(row=2, columnspan=2, sticky="WE", padx=5, pady=5, ipadx=5, ipady=5)
        self.developer_settings_labelframe.place(x=10, y=360)

                # Connection Type Settings (DEVELOPER)
        self.connection_type_label = tk.Label(self.developer_settings_labelframe, text="Connection Type:", font=self.hel10)
        self.connection_type_label.grid(row=1, column=0, sticky=tk.W)

        self.chosen_connection_type = tk.StringVar()
        self.connection_types = {"mysql.connector (DEFAULT)"}

        self.connection_type_option_menu = tk.OptionMenu(self.developer_settings_labelframe, self.chosen_connection_type, *self.connection_types)
        self.connection_type_option_menu.grid(row=1, column=1, sticky=tk.W)

        self.settings = self.get_settings() # Get and set settings
        self.settings = { # Dictionary of Settings
            "url": self.settings[1],
            "user": self.settings[2],
            "password": self.settings[3],
            "database": self.settings[4],
            "connection_type": self.settings[5]
        }

        # Keybinds
        self.bind("<Control-s>", self.save) # Ctrl+S to Save
        self.bind("<Control-t>", self.test_connection) # Ctrl+T to Test Connection

        self.config(menu=self.menubar)
        self.update_allowed_tables()

    def launch_help_window(self): # Launch help window
        if messagebox.askokcancel("Quit", "Are you sure you want to go there?\nAny changes will be left unsaved."):
            self.destroy()
            self.help_menu = HelpWindow(previous_master="settings")
            self.help_menu.mainloop()

    def close(self): # If window is closed...
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?\nAny changes will be left unsaved."):
            self.destroy()

    def allow_table(self): # Allows table
        allowed_numbers = "0123456789"
        allowed_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        allowed_other_characters = "_-"

        allowed_characters = allowed_numbers + allowed_letters + allowed_other_characters

        self.to_allow = self.allowed_tables_setting_add_entry.get()

        for letter in self.to_allow:
            if letter not in allowed_characters:
                banned_character = True
                break
            else:
                banned_character = False

        self.allowed_tables_setting_add_entry.delete(0, "end")

        if self.to_allow in [table[0] for table in self.allowed_tables]:
            messagebox.showerror("Duplicate Table Error", "You cannot add duplicate tables!")
        elif banned_character == True:
            messagebox.showerror("Table Name Error", "Table Name contains a banned character!")
        elif self.to_allow[0] not in allowed_letters:
            messagebox.showerror("Table Name Error", "Table Name must start with a letter!")
        elif self.to_allow == "":
            messagebox.showerror("Table Name Error", "You must enter something!")
        else:
            self.allowed_tables.append((self.to_allow,))
            self.update_allowed_tables()

    def remove_table(self): # Removes table from "Allowed Tables"
        try:
            self.allowed_tables.remove((self.allowed_tables_setting_added_list.get(tk.ANCHOR),))
            self.update_allowed_tables()
        except ValueError:
            pass

    def update_allowed_tables(self): # Updates allowed tables list box
        self.allowed_tables_setting_added_list.delete(0, "end")

        for table in [table[0] for table in self.allowed_tables]:
            self.allowed_tables_setting_added_list.insert("end", table)

    def test_connection(self, event=None): # Tests database connection
        if self.settings["connection_type"] == "mysql.connector (DEFAULT)": # Connect DB
            try:
                self.mysql_connection = mysql.connector.connect(
                    host=self.settings["url"],
                    user=self.settings["user"],
                    passwd=self.settings["password"],
                    database=self.settings["database"]
                )
                if self.mysql_connection is not None:
                    self.mysql_cursor = self.mysql_connection.cursor()
                    self.mysql_cursor.close()

                    self.test_connection_button.configure(bg="lawn green", state="disabled")
                    self.after("5000", lambda: self.test_connection_button.configure(bg="gray85", state="normal"))
                    messagebox.showinfo("Test Success", "Success!")
                else:
                    self.test_connection_button.configure(bg="firebrick1", state="disabled")
                    self.after("5000", lambda: self.test_connection_button.configure(bg="gray85", state="normal"))
                    messagebox.showerror("Test Failed", "Could not connect to [{}].".format(self.settings["url"]))
            except Exception as error:
                self.test_connection_button.configure(bg="firebrick1", state="disabled")
                self.after("5000", lambda: self.test_connection_button.configure(bg="gray85", state="normal"))
                messagebox.showerror("Test Failed", "Test Error: {}".format(error))

    def save(self, event=None): # Save changes
        if not self.saved:
            try:
                raw_url = self.url_setting_entry.get()

                if " " in raw_url:
                    self.url_setting_entry.configure(bg="orange2")
                    self.after("5000", lambda: self.url_setting_entry.configure(bg="white"))
                    messagebox.showerror("URL Name Error", "You cannot have a ' ' inside the Host URL!")
                    return
                elif ("https://" not in raw_url and "http://" not in raw_url) and raw_url != "localhost":
                    self.url_setting_entry.configure(bg="orange2")
                    self.after("5000", lambda: self.url_setting_entry.configure(bg="white"))
                    if not messagebox.askokcancel("Missing HTTP/S", "URL is missing 'http://' or 'https://'.\nAre you sure you want to save?"):
                        return

                # Creating Database
                db_conn = sqlite3.connect("settings.db")

                with db_conn:
                    if db_conn is not None:
                        db_cursor = db_conn.cursor()

                        # Save settings
                        db_cursor.execute("REPLACE INTO settings VALUES (:rowid, :url, :user, :password, :database, :connection_type)",
                                        {
                                            "rowid": 1,
                                            "url": raw_url,
                                            "user": self.user_setting_entry.get(),
                                            "password": self.password_setting_entry.get(),
                                            "database": self.database_setting_entry.get(),
                                            "connection_type": self.chosen_connection_type.get()
                                        }
                                    )

                        db_cursor.execute("DELETE FROM allowed_tables")
                        db_cursor.executemany("INSERT INTO allowed_tables VALUES (?);", self.allowed_tables)

                        db_cursor.execute("SELECT * FROM settings")

                        new_settings = db_cursor.fetchone() # Get and set settings
                        self.settings = { # Dictionary of Settings
                            "url": new_settings[1],
                            "user": new_settings[2],
                            "password": new_settings[3],
                            "database": new_settings[4],
                            "connection_type": new_settings[5]
                        }

                        db_conn.commit()

                        self.saved = True

                        self.save_button.configure(bg="lawn green", state="disabled")
                        messagebox.showinfo("Success", "Settings have been saved!")

                        self.after("5000", lambda: self.save_button.configure(bg="gray85", state="normal"))
                        self.after("5000", self.set_saved_false)
            except Exception as error:
                self.save_button.configure(bg="red2", state="disabled")
                messagebox.showerror("Error", "ERROR: " + str(error) + "\nCheck your modifications or call developer.")

    def set_saved_false(self): # Used in self.save(). Sets self.saved to False
        self.saved = False

    def back(self): # Back to Main
        if messagebox.askokcancel("Go back", "Are you sure you want to go back?\nAny changes will be left unsaved."):
            self.destroy()
            setup()

    def get_settings(self): # Get current settings
        db_conn = sqlite3.connect("settings.db")

        with db_conn:
            if db_conn is not None:
                db_cursor = db_conn.cursor()

                db_cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
                                            rowid INTEGER PRIMARY KEY,
                                            url TEXT,
                                            user TEXT,
                                            password TEXT,
                                            database TEXT,
                                            connection_type TEXT
                                    );""")

                db_cursor.execute("""CREATE TABLE IF NOT EXISTS allowed_tables (
                                            table_name TEXT
                                    );""")

                db_cursor.execute("SELECT * FROM settings")

                if not db_cursor.fetchone():
                    db_cursor.execute("""INSERT INTO settings ('rowid', 'url', 'user', 'password', 'database', 'connection_type')
                                            VALUES (1, :default_url, :user, :password, :database, :connection_type)""",
                                        {
                                            "default_url": "https://",
                                            "user": "root",
                                            "password": "root",
                                            "database": "database",
                                            "connection_type": "mysql.connector (DEFAULT)"
                                        })

                db_cursor.execute("SELECT * FROM settings")
                row = db_cursor.fetchone()

                self.url_setting_entry.insert(0, row[1]) # SET URL
                self.user_setting_entry.insert(0, row[2]) # SET USER
                self.password_setting_entry.insert(0, row[3]) # SET PASSWORD
                self.database_setting_entry.insert(0, row[4]) # SET DATABASE
                self.chosen_connection_type.set(row[5]) # SET CONNECTION TYPE

                db_cursor.execute("SELECT * FROM allowed_tables")
                self.allowed_tables = db_cursor.fetchall()

                self.update_allowed_tables()

                db_cursor.execute("SELECT * FROM settings")
                return db_cursor.fetchone()

    def reset_settings(self): # Reset current settings
        if messagebox.askokcancel("Reset Settings?", "Are you sure you want to reset ALL settings?\nThis includes Allowed Tables."):
            db_conn = sqlite3.connect("settings.db")

            with db_conn:
                if db_conn is not None:
                    db_cursor = db_conn.cursor()

                    db_cursor.execute("DELETE FROM settings")
                    db_cursor.execute("DELETE FROM allowed_tables")

            # Clear all entries/listboxes
            self.url_setting_entry.delete(0, tk.END)
            self.user_setting_entry.delete(0, tk.END)
            self.password_setting_entry.delete(0, tk.END)
            self.database_setting_entry.delete(0, tk.END)
            self.allowed_tables_setting_add_entry.delete(0, tk.END)
            self.allowed_tables_setting_added_list.delete(0, tk.END)

            self.reset_settings_button.configure(bg="lawn green", state="disabled")
            self.after("5000", lambda: self.reset_settings_button.configure(bg="gray85", state="normal"))

            messagebox.showinfo("Settings Reset", "Settings have been rest!")

            self.get_settings()


class Main(Application): # Main Window
    def __init__(self):
        super().__init__() # Superclass (Application)

        self.resizable(1, 1) # Enable Resizing
        self.minsize(500, 500) # Minimum Window Size (500x500)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(2, weight=1)

        for row in range(2):
            self.grid_rowconfigure(row, weight=1)
        for column in range(2):
            self.grid_columnconfigure(column, weight=1)

        # Settings
        self.settings, self.allowed_tables = self.get_settings()
        self.settings = {
            "url": self.settings[1],
            "user": self.settings[2],
            "password": self.settings[3],
            "database": self.settings[4],
            "connection_type": self.settings[5]
        }

        self.status = True
        self.viewing_table = None
        self.selected_table = tk.StringVar()

        # Window Contents
            # MenuBar
        self.menubar = tk.Menu(self)

            # Settings Menu
        self.menubar.add_command(label="Settings", command=self.launch_settings_window)

            # Connection Menu
        self.connection_menu = tk.Menu(self, tearoff=False)
        self.menubar.add_cascade(label="Connection", menu=self.connection_menu)

        self.connection_menu.add_command(label="Connect to Database", command=self.connect_db)
        self.connection_menu.add_command(label="Disconnect from Database", command=self.disconnect_db)

            # Status Box
        self.status_labelframe = tk.LabelFrame(self, text="Status")
        self.status_labelframe.grid(row=2, columnspan=2, sticky="SE", padx=5, pady=5)
        self.status_labelframe.grid(row=2, column=0, sticky="sw")

        self.status_label = tk.Label(self.status_labelframe, font=self.hel10, relief="sunken", bd=2)
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        self.disconnect_db()

        # View Menu
        self.view_menu = tk.Menu(self, tearoff=False)
        self.menubar.add_cascade(label="View", menu=self.view_menu)

        self.update_view_tables()

            # Help Menu
        self.menubar.add_command(label="Help", command=self.launch_help_window)

            # Database Frame TODO: Make database scale
        self.database_frame = tk.Frame(self, bd=2, relief="raised")

        self.config(menu=self.menubar)

    def update_view_tables(self): # Update Tables to View
        try:
            self.view_menu.delete(0, "end")
            if self.status == True:
                        if self.allowed_tables:
                            self.selected_table.set("None")

                            for allowed_table in self.allowed_tables:
                                self.view_menu.add_radiobutton(label=allowed_table, variable=self.selected_table, value=allowed_table, command=lambda table_name=allowed_table: self.update_database_frame(table_name))

                            self.view_menu.add_radiobutton(label="None", variable=self.selected_table, value="None", command=lambda: self.update_database_frame(None))
                            
                            self.update_database_frame(None)
                        else:
                            self.view_menu.add_command(label="No Tables", state="disabled")
            else:
                self.view_menu.add_command(label="Not Connected", state="disabled")
        except AttributeError:
            pass
    
    def update_database_frame(self, table_name): # Update Database Frame
        if table_name is None:
            try:
                self.database_frame.destroy()
                self.database_frame = tk.Frame(self, bd=2, relief="raised")
                self.database_frame.grid(column=1, row=1, sticky="nesw")
                
            except AttributeError:
                pass

            self.x_label = tk.Label(self.database_frame, text="✕", font="helvetica 275 bold", bg="gray75")
            self.x_label.pack(anchor="center", expand=1 )
                
            self.viewing_table = None
        else:
            try:
                self.database_frame.destroy()
                self.database_frame = tk.Frame(self, bd=2, relief="raised")
                self.database_frame.grid(column=1, row=1, sticky="nesw")
            except AttributeError:
                pass
                
            try:
                mysql_cursor = self.mysql_connection.cursor()
            
                mysql_cursor.execute("SELECT * FROM " + table_name[0])

                row_no_header = tk.Label(self.database_frame, text="", width=10, bg="gray70", relief="ridge")
                row_no_header.grid(row=0, column=0)

                column_name_no = 1
                for column_name in mysql_cursor.column_names:
                    db_column_name = tk.Label(self.database_frame, text=column_name, width=10, bg="gray70", relief="ridge")
                    db_column_name.grid(row=0, column=column_name_no)
                    column_name_no += 1
                
                row_no = 1

                row_count = len(mysql_cursor.fetchall())

                mysql_cursor.execute("SELECT * FROM " + table_name[0])

                for row_enum in range(1, row_count + 1):
                    row_no_label = tk.Label(self.database_frame, text=row_enum, width=10, bg="gray70", relief="groove")
                    row_no_label.grid(row=row_no, column=0)
                    row_no += 1

                row_no = 1

                for row in mysql_cursor:
                    for column in range(0, len(row)):
                        db_cell = tk.Entry(self.database_frame, width=10, relief="sunken")
                        db_cell.grid(row=row_no, column=column+1)
                        db_cell.insert(tk.END, row[column])
                    row_no += 1
                    
            except mysql.connector.errors.ProgrammingError as error:
                messagebox.showerror("MySQL Table Error", "Error has occured: {}".format(error))

            self.viewing_table = table_name[0]

    def launch_settings_window(self): # Launch settings window
        self.disconnect_db()
        self.destroy()
        self.settings = Settings()
        self.settings.mainloop()

    def launch_help_window(self): # Launch help window
        self.disconnect_db()
        self.destroy()
        self.help_menu = HelpWindow(previous_master="main")
        self.help_menu.mainloop()

    def get_settings(self): # Get current settings
        db_conn = sqlite3.connect("settings.db")

        with db_conn:
            if db_conn is not None:
                db_cursor = db_conn.cursor()

                db_cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
                                            rowid INTEGER PRIMARY KEY,
                                            url TEXT,
                                            user TEXT,
                                            password TEXT,
                                            database TEXT,
                                            connection_type TEXT
                                    );""")

                db_cursor.execute("""CREATE TABLE IF NOT EXISTS allowed_tables (
                                            table_name TEXT
                                    );""")

                db_cursor.execute("SELECT * FROM settings")

                if not db_cursor.fetchone():
                    db_cursor.execute("""INSERT INTO settings ('rowid', 'url', 'user', 'password', 'database', 'connection_type')
                                            VALUES (1, :default_url, :user, :password, :database, :connection_type)""",
                                        {
                                            "default_url": "https://",
                                            "user": "root",
                                            "password": "root",
                                            "database": "database",
                                            "connection_type": "mysql.connector (DEFAULT)"
                                        })

                db_cursor.execute("SELECT * FROM settings")
                settings = db_cursor.fetchone()

                db_cursor.execute("SELECT * FROM allowed_tables")
                allowed_tables = db_cursor.fetchall()

                db_conn.commit()
                return settings, allowed_tables

    def disconnect_db(self):
        if self.status:
            if self.settings["connection_type"] == "mysql.connector (DEFAULT)":

                try:
                    if self.mysql_connection is not None:
                        self.mysql_cursor.close()
                except AttributeError:
                    pass

            self.connection_menu.entryconfig(1, state="disabled")
            self.connection_menu.entryconfig(0, state="normal")
            self.status = False
            self.viewing_table = None
            self.status_label.configure(bg="gray75", text="Disconnected")

            try:
                self.x_label.pack_forget()
                self.database_frame.place_forget()
            except AttributeError:
                pass

            self.update_view_tables()

    def connect_db(self):
        if not self.status:
            if self.settings["connection_type"] == "mysql.connector (DEFAULT)":
                try:
                    self.mysql_connection = mysql.connector.connect(
                        host=self.settings["url"],
                        user=self.settings["user"],
                        passwd=self.settings["password"],
                        database=self.settings["database"]
                    )
                    if self.mysql_connection is not None:
                        self.mysql_cursor = self.mysql_connection.cursor()

                        self.on_database = None
                        self.connection_menu.entryconfig(0, state="disabled")
                        self.connection_menu.entryconfig(1, state="normal")
                        self.status = True
                        self.status_label.configure(bg="lawn green", text="Connected")
                    else:
                        password_to_show = "".join("*" for letter in self.settings[3])
                        messagebox.showerror("MySQL Error", "There was a problem connecting to the MySQL Database.\nPlease check your settings:\nHost URL: {}\nUser: {}\nPassword: {}\nDatabase: {}".format(
                            self.settings["url"], self.settings["user"], self.settings["password"], self.settings["database"]))
                except Exception as error:
                    messagebox.showerror("MySQL Error", "Error: {}".format(error))
                else:
                    self.update_view_tables()


def setup(): # Main Menu Setup
    main = Main() # Main Menu Window (init)
    main.mainloop() # Window Loop


if __name__ == "__main__": # If Program is run directly...
    os.chdir(os.path.dirname(__file__))

    try:
        os.chdir(r"./Files/")
    except FileNotFoundError: # Shouldn't happen anymore
        os.chdir(r"./Python (Windows 10)/Files/") # Edit based on folder name

    setup() # App Setup