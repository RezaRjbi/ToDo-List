import sqlite3
import os
import logging

is_not_dir = True
while is_not_dir:  # if there is no "data" directory it will create one, else it do nothing
    try:
        logging.basicConfig(filename="data/task.log", level=logging.INFO,
                            format="%(levelname)s:%(asctime)s: %(message)s")
        is_not_dir = False
    except FileNotFoundError:
        os.mkdir("data")


class Database:
    """
    front end (todo.py) uses this class
    and its functions to query on database
     and make changes
    """
    def __init__(self, dbname):
        self.con = sqlite3.connect("data/" + dbname)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS todolist(id INTEGER PRIMARY KEY ,task text)")  # create a todolist
        # table in data base
        # if this table already exist in database it will do nothing

    def view(self):
        self.cur.execute("SELECT * FROM Todolist")
        return self.cur.fetchall()  # fetch all rows in database and return it as a list

    def add(self, task):
        self.cur.execute("INSERT INTO todolist VALUES(NULL,:task)", {"task": task}) # add task to task column in db
        self.con.commit()
        logging.info(f'"{task}" has been added')

    def search(self, task):
        self.cur.execute("SELECT * FROM Todolist WHERE task=:task", {"task": task})
        return self.cur.fetchall()

    def delete(self, id):
        self.cur.execute("DELETE FROM todolist WHERE id=:id", {"id": id})
        self.con.commit()

    def __del__(self):
        self.con.close()
