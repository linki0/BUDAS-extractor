#
# This program allow one to transfer the result from the annotator to the database
#
# You need to change the usernbame and password variable
#    together with the location of the file to be uploaded
#

import mysql.connector
import re

re1 = re.compile(':.*:')
user1 = "root"
password1 = "root"

fname = "c:/cygwin64/home/KingIp/_floorplan/01-14/BUDAS_output.txt"

mydb = mysql.connector.connect( host="localhost", user=user1, passwd=password1,database="archalyze_db_v2")
print(mydb)


hid = input("Enter house ID ")
sql = "SELECT house_id FROM houses where house_id = " + str(hid)
cur = mydb.cursor(sql)
cur.execute(sql)
cur.fetchall()
print(cur.rowcount)

if (cur.rowcount == 0):4
    print("No house with that ID, exiting.")
    exit()
f = open(fname)
print(f)
print(re1.search("ab:asda:a"))
room_num = 1
for line in f:
    print(line)
    m =  re1.search(line)
    print(m)
    if m:
        g = m.group()
        g1 = g[1:-1]
        print(m.group())
        print(g1)
        print(g1.strip())
        #isql = "INSERT INTO rooms VALUES (" + str(room_num) + ", " + str(hid) + ', \"' + g1 + '\")'
        isql = "INSERT INTO rooms VALUES (" + str(room_num) + ", "+  str(hid) + ', \"' + g1 + '\", 0, "terminate", 0, 0, 0, "other")'
        print(isql)
        cur.execute(isql)        
        room_num = room_num + 1
        mydb.commit()
print("Database updated")
