## /!\ only run one time to init table users 

import sqlite3

try: 
    # Connect to DB and create a cursor
    cnt = sqlite3.connect('user.db')
    # create table USERS
    cnt.execute('''CREATE TABLE users(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT UNIQUE,
        PASSWORD TEXT,
        IPADDRESS TEXT,
        PORT INTEGER
        );''')
# Handle errors
except sqlite3.Error as error:
    print('Error occured - ', error)
# Close DB Connection irrespective of success or failure
finally:
    if cnt:
        cnt.close()
        print('SQLite Connection closed')