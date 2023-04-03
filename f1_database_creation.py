import pandas as pd
import pyodbc as py
import traceback
import numpy as np
from itertools import cycle
from time import sleep
import threading


# things to note before running the file
'''
1. Line 54: Chnage to the path name of where the csv files folder is stored on your own 
   computer. For example replace '/Users/owenostermann/Desktop/COMP 3380/Project/f1db_csv/'
   with '/your path name here/f1db_csv'. Please leave the (+name+'.csv') as this will allow 
   for all of the csv files to be read in from the f1db_csv folder. 
2. Make sure you have all of the packages isntalled on your computer locally. If you dont have
   one of those please copy and run this in your terminal before running the file. 
   ------------------
   pip install pandas 
   pip install pyodbc 
   pip install traceback
   pip install numpy
   pip install time
   pip install itertools
   pip install threading
   ------------------
3. Please make sure that you connect to database in terminal before running the file and running the SQL
   command (CREATE DATABASE f1;)
4. Once that is complete, then on line 397 please change (server = "192.168.100.11,32768") 
   to your own databases server name where you created the f1 database. Please input
   your username and password for ypur local database server on your own device. If you do not have 
   a database username and password please remove this from the connection string in line 388.
   (conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes;'))
   should chnage to the following if no username and password
   (conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;TrustServerCertificate=yes;'))
   Please chnage the driver name to the driver that you are using on your own computer. 
5. Once all the steps are complete, then the file should work and create the database on your computer where 
   you gave the connection (could be localhost or wherever your database server is on your computer).
   The files will be populated now and you can run the interface to get the output from the sql queries. 
'''

# STEP1: READING IN THE DATA INTO PANDAS DATAFRAMES
#---------------------------------------------------------------------------------------
# names of the csv files
names = ['Circuit', 'Constructor_Results', 'Constructor_Standing',
         'Constructor', 'Driver_Standings', 'Drivers', 
         'Pitstop', 'Qualify', 'Races', 'Results']

# to store the data
data = {}

# loop to read in the data
for name in names: 
    filename = '/Users/owenostermann/Desktop/COMP 3380/Project/f1db_csv/'+name+'.csv'
    # please chnage to path name of where the f1db_csv folder is located on your computer
    data[name] = pd.read_csv(filename)
#---------------------------------------------------------------------------------------

