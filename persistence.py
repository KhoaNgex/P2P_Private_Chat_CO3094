import sqlite3

def get_all_users():
    try:
        # Connect to DB 
        cnt = sqlite3.connect('user.db')
        # open a cursor
        cursor = cnt.execute('''SELECT NAME FROM users;''')
        user_list = []
        for row in cursor:
            user_list.append(row[0])

        cursor.close() # close cursor
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 
        return user_list

def get_user_password(username):
    try:
        # Connect to DB 
        cnt = sqlite3.connect('user.db')
        # open a cursor
        cursor = cnt.execute('''SELECT PASSWORD FROM users WHERE NAME = ?;''', (username,))
        result = []
        for row in cursor:
            result.append(row[0])

        cursor.close() # close cursor
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 
        return str(result[0])

def add_new_user(username, password):
    try:
        # Connect to DB 
        cnt = sqlite3.connect('user.db')
        # insert new record 
        cnt.execute('''INSERT INTO users (NAME,PASSWORD) VALUES(?,?);''', (username,password,))
        cnt.commit() # save the change
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 

def delete_user(username):
    try:
        # Connect to DB
        cnt = sqlite3.connect('user.db')
        # delete a record 
        cnt.execute('''DELETE FROM users WHERE NAME = ?;''', (username,))
        cnt.commit()
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 

def update_user_password(username, password):
    try:
        # Connect to DB
        cnt = sqlite3.connect('user.db')
        # update a record 
        cnt.execute('''UPDATE users SET PASSWORD = ? WHERE NAME = ?;''', (password, username,))
        cnt.commit()
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 

def update_user_address_port(username, ipaddress, port):
    try:
        # Connect to DB
        cnt = sqlite3.connect('user.db')
        # update a record 
        cnt.execute('''UPDATE users SET IPADDRESS = ?, PORT = ? WHERE NAME = ?;''', (ipaddress,port,username));
        cnt.commit()
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 

def get_all_table():
    try:
        # Connect to DB 
        cnt = sqlite3.connect('user.db')
        # open a cursor
        cursor = cnt.execute('''SELECT * FROM users;''')
        user_list = []
        for row in cursor:
            user_list.append(row)

        cursor.close() # close cursor
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 
            print (user_list)

def delete_all_users():
    try:
        # Connect to DB
        cnt = sqlite3.connect('user.db')
        # delete a record 
        cnt.execute('''DELETE FROM users;''', )
        cnt.commit()
    # Handle errors
    except sqlite3.Error as error:
        print('Error occured - ', error)
    # Close DB Connection irrespective of success or failure
    finally:
        if cnt:
            cnt.close() 
