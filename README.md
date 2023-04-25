# ESPNWebScraper
Web Scraper portfolio project made using Python 3+, SQLite 3, user interface created by CustomTkinter, and web scraping done via Beautiful Soup. Includes a login / register page, which saves via database, and then a web scraper that connects to ESPN/NFL and pulls headlines from their daily site.

Video Presentation: https://www.youtube.com/watch?v=PJihszxzDno&ab_channel=MilesEngelbrecht

The Login/Register pages include all the usual login logic you'd expect, with checks to ensure blank fields are not allowed, passwords match, etc etc. There is also a "remember me" feature, I used uuid and take the user's MAC address, store it in the database, with a corresponding boolean variable. If the user asked the application to rmember them, the database will see their mac address matches and auto import their user/password the next time they log in. Database also stores passwords fully encrypted thanks to Fernet. After the user logs in, they are able to enter a search term for ESPN headlines, and if that search term matches any headlines they will be returned into a text box. The user can save those headlines into a database which will also save some other useful information like what user searched, when it was searched, and what the seach term was. Lastly there is another page dedicated to pulling data that has been saved out of the database, this page allows the user to comb through the database by way of search term, article name, or user name. Again, all the relevant data (if there is any) will be read from the database and inserted into the page's textbox.  
