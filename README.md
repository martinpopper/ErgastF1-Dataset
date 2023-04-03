# Formula 1 Dataset - README

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


## Instructions
### Editing the f1_database_creation.py file

1. On line 54 of the script, replace '/Users/owenostermann/Desktop/COMP 3380/Project/f1db_csv/' with the path name of where the CSV files folder is stored on your own computer. Leave the `(+name+'.csv')` in place, as it will allow all of the CSV files to be read in from the f1db_csv folder.


2. Connect to the database in your terminal and run the SQL command `CREATE DATABASE f1;`
   
3. On line 397 of the script, replace (server = "192.168.100.11,32768") with your own database server name where you created the f1 database. Enter your username and password for your local database server on your own device. If you do not have a database username and password, remove this from the connection string in line 388.
   `(conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes;'))`
   should be changed to the following if no username and password:
   `(conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;TrustServerCertificate=yes;'))`
Be sure to change the driver name to the driver that you are using on your own computer.

4. Once all the steps are complete, the script should create the database on your computer where you specified the connection. The files will be populated now and you can run the interface to get the output from the SQL queries.

## Contributions
- [Martin Popper](https://github.com/martinpopper)
- [Owen Ostermann](https://github.com/oostermann10)
- [Christian Trites](https://github.com/ChristianTrites)
- [Filip Karamanov](https://github.com/FilipKaramanov)
