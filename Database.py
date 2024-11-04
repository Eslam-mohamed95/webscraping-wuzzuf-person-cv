import sqlite3 


class Database:
   
    def __init__(self):
        
        self.db = sqlite3.connect("personal_infromation.db")# connect dadabase
        self.database = self.db.cursor() # make cursor to data connection
        self.database.execute("create table if not exists data (name text, location text , skills text , language text , works text)")
        self.db.commit()

    # insert values in database table
    def insert(self, name, location, all_skill, all_languages, job):

        self.db= sqlite3.connect("personal_infromation.db")
        self.database =self.db.cursor() 

    # data save in data base      
        self.database.execute("insert into data (name , location , skills , language , works) values (?,?,?,?,? )",
                                (name, location, all_skill, all_languages, job))
        
    # show you >> one of data for personal was saved 
        self.database.execute("select * from data")
    # close data_base
        self.db.commit()
        self.db.close()
    