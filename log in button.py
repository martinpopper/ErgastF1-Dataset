import customtkinter as ct
import subprocess as sp
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk
import pyodbc as py
import pandas as pd

'''
Line 126 need to make it so that it connects to the local datbase on your computer, 
need to run the f1_database_creation file first to have the populated database, then you can run the 
sample queires in this interface. But ensure that you pip install all of the imports above. 

pip install customtkinter
pip install subprocess
pip install tkinter

pyodbc and pandas were installed while running the last file
'''


# set the apperance to the users 
# -------------------------------------------------------------------------------------------------
ct.set_appearance_mode("system")
ct.set_default_color_theme("dark-blue")
# -------------------------------------------------------------------------------------------------
global sqlCodeValid, text_box, result_label, conn, treeview_frame, tree
sqlCodeValid = False
text_box = None
result_label = None
treeview_frame = None
tree = None


invalid_keywords = ['create', 'update', 'table', 'alter', 'add', 'insert', 'into', 'values', 'drop', 
                    'delete', 'update', 'index', 'view', 'set', 'trigger']
valid_keywords = ['select', 'from', 'group by', 'where', 'order by', 'asc', 'desc', 'having', 'as', 
                 'count', 'max', 'min', 'join', 'inner join', 'outer join', 'on', 'left outer join', 
                 'right outer join', 'limit']

# create the sql interface
# -------------------------------------------------------------------------------------------------  
def theinterface():
    global sqlCodeValid, text_box, result_label, interface
    interface = ct.CTk()
    interface.geometry("700x700")
    # labels at the top
    label = ct.CTkLabel(master=interface, text="Welcome to the database!")
    label2 = ct.CTkLabel(master=interface, text="Please enter your SQL queries below:")
    label.pack(pady=12, padx=10)
    label2.pack(pady=12, padx=10)
    # textbox that the sql codes go in to
    text_box = ct.CTkTextbox(master=interface, height=180, width=500)
    text_box.pack(pady=12, padx=10)
    #run button in the top right corner
    run_button = ct.CTkButton(master=interface, text="Run Code", command=run)
    run_button.pack(pady=12, padx=10)
    run_button.place(relx=1.0, y=0, anchor="ne")
    
    # label for displaying the result of the SQL query if it is executed properly
    if sqlCodeValid:
        result_label = ct.CTkLabel(master=interface, text="", text_color="black")
        result_label.pack(pady=12, padx=10)
    else:
        result_label = ct.CTkLabel(master=interface, text="", text_color="black")
        result_label.pack(pady=12, padx=10)
    interface.mainloop()
# -------------------------------------------------------------------------------------------------

def display_dataframe(df):
    global interface
    global treeview_frame
    global tree
    
    # Clear existing Treeview widget
    if tree is not None:
        tree.delete(*tree.get_children())

    # Create the Treeview widget if it doesn't exist
    if tree is None:
        treeview_frame = ct.CTkFrame(master=interface)
        treeview_frame.pack(pady=12, padx=10)

        tree = ttk.Treeview(master=treeview_frame, show='headings', selectmode='browse')
        tree.pack(side="left", fill="both", expand=True)

    # Set columns and headings
    columns = list(df.columns)
    if columns != tree["columns"]:
        tree["columns"] = columns
        for col in columns:
            tree.column(col, width=100, minwidth=50)
            tree.heading(col, text=col)

    # Add rows to the Treeview widget
    for i, row in df.iterrows():
        tree.insert("", i, values=list(row))




# define the run command
# -------------------------------------------------------------------------------------------------
def run():
    global sqlCodeValid, text_box, result_label
    input = text_box.get("1.0", "end-1c").replace("\n", " ")
    words = input.split() # split the string into a list of words
    sql_query = " ".join(words) # join the words back by a space so its easy for sql to understand
    sql_query = sql_query.lower()
    if words[0].lower() in valid_keywords:
        sqlCodeValid = True
        result_valid = "Your SQL code has been executed successfully!"
        result_label.configure(text=result_valid)
        dataframe = pd.read_sql(sql_query, conn)
        display_dataframe(dataframe)
    else: 
        sqlCodeValid = False
        result_invalid = "Error in SQL code, please try again."
        result_label.configure(text=result_invalid)
# -------------------------------------------------------------------------------------------------


# Code for when the user logs in to the interface
# -------------------------------------------------------------------------------------------------
def login():
    global conn
    # Define the correct username and password
    correct_username = "admin"
    correct_password = "1234"

    # Get the entered username and password from the entry widgets
    username = entry1.get()
    password = entry2.get()

    # Check if the entered username and password are correct
    if username == correct_username and password == correct_password:
        # close the log in 
        try:
            # connecting to my own database server at home
            server = "192.168.100.11,32768" # change to your own computers database server
            database = "f1"
            username = "sa" # username and password for your database server
            password = "On3cl!ck_23" # password for your database server
            driver = "{ODBC Driver 18 for SQL Server}" # please change to your own driver
            # the connection 
            conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes;')
        except py.Error as e: 
            print("error in connecting to the database")
        loginInterface.destroy()
        # open the interface
        theinterface()
    else:
        # If the entered username and password are incorrect, show an error message
        error = ct.CTkLabel(master = frame, text = "Incorrect username or password", text_color = "red")
        error.pack(pady =12, padx = 10)
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
# -------------------------------------------------------------------------------------------------


# create the login interface, the thing that holds the widget
# -------------------------------------------------------------------------------------------------
loginInterface = ct.CTk()
loginInterface.geometry("500x360")
# the entire widget box
frame = ct.CTkFrame(master = loginInterface)
frame.pack(pady=20,padx=60, fill ="both", expand =True)
# main label above the username and passowrd
label = ct.CTkLabel(master=frame, text="Formula 1 Database Login System")
label.pack(pady=12, padx=10)
# username entry
entry1 = ct.CTkEntry(master =frame, placeholder_text="Username")
entry1.pack(pady=12,padx=10)
# password user entry
entry2 = ct.CTkEntry(master =frame, placeholder_text="Password", show ="*")
entry2.pack(pady=12,padx=10)
# create the log in button, uses the function login from above
button = ct.CTkButton(master = frame, text = "Login", command =login)
button.pack(pady=12, padx=10)
loginInterface.bind('<Return>', lambda event: button.invoke()) 
# the line above allows for the return key to be used to log in as well.
# remeber me box that has the checking functionality
checkbox = ct.CTkCheckBox(master = frame, text = "Remember Me")
checkbox.pack(pady =12, padx = 10)   
loginInterface.mainloop()
# -------------------------------------------------------------------------------------------------