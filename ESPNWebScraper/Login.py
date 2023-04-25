import customtkinter 
import sqlite3
from tkinter import messagebox
import uuid
from cryptography.fernet import Fernet

import Register
import ESPNWebScraper


#Logins. Same as Register except for a few changes. Overall a class system would have been efffective here but I digress. 
def login(username, decodedpassword):

    customtkinter.set_appearance_mode("dark")

    customtkinter.set_default_color_theme("dark-blue")

    login_root = customtkinter.CTk()
    login_root.geometry("850x550")
    login_root.title("Login")

    login_frame = customtkinter.CTkFrame(master=login_root)
    login_frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=login_frame, text="Login")
    label.pack(pady=12, padx=10)

    entry0 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username")
    entry0.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
    entry1.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=login_frame, text="Login", command=lambda: sign_in(entry0.get(), entry1.get(), login_root))
    button.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=login_frame, text="Remember Me", onvalue=True, offvalue=False)
    checkbox.pack(pady=12, padx=10)

    new_button = customtkinter.CTkButton(master=login_frame, text="Don't have an account? Register now.", command=lambda: [hide_login(login_root), Register.register(login_root)])
    new_button.pack(pady=10, padx=10)

    if(username != None):
        entry0.insert(0, username)
        entry1.insert(0, decodedpassword)
        checkbox.select()

    login_root.mainloop()
    
#Hide the login page. (Please note this does not take the page out of memory, the reason for this is because the user will still need to login after completing the register page. Therefore I did
#not want to have to reload this page, small performance tweak that ensures smooth operations in day to day operation).
def hide_login(root):
    root.withdraw()

#Reshow the Login Page
def show_login(root):
    root.deiconify()

#Signs the user in assuming they used credentials that exist within the database.
def sign_in(check_name, check_pass, root):
    connect = sqlite3.connect('WebScraper.db')
    cursor = connect.cursor()
    try:
        credentials = cursor.execute('''SELECT * FROM registered_users WHERE username=?''', (check_name,))
        credentials = cursor.fetchone()
        check_username = credentials[0]
        key = bytes(credentials[2])
        cipher = Fernet(key)
        password_decoded = cipher.decrypt(credentials[1]).decode('utf-8')

        if(check_pass == password_decoded):
            print("Now we log in.")
            ESPNWebScraper.scraper(check_username)
            hide_login(root)
        else:
            messagebox.showerror("Login Error", "Invalid Password.")

    except Exception as ex:
        print("No user by that name!")
        messagebox.showerror("Login Error", "That user does not exist.")
        

    connect.commit()

#This function checks to see if the device that is logging in has registered before with the "Remember Me" feature. I used uuid Mac addresses to determine 
#Who registered and saved both the Mac uuid and whether or not they put "Remember Me" in the database. This searches through and returns if both of those are true.
def check_database_memory():
    connect = sqlite3.connect('WebScraper.db')
    try:
        cursor = connect.cursor()
        mac = uuid.getnode()
        check_memory = cursor.execute('''SELECT memory FROM registered_users WHERE mac=?''', (mac,))
        check_memory = cursor.fetchall()
        for checks in check_memory:
            print(checks)

            if(checks[0] == 1):
                credentials = cursor.execute('''SELECT username, password, key FROM registered_users where mac=? and memory=1''', (mac,))
                credentials = cursor.fetchone()
                print("Test:", credentials)
                key = bytes(credentials[2])
                cipher = Fernet(key)
                password_decoded = cipher.decrypt(credentials[1])
                print(password_decoded)
            
                return credentials[0], password_decoded
    except Exception as ex:
        print("Database does not exist!")
        return None
        
        