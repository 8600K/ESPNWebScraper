from cryptography.fernet import Fernet
import customtkinter
import sqlite3
import uuid
from tkinter import messagebox
import Login


#Registers the user. Creates the CustomTKinter box and all the buttons, checkboxes, and labels needed.
def register(login_root):

    register_root = customtkinter.CTk()
    register_root.geometry("850x550")
    register_root.title("Register")
                       
    register_root.attributes('-topmost', True)
    register_root.update()

    register_frame = customtkinter.CTkFrame(master=register_root)
    register_frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=register_frame, text="Register")
    label.pack(pady=12, padx=10)

    entry0 = customtkinter.CTkEntry(master=register_frame, placeholder_text="Username")
    entry0.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=register_frame, placeholder_text="Password", show="*")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=register_frame, placeholder_text="Confirm Password", show="*")
    entry2.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=register_frame, text="Register", command=lambda: submit(entry0.get(), entry1.get(), entry2.get(), checkbox.get(), register_root))
    button.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=register_frame, text="Remember Me", onvalue=True, offvalue=False)
    checkbox.pack(pady=12, padx=10)

    new_button = customtkinter.CTkButton(master=register_frame, text="Already have an account? Sign in.", command=lambda: [Login.show_login(login_root), destroy_register(register_root)])
    new_button.pack(pady=10, padx=10)

#Destroy the Register Window. Instead of hiding it, this should only ever need to run one time. Therefore I destroy it, if for whatever reason the user needs to register again, I will gladly take the
#small hit in speed to ensure 99% of users have a better experience with less memory leaks. 
def destroy_register(root):
    root.after(100, root.destroy)
    #The small delay is to ensure proper operation. Otherwise a little error pops up in the terminal.
    #Nothing actually breaks, just slightly annoying. This way we keep a window running before deleting the
    #Registration window, which Tkinter appreciates.   

#When the users registers a new user. 
def submit(user, passw, confirm, checkbox, root):
    name = user
    password = passw
    conf = confirm
    mac = uuid.getnode()
    memory = checkbox
    

    if(name == ""):
        messagebox.showerror("Login Error", "Please enter a valid username.")
    elif(confirm != password):
        messagebox.showerror("Login Error", "Passwords do not match.")
    elif(confirm == ""):
        messagebox.showerror("Login Error", "Password cannot be left blank.")
    else:
        print("Success. Signing in...")
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(bytes(confirm, 'utf-8'))
        connect = sqlite3.connect('WebScraper.db')
        cursor = connect.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS registered_users
                                (username text PRIMARY KEY, password text, key text, mac text, memory boolean)''')
        
        cursor.execute('''INSERT OR IGNORE INTO registered_users (username, password, key, mac, memory) VALUES (?, ?, ?, ?, ?)''',
                                (name, encrypted, key, mac, memory))
    
        connect.commit()
        destroy_register(root)
        if(checkbox == True):
            Login.login(user, passw)
        else:
            Login.login(None, None)

        
        
         
        
