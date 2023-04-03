# Formula 1 Dataset - README

This dataset includes information on Formula 1 races, drivers, teams, and results. In order to use this dataset in a Python script, please follow the instructions below:

## Instructions

1. On line 54 of the script, replace '/Users/owenostermann/Desktop/COMP 3380/Project/f1db_csv/' with the path name of where the CSV files folder is stored on your own computer. Leave the `(+name+'.csv')` in place, as it will allow all of the CSV files to be read in from the f1db_csv folder.

2. Ensure that you have all of the required packages installed on your local machine by running the following commands in your terminal:
- `pip install pandas`
- `pip install pyodbc`
- `pip install traceback`
- `pip install numpy`
- `pip install time`
- `pip install itertools`
- `pip install threading`

3. Connect to the database in your terminal and run the SQL command `CREATE DATABASE f1;`
4. On line 397 of the script, replace (server = "192.168.100.11,32768") with your own database server name where you created the f1 database. Enter your username and password for your local database server on your own device. If you do not have a database username and password, remove this from the connection string in line 388.
   `(conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes;'))`
   should be changed to the following if no username and password:
   `(conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;TrustServerCertificate=yes;'))`
Be sure to change the driver name to the driver that you are using on your own computer.

5. Once all the steps are complete, the script should create the database on your computer where you specified the connection. The files will be populated now and you can run the interface to get the output from the SQL queries.

## Contributions
- [Martin Popper](https://github.com/martinpopper)
- [Owen Ostermann](https://github.com/oostermann10)
- [Christian Trites](https://github.com/ChristianTrites)
- Filip Karamanov
