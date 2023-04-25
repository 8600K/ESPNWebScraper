#Created by Miles Engelbrecht as a learning and portfolio project.

import Login

user_id = None
password_decoded = None

#This code checks for if a user is already registered by combing through the database. 
signed_in = Login.check_database_memory()
#This ensures the program will run smoothly regardless of if the table has been created or not.
if(signed_in != None):
    user_id = signed_in[0]
    password_decoded = signed_in[1]
    print(user_id)
Login.login(user_id, password_decoded)
