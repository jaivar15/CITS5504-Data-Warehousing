:setvar SqlSamplesSourceDataPath "C:\Users\anish\OneDrive - The University of Western Australia\Desktop\dw\"
:setvar DatabaseName "warehouse"
BULK INSERT [dbo].[dimCountry] 
FROM '$(SqlSamplesSourceDataPath)dimCountry.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a'
    --KEEPIDENTITY,

);

BULK INSERT [dbo].[dimExpectancy] 
FROM '$(SqlSamplesSourceDataPath)dimExpectancy.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a',
    --KEEPIDENTITY,
    TABLOCK
);

BULK INSERT [dbo].[dimTime] 
FROM '$(SqlSamplesSourceDataPath)dimTime.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a'
    --KEEPIDENTITY,

);

BULK INSERT [dbo].[dimSize] 
FROM '$(SqlSamplesSourceDataPath)dimSize.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a'
    --KEEPIDENTITY,

);


BULK INSERT [dbo].[FactTable] 
FROM '$(SqlSamplesSourceDataPath)factTable.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a',
    --KEEPIDENTITY,
    TABLOCK
);