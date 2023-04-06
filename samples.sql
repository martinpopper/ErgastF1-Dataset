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
SELECT Drivers.forename, Drivers.surname, COUNT(Driver_Standings.wins) AS wins, SUM(Driver_Standings.points) AS total_points
FROM Drivers
INNER JOIN Driver_Standings ON Drivers.driverId = Driver_Standings.driverId
GROUP BY Drivers.driverId;

--Get the average duration of pitstops for each race
SELECT Races.name, AVG(Pitstop.duration) AS avg_duration
FROM Races
LEFT OUTER JOIN Pitstop ON Races.raceId = Pitstop.raceId
GROUP BY Races.raceId;

--Get the constructor standings for a particular race:
SELECT Constructor.name, Constructor_Standing.points, Constructor_Standing.wins
FROM Constructor_Standing
INNER JOIN Constructor ON Constructor_Standing.constructorId = Constructor.constructorId
WHERE Constructor_Standing.raceId = [raceId]
ORDER BY Constructor_Standing.points DESC;

--Retrieve the circuit name, race name, and the average lap time for each race held in the circuit with the circuit_id = 5, only for races held in the year 2022 or later, ordered by the average lap time in ascending order:
SELECT c.name AS circuit_name, r.name AS race_name, AVG(milliseconds) AS average_lap_time
FROM Circuit c
INNER JOIN Races r ON c.circuitId = r.circuitId
INNER JOIN Results rs ON r.raceId = rs.raceId
WHERE c.circuitId = 5 AND YEAR(r.date) >= 2022
GROUP BY r.raceId
ORDER BY average_lap_time ASC;
