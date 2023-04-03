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
