PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = N'warehouse')
DROP DATABASE warehouse;
GO

PRINT '';
PRINT '*** Creating Database';
GO

Create database warehouse
Go

Use warehouse
Go

PRINT '';
PRINT '*** Creating Table dimCountry';
GO

CREATE TABLE dimCountry (
	countryID INT PRIMARY KEY,
	countryName VARCHAR(100) NOT NULL, 
	continentName VARCHAR(100) NOT NULL,
	regionName VARCHAR(100) NOT NULL
);
GO 

PRINT '';
PRINT '*** Creating Table dimTime';
GO

CREATE TABLE dimTime (
	timeID INT PRIMARY KEY, 
	month VARCHAR(50) NOT NULL,
	quarter VARCHAR(50) NOT NULL, 
	year INT NOT NULL
)
GO

PRINT '';
PRINT '*** Creating Table dimExpectancy';
GO

CREATE TABLE dimExpectancy (
	expID INT PRIMARY KEY, 
	life_expectancy VARCHAR(50) NOT NULL, 
)
GO


PRINT '';
PRINT '*** Creating Table dimSize';
GO

CREATE TABLE dimSize (
	sizeID INT PRIMARY KEY, 
	size VARCHAR(50) NOT NULL, 
)
GO


PRINT '';
PRINT '*** Creating Table FactTable';
GO

CREATE TABLE FactTable (
	facttableID INT PRIMARY KEY,
	countryID INT NOT NULL, 
	timeID INT NOT NULL,
	sizeID INT NOT NULL,
	expID INT NOT NULL,
	confirmed INT NOT NULL,
	deaths INT NOT NULL,
	recovered INT NOT NULL
)
GO


AlTER TABLE FactTable ADD CONSTRAINT
FK_countryID FOREIGN KEY (countryID)REFERENCES dimCountry(countryID);
AlTER TABLE FactTable ADD CONSTRAINT
FK_timeID FOREIGN KEY (timeID)REFERENCES dimTime(timeID);
AlTER TABLE FactTable ADD CONSTRAINT
FK_expID FOREIGN KEY (sizeID)REFERENCES dimSize(sizeID);
AlTER TABLE FactTable ADD CONSTRAINT
FK_sizeID FOREIGN KEY (expID)REFERENCES dimExpectancy(expID);