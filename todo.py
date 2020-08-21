from tkinter import *
from tkinter.ttk import *
from backend import Database
import logging
import webbrowser

database = Database("to-do-list.db")
logging.basicConfig(filename="data/task.log", level=logging.INFO,
                    format="%(levelname)s:%(asctime)s:%(message)s")

row = 0


def get_selected_row(event):  # for each click event passes to function
    try:
        global row
        index = list1.curselection()[0]
        row = list1.get(index)
    except IndexError:
        pass


def view_command():
    list1.delete(0, END)
    for task in database.view():
        list1.insert(END, task)


def add_command():
    if e1_value.get().strip() == "":
        return None
    database.add(e1_value.get())
    list1.delete(0, END)
    list1.insert(END, e1_value.get())
    e1.delete(0, END)


def enter(event):  # for each click event passes to function
    add_command()


def done():
    try:
        search = database.search(row[1])
        if search:
            logging.info(f'"{row[1]}", has been done!')
            database.delete(row[0])
            view_command()
    except TypeError:
        pass


def log():
    new_window = Toplevel(window)
    new_window.title("LOG")
    text = Text(new_window)
    text.pack()
    with open("data/task.log") as logfile:
        content = logfile.read()
    text.delete("1.0", END)
    text.insert(END, content)


def about():
    url = "https://github.com/RezaRjbi"
    webbrowser.open_new_tab(url=url)


window = Tk(className="To-Do list")

label1 = Label(window, text="Task")
label1.grid(row=0, column=0)

e1_value = StringVar()
e1 = Entry(window, textvariable=e1_value)
e1.grid(row=0, column=1)

label2 = Label(window)
label2.grid(row=1)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=2, column=0, columnspan=2, rowspan=6)

scrollbar = Scrollbar(window)
scrollbar.grid(row=2, rowspan=6, column=2)

list1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=list1.yview)

list1.bind("<<ListboxSelect>>", get_selected_row)

b1 = Button(window, text="View List", width=12, command=view_command)
b1.grid(row=1, column=3)

b2 = Button(window, text="Add Task", width=12, command=add_command)
b2.grid(row=2, column=3)

b3 = Button(window, text="Done", width=12, command=done)
b3.grid(row=3, column=3)

b4 = Button(window, text="log", width=12, command=log)
b4.grid(row=4, column=3)

b5 = Button(window, text="About", width=12, command=about)
b5.grid(row=5, column=3)

window.bind("<Return>", enter)

mainloop()
