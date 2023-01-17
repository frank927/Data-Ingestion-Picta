import sqlite3

connection=sqlite3.connect("Picta/Picta.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Comments (Links TEXT PRIMARY KEY, Comments TEXT NOT NULL, Num TEXT, Category TEXT, Published TEXT)")

cursor.execute("SELECT SUM(Num) FROM Comments;")   
Total=cursor.fetchall()
#print(Total)

cursor.execute("""DELETE FROM Comments WHERE Num="14" """)
connection.commit()

#cursor.execute("drop table Comments")
#connection.commit() 
        
