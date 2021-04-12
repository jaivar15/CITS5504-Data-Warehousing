PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = N'galaxy_schema')
DROP DATABASE galaxy_schema;
GO

PRINT '';
PRINT '*** Creating Database';
GO

Create database galaxy_schema
Go

Use galaxy_schema
Go

PRINT '';
PRINT '*** Creating Table dimCountry';
GO

CREATE TABLE dimCountry (
	countryID INT PRIMARY KEY,
	countryName VARCHAR(100) NOT NULL, 
	regionName VARCHAR(100) NOT NULL
);
GO 

PRINT '';
PRINT '*** Creating Table dimLogtype';
GO

CREATE TABLE dimLogType (
	logID INT PRIMARY KEY,
	log_type VARCHAR(150) NOT NULL, 
);
GO 

PRINT '';
PRINT '*** Creating Table dimGovCat';
GO

CREATE TABLE dimGovCat (
	govcat_ID INT PRIMARY KEY,
	category_type VARCHAR(150) NOT NULL, 
);
GO 

PRINT '';
PRINT '*** Creating Table dimMeasures';
GO

CREATE TABLE dimMeasures (
	measureID INT PRIMARY KEY,
	govcat_key INT NOT NULL, 
	measure VARCHAR(150) NOT NULL
);

GO 


PRINT '';
PRINT '*** Creating Table dimNonCompliance';
GO

CREATE TABLE dimNonCompliance (
	noncomplianceID INT PRIMARY KEY,
	non_compliance_type VARCHAR(150) NOT NULL
);

GO 

PRINT '';
PRINT '*** Creating Table dimTime';
GO

CREATE TABLE dimTime (
	timeID INT PRIMARY KEY,
	year INT NOT NULL, 
	day INT NOT NULL,
	month INT NOT NULL, 
);

GO 

PRINT '';
PRINT '*** Creating Table dimSource';
GO

CREATE TABLE dimSource (
	sourceID INT PRIMARY KEY,
	sourcetype_ID INT NOT NULL, 
	source varchar(150) NOT NULL
);

GO 

PRINT '';
PRINT '*** Creating Table dimSourceType';
GO

CREATE TABLE dimSourceType (
	sourcetype_ID INT PRIMARY KEY, 
	source_type varchar(050) NOT NULL
);

GO 

PRINT '';
PRINT '*** Creating Table FactTable';
GO

CREATE TABLE FactTableCovid (
	covidfactKey INT PRIMARY KEY, 
	locationID INT NOT NULL, 
	timeID INT NOT NULL, 
	confirmed INT, 
	recovery INT, 
	deaths INT
);

GO 

PRINT '';
PRINT '*** Creating Table FactTable';
GO

CREATE TABLE FactTableGovernment (
	governmentFactKey INT PRIMARY KEY, 
	countryID INT NOT NULL, 
	logID INT NOT NULL, 
	govcat_ID INT NOT NULL, 
	noncomplianceID INT NOT NULL, 
	target_pop INT, 
	comments VARCHAR(250),
	dateImplementedID INT NOT NULL, 
	sourceID INT NOT NULL,
	LINK VARCHAR(250) NOT NULL

);

AlTER TABLE FactTableGovernment ADD CONSTRAINT
FK_countryID FOREIGN KEY (countryID)REFERENCES dimCountry(countryID);
AlTER TABLE FactTableGovernment ADD CONSTRAINT
FK_logID FOREIGN KEY (logID)REFERENCES dimLogType(logID);
AlTER TABLE FactTableGovernment ADD CONSTRAINT
FK_govcat_ID FOREIGN KEY (govcat_ID)REFERENCES dimMeasures(measureID);
AlTER TABLE FactTableGovernment ADD CONSTRAINT
FK_noncomplianceID FOREIGN KEY (noncomplianceID)REFERENCES dimNonCompliance(noncomplianceID);
AlTER TABLE FactTableGovernment ADD CONSTRAINT
FK_dateImplementedID FOREIGN KEY (dateImplementedID)REFERENCES dimTime(timeID);
AlTER TABLE FactTableGovernment ADD CONSTRAINT
FK_sourceID FOREIGN KEY (sourceID)REFERENCES dimSource(sourceID);

AlTER TABLE FactTableCovid ADD CONSTRAINT
FK_countryCovidID FOREIGN KEY (locationID)REFERENCES dimCountry(countryID);
AlTER TABLE FactTableCovid ADD CONSTRAINT
FK_timeCovidID FOREIGN KEY (timeID)REFERENCES dimTime(timeID);

AlTER TABLE dimSource ADD CONSTRAINT
FK_sourcetype_ID FOREIGN KEY (sourcetype_ID)REFERENCES dimSourceType(sourcetype_ID);
AlTER TABLE dimMeasures ADD CONSTRAINT
FK_govtID FOREIGN KEY (govcat_key)REFERENCES dimGovCat(govcat_ID);


GO 