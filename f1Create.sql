USE F1;

CREATE TABLE Circuit (
circuitId INT PRIMARY KEY,
name VARCHAR(100),
alt FLOAT,
lng FLOAT,
lat FLOAT,
country VARCHAR(50),
location VARCHAR(50)
);

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

CREATE TABLE Constructor (
constructorId INT PRIMARY KEY,
name VARCHAR(50),
nationality VARCHAR(50)
);

CREATE TABLE Drivers (
driverId INT PRIMARY KEY,
forename VARCHAR(50),
surname VARCHAR(50),
dob DATE,
nationality VARCHAR(50)
);

CREATE TABLE Driver_Standings (
points INT,
position INT,
wins INT,
driverId INT,
raceId INT,
FOREIGN KEY (driverId) REFERENCES Drivers(driverId),
FOREIGN KEY (raceId) REFERENCES Races(raceId)
);

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

CREATE TABLE Constructor_Standing (
constructorStandingsId INT PRIMARY KEY,
points INT,
wins INT,
constructorId INT,
raceId INT,
FOREIGN KEY (raceId) REFERENCES Races(raceId),
FOREIGN KEY (constructorId) REFERENCES Constructor(constructorId)
);

CREATE TABLE Constructor_Results (
constructorResultsId INT,
points INT,
constructorId INT,
raceId INT,
FOREIGN KEY (raceId) REFERENCES Races(raceId),
FOREIGN KEY (constructorId) REFERENCES Constructor(constructorId),
);

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