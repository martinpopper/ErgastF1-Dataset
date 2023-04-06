
-- Select the number of wins for each driver and order them by the number of wins:
SELECT Drivers.surname, Drivers.forename, COUNT(Driver_Standings.wins) as wins
FROM Drivers
JOIN Driver_Standings ON Drivers.driverId = Driver_Standings.driverId
GROUP BY Drivers.surname, Drivers.forename
ORDER BY wins DESC;

-- Select the results of the race with id 200 and order them by the position of the drivers:
SELECT Results.position, Drivers.surname, Drivers.forename, Constructor.name as 
constructor_name, Drivers.driverId, Drivers.nationality
FROM Results 
JOIN Drivers ON Results.driverId = Drivers.driverId 
JOIN Constructor ON Results.constructorId = Constructor.constructorId 
WHERE Results.raceId = 200 
ORDER BY Results.position;

-- Select the number of races held in each country and order them by the number of races:
SELECT Circuit.country, COUNT(Races.raceId) as num_races 
FROM Races 
JOIN Circuit ON Races.circuitId = Circuit.circuitId 
GROUP BY Circuit.country 
ORDER BY num_races DESC;

-- Get the number of wins and total points for each driver
SELECT Drivers.driverId, Drivers.forename, Drivers.surname, COUNT(Driver_Standings.wins) AS wins, SUM(Driver_Standings.points) AS total_points
FROM Drivers
INNER JOIN Driver_Standings ON Drivers.driverId = Driver_Standings.driverId
GROUP BY Drivers.driverId, Drivers.forename, Drivers.surname;

--Get the average duration of pitstops for each race
SELECT Races.name, AVG(Pitstop.milliseconds) AS avg_milliseconds_pitstop
FROM Races
INNER JOIN Pitstop ON Races.raceId = Pitstop.raceId
GROUP BY Races.name;

--Get the constructor standings for raceId 100
SELECT Constructor.name, Constructor_Standing.points, Constructor_Standing.wins
FROM Constructor_Standing
INNER JOIN Constructor ON Constructor_Standing.constructorId = Constructor.constructorId
WHERE Constructor_Standing.raceId = 100
ORDER BY Constructor_Standing.points DESC;

-- retreive the fastets lap speed of the montreal grand prix of the 2022 race to and the drivers name to see which 
-- drivers had the fastest lap during that race
SELECT forename, surname, fastestLapSpeed 
FROM Races
INNER JOIN Circuit ON Circuit.circuitId = Races.circuitId
INNER JOIN Results ON Races.raceId = Results.raceId
INNER JOIN Drivers on Drivers.driverId = Results.driverId
WHERE Circuit.circuitId = 7 AND YEAR(Races.date) = 2022
ORDER BY fastestLapSpeed DESC;