# STEP2: DATA CLEANING AND PREPERATION FOR SQL CONVERSION
#---------------------------------------------------------------------------------------
# CIRCUIT DATAFRAME 
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Circuit = data['Circuit']
# drop the columns that we dont need when creating the sql database
Circuit = Circuit.drop(columns=['circuitRef', 'url'])
# set the Na values in altidute to 0
Circuit.loc[Circuit['alt'] == '\\N', 'alt'] = '0'
# convert the alt into the proper data type
Circuit['alt'] = Circuit['alt'].astype(float)
# now we have the proper datatypes for each column
'''
circuitId      int64
name          object
location      object
country       object
lat          float64
lng          float64
alt          float64
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# CONSTRUCTOR RESULTS DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Constructor_Results = data['Constructor_Results']
# drop the columns that we dont need
Constructor_Results = Constructor_Results.drop(columns=['status'])
# convert points to int 
Constructor_Results['points'] = Constructor_Results['points'].astype(int)
# now we have the proper datatypes of each column 
'''
raceId           int64
constructorId    int64
points           int64
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# CONSTRUCTOR DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Constructor = data['Constructor']
# drop the columns that we dont need when creating the sql database
Constructor = Constructor.drop(columns=['constructorRef', 'url'])
# now we have the proper datatypes for each column
'''
constructorId     int64
name             object
nationality      object
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# DRIVERS DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Drivers = data['Drivers']
# drop the columns that we dont need when creating the sql database 
Drivers = Drivers.drop(columns=['number', 'code', 'url', 'driverRef'])
# update the date of birth column to a date datatype 
Drivers['dob'] = pd.to_datetime(Drivers['dob'], format = '%Y-%m-%d')
# now we have the proper datatypes for each column 
'''
driverId                int64
forename               object
surname                object
dob            datetime64[ns]
nationality            object
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# DRIVER STANDINGS DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Driver_Standings = data['Driver_Standings']
# drop the columns that we dont need when creating the sql database
Driver_Standings = Driver_Standings.drop(columns=['driverStandingsId', 'positionText'])
# Convert points to int as it is in the form of float when reading in 
Driver_Standings['points'] = Driver_Standings['points'].astype(int)
# now we have the proper datatypes for each column
'''
raceId      int64
driverId    int64
points      int64
position    int64
wins        int64
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# RESULTS DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Results = data['Results']
# drop the columns that we dont need when creating the sql database
Results = Results.drop(columns=['number', 'positionText', 'statusId','time',
                                'fastestLap','rank'])
# convert to proper datatypes for sql database 
Results['points'] = Results['points'].astype(int)
Results.loc[Results['position'] == '\\N', 'position'] = '0'
Results['position'] = Results['position'].astype(int)
Results.loc[Results['milliseconds'] == '\\N', 'milliseconds'] = '0'
Results['milliseconds'] = Results['milliseconds'].astype(int)
Results.loc[Results['fastestLapSpeed'] == '\\N', 'fastestLapSpeed'] = '0'
Results['fastestLapSpeed'] = Results['fastestLapSpeed'].astype(float)
Results.loc[Results['fastestLapTime'] == '\\N', 'fastestLapTime'] = '0:00.000'
Results['fastestLapTime'] = pd.to_datetime(Results['fastestLapTime'], format = '%H:%S.%f')
# now we have the proper datatypes for each column
'''
resultId             int64
raceId               int64
driverId             int64
constructorId        int64
grid                 int64
position             int64
points               int64
laps                 int64
milliseconds         int64
fastestLapTime      datetime64[ns]
fastestLapSpeed    float64
positionOrder        int64
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# QUALIFY DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Qualify = data['Qualify']
# convert to proper datatypes for sql database
Qualify.loc[Qualify['q1'] == '\\N', 'q1'] = '0:00.000'
Qualify.loc[Qualify['q2'] == '\\N', 'q2'] = '0:00.000'
Qualify.loc[Qualify['q3'] == '\\N', 'q3'] = '0:00.000'
Qualify['q1'] = pd.to_datetime(Qualify['q1'], format = '%H:%S.%f')
Qualify['q2'] = pd.to_datetime(Qualify['q2'], format = '%H:%S.%f')
Qualify['q3'] = pd.to_datetime(Qualify['q3'], format = '%H:%S.%f')
# now we have the proper datatypes for each column
'''
qualifyId                 int64
raceId                    int64
driverId                  int64
constructorId             int64
number                    int64
position                  int64
q1               datetime64[ns]
q2               datetime64[ns]
q3               datetime64[ns]
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# CONSTRUCTOR STANDINGS DATAFRAME 
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Constructor_Standing = data['Constructor_Standing']
# drop the columns that we dont need when creating the sql database
Constructor_Standing = Constructor_Standing.drop(columns=['position', 'positionText'])
# convert to proper datatypes for sql database
Constructor_Standing['points'] = Constructor_Standing['points'].astype(int)
# now we have the proper datatypes for each column
'''
constructorStandingsId    int64
raceId                    int64
constructorId             int64
points                    int64
wins                      int64
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# CONSTRUCTOR RESULTS DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Races = data['Races']
# drop the columns that we dont need when creating thr sql database
Races = Races.drop(columns=['url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time',
                            'fp3_date', 'fp3_time', 'quali_date', 'quali_time',
                            'sprint_date', 'sprint_time'])
