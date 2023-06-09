# Formula 1 Dataset - README

## Contributions
- [Martin Popper](https://github.com/martinpopper)
- [Owen Ostermann](https://github.com/oostermann10)
- [Christian Trites](https://github.com/ChristianTrites)
- [Filip Karamanov](https://github.com/FilipKaramanov)

This dataset includes information on Formula 1 races, drivers, teams, and results. In order to use this dataset in a Python script, please follow the instructions below:
## Prerequisites
There are a couple packages you will need to install in order to run. To install each one, open your command terminal, and copy each command in.

pandas: a library for data manipulation and analysis, particularly for working with tabular data.
- `pip install pandas`
  
pyodbc: a library for connecting to and querying databases using the Open Database Connectivity (ODBC) API.
- `pip install pyodbc`
  
traceback: a module for formatting and printing Python stack traces, which can be used for debugging.
- `pip install traceback`

numpy: a library for numerical computing in Python, particularly for working with arrays and matrices.
- `pip install numpy`

time: a module for working with time and dates in Python, including measuring elapsed time and formatting time values.
- `pip install time`

itertools: a module for creating and manipulating iterators, which are objects that can be iterated (looped) over, such as lists or arrays.
- `pip install itertools`

threading: a module for creating and managing threads in Python, which can be used for concurrent programming. 
- `pip install threading`

customtikinter: a custom-made module that extends or modifies the functionality of the built-in "tkinter" GUI toolkit in Python.
- `pip install customtkinter`
- `pip install tkinter`

subprocess: a module that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
- `pip install subprocess`

## Instructions
### Editing the f1_database_creation.py file

1. On line 54 of the script, replace '/Users/owenostermann/Desktop/COMP 3380/Project/f1db_csv/' with the path name of where the CSV files folder is stored on your own computer. Leave the `(+name+'.csv')` in place, as it will allow all of the CSV files to be read in from the f1db_csv folder.

2. Connect to the local database server on your computer in your terminal or in your database managment system and run the SQL command 
   - `CREATE DATABASE f1;`
so that you have an empty database named f1 on your server. This allows for the python file to connect to that datbase on your server through the connection string and create tables and populate those tables.
   
3. On line 397 of the script, replace (server = "192.168.100.11,32768") with your own database server name where you created the f1 database. Enter your username and password for your local database server on your own device. If you do not have a database username and password, remove this from the connection string in line 388.
   `(conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes;'))`
   should be changed to the following if no username and password:
   `(conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;TrustServerCertificate=yes;'))`
Be sure to change the driver name to the driver that you are using on your own computer.

4. Once all the steps are complete, you can run the py file and you will have the database locally populated from the csv files. 
   
   the script should create the tables in the f1 database on your computers database server where you specified the connection string. The tables will be populated now and you can run the interface to get the output from the SQL queries. Based on the large amount of data, the f1_database_creation.py may take a bit of time to execute depending on the abilities of your computer. But in the terminal when you run the file there is an animation that tells you the status of the insertion and populating of the tables. Just watch the animation and it will tell you when it is complete. Once it says "successfully closed to the database" the process is complete.

### Editing the log in button.py file
1. On line 140 in the interface file (log in button.py) the GUI needs to connect to the database in order to execute the SQL statements. You will need to do as above in step 3. You need to connect to your local server and use your serves username and password (if it has one) and chnage the driver. Once this is modfied in the code, the interface can be run.

## Running the program
1. Run `log in button.py`
2. Log in to the database with username: `admin` and password: `1234`
3. Copy and paste queries from `samples.sql` into the text box. Once you copy and paste a query into the run box, copy the next query in its place and hit the run button to get the next queries output.
4. Try some commands like `CREATE TABLE newTable;` or `DELETE TABLE Circuit;`. The interface will not let you execute these commands. As an analyst you do not have the ability to chnage the structure of the database, you only are able to get information from the database.
5. Keep repeating this process until you are satisfied. 
