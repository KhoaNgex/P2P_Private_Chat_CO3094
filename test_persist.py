import sqlite3
import persistence as ps

try:
    # Connect to DB 
    cnt = sqlite3.connect('user.db')
    # open a cursor
    cursor = cnt.execute('''SELECT NAME, PASSWORD FROM users;''')
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

# username = 'khoacaotran'
# print (ps.get_user_password(username))

