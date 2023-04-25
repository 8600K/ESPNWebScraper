
#Project to scrape data off of ESPN and then run some fun analytics.
from cgitb import text
import requests 
import customtkinter 
import sqlite3
import tkinter

#Python Files we are running.
import Database

from datetime import date
from bs4 import BeautifulSoup

#This function creates the scraper page. Pretty much the same as all the other pages with only a couple differences in commands and some widgets.
def scraper(username):

    register_root = customtkinter.CTk()
    register_root.geometry("850x550")
    register_root.title("Web Scraper")
                       
    register_root.attributes('-topmost', True)
    register_root.update()

    register_frame = customtkinter.CTkFrame(master=register_root)
    register_frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=register_frame, text="Search ESPN")
    label.pack(pady=12, padx=10)

    entry0 = customtkinter.CTkEntry(master=register_frame, placeholder_text="Search ESPN's daily articles for:", width=250)
    entry0.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=register_frame, text="Search", command=lambda: nfl_scraper(entry0.get(), text_box))
    button.pack(pady=12, padx=10)

    button1 = customtkinter.CTkButton(master=register_frame, text="Save to Database", command=lambda: save_to_database(username, entry0.get(), text_box))
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=register_frame, text="Go To Database", command=lambda: [destroy_page(register_root), Database.database_page(username)])
    button2.pack(pady=12, padx=10)

    text_box = customtkinter.CTkTextbox(master=register_frame, width=400, wrap="word")
    text_box.pack(pady=12, padx=10)
    
    
    
    #text_list = nfl_scraper()
    #print(text_list)
def destroy_page(root):
    root.withdraw()
    
    
#Here's what actually delivers the user data. We connect to ESPN/NFL using BeautifulSoup, then search their headers for the headlines.
#Afterwards we can insert that into a database if we press the 'Save to Database' button.
#The function also clears any former input from previous searches everytime it runs.
def nfl_scraper(input_text, text_box):
    r_nfl =  requests.get("https://www.espn.com/nfl/")
    #Empties the Textbox for multiple searches.
    text_box.delete("1.0", tkinter.END)
    
    #This should say 200, it just lets us know the status of the website we're trying to scrape.
    print(r_nfl.status_code)

    soup = BeautifulSoup(r_nfl.content, 'html.parser')

    search = soup.find('section', id='news-feed')


    headers = search.find_all('h2')

    print(headers)

    for header in headers:
        if(input_text.lower() in header.text.lower()):
            text_box.insert("0.0", header.text + "\n")

#This saves the current content in the textbox to the database. It saves it in NFLData table with Username, date_added, headline, and search_term.
def save_to_database(username, search_term, text_box):
    connect = sqlite3.connect('WebScraper.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS NFLData
                                (username text, date_added date, headline text, search_term text)''')


    today = date.today()

    split_text = (text_box.get("1.0", tkinter.END).split('\n'))
    #Minus 2 because of what Split does with Tkinter objects.
    length_mod = len(split_text) - 2

    for counter, i in enumerate(split_text):
        if(counter >= length_mod):
            break

        print(i)
        cursor.execute('''INSERT INTO NFLData (username, date_added, headline, search_term) VALUES (?, ?, ?, ?)''', 
                       (username, today, i, search_term))

        connect.commit()

