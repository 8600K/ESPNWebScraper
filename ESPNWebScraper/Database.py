import customtkinter 
import sqlite3

import ESPNWebScraper

def database_page(username):

    database_root = customtkinter.CTk()
    database_root.geometry("850x550")
    database_root.title("Web Scraper")
                       
    database_root.attributes('-topmost', True)
    database_root.update()

    database_frame = customtkinter.CTkFrame(master=database_root)
    database_frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=database_frame, text="Search Database")
    label.pack(pady=12, padx=10)

    menu = customtkinter.StringVar(database_root)

    dropdown = customtkinter.CTkComboBox(master=database_frame, values=["Search by Username", "Search by Search Term", "Search by Article"], width=250, state="readonly")
    dropdown.set("Search by Username")
    dropdown.pack(pady=12, padx=10)

    entry0 = customtkinter.CTkEntry(master=database_frame, placeholder_text="Search Database for:", width=250)
    entry0.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=database_frame, text="Search", command=lambda: search_database(dropdown.get(), entry0.get(), text_box))
    button.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=database_frame, text="Go to Scraper", command=lambda: [ESPNWebScraper.scraper(username), destroy_page(database_root)])
    button2.pack(pady=12, padx=10)

    text_box = customtkinter.CTkTextbox(master=database_frame, width=400, wrap="word")
    text_box.pack(pady=12, padx=10)


def search_database(dropdown, entry, text_box):
    print(dropdown)
    print("ENTRY: ",entry)

    #Empties the Textbox for multiple searches.
    text_box.delete("1.0", customtkinter.END)

    sql_query = ""
    connect = sqlite3.connect('WebScraper.db')
    cursor = connect.cursor()

    if(dropdown == "Search by Article"):
        sql_query = '''SELECT * FROM NFLData WHERE headline = ?'''
        cursor.execute(sql_query, (entry,))

        records = cursor.fetchall()
        for row in records:
            print("Name: ", row[0])
            print("Date: ", row[1])
            print("Headline: ", row[2])
            print("Search-Term: ", row[3])
            text_box.insert("0.0", ("Name: " + str(row[0]) + "\n" +
                        "Date: " + str(row[1]) + "\n" +
                         "Headline: " + str(row[2]) + "\n" +
                         "Search-Term: " + str(row[3]) + "\n") )

    elif(dropdown == "Search by Username"):
        sql_query = '''SELECT * FROM NFLData WHERE username = ?'''
        cursor.execute(sql_query, (entry,))

        records = cursor.fetchall()
        for row in records:
            print("Name: ", row[0])
            print("Date: ", row[1])
            print("Headline: ", row[2])
            print("Search-Term: ", row[3])
            text_box.insert("0.0", ("Name: " + str(row[0]) + "\n" +
                        "Date: " + str(row[1]) + "\n" +
                         "Headline: " + str(row[2]) + "\n" +
                         "Search-Term: " + str(row[3]) + "\n") )

    elif(dropdown == "Search by Search Term"):
        sql_query = '''SELECT * FROM NFLData WHERE search_term = ?'''
        cursor.execute(sql_query, [entry])

        records = cursor.fetchall()
        for row in records:
            print("Name: ", row[0])
            print("Date: ", row[1])
            print("Headline: ", row[2])
            print("Search-Term: ", row[3])
            text_box.insert("0.0", ("Name: " + str(row[0]) + "\n" +
                        "Date: " + str(row[1]) + "\n" +
                         "Headline: " + str(row[2]) + "\n" +
                         "Search-Term: " + str(row[3]) + "\n") )
    else:
        print("An Error has occured. Please try again.")
        return

    


def destroy_page(root):
    root.withdraw()