# convert to proper datatypes for sql database
Races['date'] = pd.to_datetime(Races['date'], format = '%Y-%m-%d')
Races.loc[Races['time'] == '\\N', 'time'] = '0:00:000'
Races['time'] = pd.to_datetime(Races['time'], format = '%H:%S:%f')
Races['time'] = Races['time'].dt.time
# now we have the proper datatypes for each column
'''
raceId                int64
year                  int64
round                 int64
circuitId             int64
name                 object
date         datetime64[ns]
time         datetime64[ns]
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# PITSTOP DATAFRAME
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Pitstop = data['Pitstop']
# drop the columns that we dont need when creating the sql database
Pitstop = Pitstop.drop(columns=['duration'])
# convert to proper datatypes fro sql database
Pitstop['time'] = pd.to_datetime(Pitstop['time'], format='%H:%S:%f')
# Pitstop['time'] = Pitstop['time'].dt.time for sql tmr check
# now we have the proper datatypes for each column
'''
raceId                   int64
driverId                 int64
stop                     int64
lap                      int64
time            datetime64[ns]
milliseconds             int64
'''
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#---------------------------------------------------------------------------------------

# STEP3: CREATING THE SQL TABLE STRINGS FOR THE DATABASE
#---------------------------------------------------------------------------------------
Circuit_Sql = """
CREATE TABLE Circuit (
circuitId INT PRIMARY KEY,
name VARCHAR(100),
alt FLOAT,
lng FLOAT,
lat FLOAT,
country VARCHAR(50),
location VARCHAR(50)
);
"""

Races_Sql = """
CREATE TABLE Races (
raceId INT PRIMARY KEY,
year INT,
time TIME,
round INT,
date DATE,
name VARCHAR(100),
circuitId INT,
FOREIGN KEY (circuitId) REFERENCES Circuit(circuitId)
);
"""

Constructor_Sql = """
CREATE TABLE Constructor (
constructorId INT PRIMARY KEY,
name VARCHAR(50),
nationality VARCHAR(50)
);
"""

Drivers_Sql = """
CREATE TABLE Drivers (
driverId INT PRIMARY KEY,
forename VARCHAR(50),
surname VARCHAR(50),
dob DATE,
nationality VARCHAR(50)
);
"""

Driver_Standings_Sql = """
CREATE TABLE Driver_Standings (
points INT,
position INT,
wins INT,
driverId INT,
raceId INT,
FOREIGN KEY (driverId) REFERENCES Drivers(driverId),
FOREIGN KEY (raceId) REFERENCES Races(raceId)
);
"""

Results_Sql = """
CREATE TABLE Results (
resultId INT PRIMARY KEY,
position INT,
positionOrder INT,
points INT,
grid INT,
fastestLapSpeed FLOAT,
fastestLapTime TIME,
milliseconds INT,
raceId INT,
driverId INT,
constructorId INT,
laps INT,
FOREIGN KEY(raceId) REFERENCES Races(raceId),
FOREIGN KEY(driverId) REFERENCES Drivers(driverId),
FOREIGN KEY (constructorId) REFERENCES Constructor(constructorId)
);
"""

Qualify_Sql = """
CREATE TABLE Qualify (
qualifyId INT PRIMARY KEY,
constructorId INT,
driverId INT,
raceId INT,
position INT,
number INT,
q1 TIME,
q2 TIME,
q3 TIME,
FOREIGN KEY (constructorId) REFERENCES Constructor(constructorId),
FOREIGN KEY (driverId) REFERENCES Drivers(driverId),
FOREIGN KEY (raceId) REFERENCES Races(raceId),
);
"""

Constructor_Standing_Sql = """
CREATE TABLE Constructor_Standing (
constructorStandingsId INT PRIMARY KEY,
points INT,
wins INT,
constructorId INT,
raceId INT,
FOREIGN KEY (raceId) REFERENCES Races(raceId),
FOREIGN KEY (constructorId) REFERENCES Constructor(constructorId)
);
"""

Constructor_Results_Sql = """
CREATE TABLE Constructor_Results (
constructorResultsId INT,
points INT,
constructorId INT,
raceId INT,
FOREIGN KEY (raceId) REFERENCES Races(raceId),
FOREIGN KEY (constructorId) REFERENCES Constructor(constructorId),
);
"""

Pitstop_Sql = """
CREATE TABLE Pitstop (
raceId INT,
stop INT,
lap INT,
time TIME,
driverId INT,
milliseconds INT,
FOREIGN KEY (driverId) REFERENCES Drivers(driverId),
FOREIGN KEY (raceId) REFERENCES Races(raceId)
);
"""
#---------------------------------------------------------------------------------------

# STEP4: CONNECTING TO THE DATABASE
#---------------------------------------------------------------------------------------
try:
    # connecting to my own database server at home
    server = "192.168.100.11,32768" # change to your own computers database server
    database = "f1"
    username = "sa" # username and password for your database server
    password = "On3cl!ck_23" # password for your database server
    driver = "{ODBC Driver 18 for SQL Server}" # please change to your own driver
    # the connection 
    conn = py.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes;')
    print("successfully connected to the database")
except py.Error as e: 
    print("error in connecting to the database")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#---------------------------------------------------------------------------------------

# STEP5: CREATING THE TABLES IN SQL
#---------------------------------------------------------------------------------------
try: 
    conn.execute(Circuit_Sql)
    conn.execute(Races_Sql)
    conn.execute(Constructor_Sql)
    conn.execute(Drivers_Sql)
    conn.execute(Driver_Standings_Sql)
    conn.execute(Results_Sql)
    conn.execute(Qualify_Sql)
    conn.execute(Constructor_Results_Sql)
    conn.execute(Constructor_Standing_Sql)
    conn.execute(Pitstop_Sql)
    print("tables created successfully")
except py.Error as e:
    print("error in table creation")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#---------------------------------------------------------------------------------------

# STEP6: INSERTING THE DATA INTO THE TABLES
# ------------------------------------------------------------------------------
def display_loading_animation(message, ev):
    n_points = 6
    points_l = ['.' * i + ' ' * (n_points - i) + '\r' for i in range(n_points)]
    while not ev.is_set():
        for points in cycle(points_l):
            if ev.is_set():
                break
            print(message + points, end='')
            sleep(0.3)
    print(message + ' ' * n_points + '\r')


# Circut Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try:
    ev1 = threading.Event()
    t1 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Circuit table ", ev1))
    t1.start()
    
    insert_Circut = """
    INSERT INTO Circuit 
    (circuitId, name, location, country, lat, lng, alt)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """    
    Circut_cursor = conn.cursor()
    for index, row in Circuit.iterrows():
        Circut_cursor.execute(insert_Circut, 
                            (row['circuitId'],row['name'], row['location'],
                            row['country'], row['lat'], row['lng'], row['alt']))
    ev1.set()  # stop the animation
    t1.join()
    print("Circuit table insertion complete")
    
except py.Error as e:
    print("error inserting into Circuit table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Races Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try:
    ev2 = threading.Event()
    t2 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Races table ", ev2))
    t2.start()
    
    insert_Races = """
    INSERT INTO Races 
    (raceId, circuitId, name, date, year, time, round)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    Races_cursor = conn.cursor()
    for index, row in Races.iterrows():
        Races_cursor.execute(insert_Races, 
                            (row['raceId'], row['circuitId'], row['name'], 
                            row['date'], row['year'], row['time'], row['round']))
    ev2.set()  # stop the animation
    t2.join()
    print("Races table insertion complete")
    
    
except py.Error as e:
    print("error inserting into Races table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# Constructor Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try:
    ev3 = threading.Event()
    t3 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Constructor table ", ev3))
    t3.start()
    
    insert_Constructor = """
    INSERT INTO Constructor 
    (constructorID, name, nationality)
    VALUES (?, ?, ?);
    """
    Constructor_cursor = conn.cursor()
    for index, row in Constructor.iterrows():
        Constructor_cursor.execute(insert_Constructor, (row['constructorId'],
                                                        row['name'], row['nationality']))
    ev3.set()  # stop the animation
    t3.join()
    print("Constructor table insertion complete")
    
except py.Error as e:
    print("error inserting into Constructor table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Drivers Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
try: 
    ev4 = threading.Event()
    t4 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Drivers table ", ev4))
    t4.start()

    insert_Drivers = """
    INSERT INTO Drivers
    (driverId, forename, surname, dob, nationality)
    VALUES (?, ?, ?, ?, ?);
    """
    Drivers_cursor = conn.cursor()
    for index, row in Drivers.iterrows():
        Drivers_cursor.execute(insert_Drivers, (row['driverId'], row['forename'], 
                                                row['surname'], row['dob'], row['nationality']))
    ev4.set()  # stop the animation
    t4.join()
    print("Drivers table insertion complete")

except py.Error as e:
    print("error inserting into Drivers table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

# Driver Standings Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
try:
    ev5 = threading.Event()
    t5 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Driver Standings table ", ev5))
    t5.start()

    insert_Driver_Standings = """
    INSERT INTO Driver_Standings
    (driverId, raceId, position, points, wins)
    VALUES (?, ?, ?, ?, ?);
    """
    Driver_Standings_cursor = conn.cursor()
    # create a list of tuples containing the parameter values for each row
    rows = [(int(row['driverId']), int(row['raceId']), int(row['position']),
             int(row['points']), int(row['wins'])) for index, row in Driver_Standings.iterrows()]
    # execute the INSERT statement for all rows using executemany()
    Driver_Standings_cursor.executemany(insert_Driver_Standings, rows)    
    ev5.set()  # stop the animation
    t5.join()
    print("Driver Standings table insertion complete")


except py.Error as e:
    print("error inserting into Driver Standings table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Results Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try: 
    ev6 = threading.Event()
    t6 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Results table ", ev6))
    t6.start()

    insert_Results = """
    INSERT INTO Results
    (resultId, raceId, driverId, constructorId, position, positionOrder,
    points, grid, fastestLapSpeed, fastestLapTime, milliseconds, laps)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    Results_cursor = conn.cursor()
    rows_to_insert = [(row['resultId'], row['raceId'], row['driverId'], row['constructorId'], 
                       row['position'], row['positionOrder'], row['points'], row['grid'], 
                       row['fastestLapSpeed'], row['fastestLapTime'], row['milliseconds'], 
                       row['laps']) for index, row in Results.iterrows()]
    Results_cursor.executemany(insert_Results, rows_to_insert)
    ev6.set()  # stop the animation
    t6.join()
    print("Results table insertion complete")

except py.Error as e:
    conn.rollback()
    print("error inserting into Results table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Qualify Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try:
    ev7 = threading.Event()
    t7 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Qualify table ", ev7))
    t7.start()

    insert_Qualify = """
    INSERT INTO Qualify
    (qualifyId, constructorId, driverId, raceId, position, number, q1, q2, q3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    Qualify_cursor = conn.cursor()
    rows_to_insert = [(row['qualifyId'], row['constructorId'], row['driverId'], row['raceId'],
                       row['position'], row['number'], row['q1'], 
                       row['q2'], row['q3']) for index, row in Qualify.iterrows()]
    Qualify_cursor.executemany(insert_Qualify, rows_to_insert)
    ev7.set()  # stop the animation
    t7.join()
    print("Qualify table insertion complete")

except py.Error as e:
    conn.rollback()
    print("error inserting into Qualify table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

# Contructor Standings Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try:
    ev8 = threading.Event()
    t8 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Constructor Standings table ", ev8))
    t8.start()

    insert_Constructor_Standing = """
    INSERT INTO Constructor_Standing 
    (constructorStandingsId, constructorId, raceId, wins, points)
    VALUES (?, ?, ?, ?, ?);
    """
    Constructor_Standing_cursor = conn.cursor()
    data = [(int(row['constructorStandingsId']), int(row['constructorId']), 
             int(row['raceId']), int(row['wins']), int(row['points'])) 
            for index, row in Constructor_Standing.iterrows()]
    Constructor_Standing_cursor.executemany(insert_Constructor_Standing, data)
    ev8.set()  # stop the animation
    t8.join()
    print("Constructor Standing table insertion complete")

except py.Error as e:
    conn.rollback()
    print("error inserting into Constructor Standings table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Constructor Results Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try: 
    ev9 = threading.Event()
    t9 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Constructor Results table ", ev9))
    t9.start()

    insert_Constructor_Results = """
    INSERT INTO Constructor_Results
    (constructorResultsId, constructorId, raceId, points)
    VALUES (?, ?, ?, ?);
    """
    Constructor_Results_cursor = conn.cursor()
    data = [(int(row['constructorResultsId']), int(row['constructorId']), 
             int(row['raceId']), int(row['points'])) 
            for index, row in Constructor_Results.iterrows()]
    Constructor_Results_cursor.executemany(insert_Constructor_Results, data)
    ev9.set()  # stop the animation
    t9.join()
    print("Constructor Results table insertion complete")

except py.Error as e:
    conn.rollback()
    print("error inserting into Constructor Results table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Pitstop Table Insert
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
try:
    ev10 = threading.Event()
    t10 = threading.Thread(target=display_loading_animation, 
                         args=("Inserting into the Pitstop table ", ev10))
    t10.start()

    insert_Pitstop = """
    INSERT INTO Pitstop
    (raceId, driverId, lap, stop, time, milliseconds)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    Pitstop_cursor = conn.cursor()
    rows_to_insert = [(row['raceId'], row['driverId'], row['lap'], 
                       row['stop'], row['time'], 
                       row['milliseconds']) for index, row in Pitstop.iterrows()]
    Pitstop_cursor.executemany(insert_Pitstop, rows_to_insert)
    ev10.set()  # stop the animation
    t10.join()
    print("Pitstop table insertion completed")

except py.Error as e:
    conn.rollback()
    print("error inserting into Pitstop table")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# ------------------------------------------------------------------------------

# STEP7: COMMIT TO DATABASE CHANGES
# ------------------------------------------------------------------------------
try:
    conn.commit()
    print("successfully committed to the database changes")
except py.Error as e:
    print("error in committing to the database changes")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
# ------------------------------------------------------------------------------


# STEP8: CLOSE THE DATABASE CONNECTION 
# ------------------------------------------------------------------------------
try:
    conn.close()
    print("successfully closed to the database")
except py.Error as e:
    print("error in closing the database")
    print(str(e))
    print("Stack trace:")
    print(traceback.format_exc())
# ------------------------------------------------------------------------------

# THE DATABASE IS NOW POPULATED AND IT IS READY TO BE USED WITH THE INTERFACE
