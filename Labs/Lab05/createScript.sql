:setvar DatabaseName "AdventureWorksDWNew"

-- ****************************************
-- Drop Database
-- ****************************************
PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = N'$(DatabaseName)')
    DROP DATABASE $(DatabaseName);

-- If the database has any other open connections close the network connection.
IF @@ERROR = 3702 
    RAISERROR('$(DatabaseName) database cannot be dropped because there are still other open connections', 127, 127) WITH NOWAIT, LOG;
GO

-- ****************************************
-- Create Database
-- ****************************************
PRINT '';
PRINT '*** Creating Database';
GO

CREATE DATABASE $(DatabaseName);
GO

USE $(DatabaseName);
GO

CREATE TABLE [dbo].[DimProductDest](
	[EnglishProductName] [nvarchar](50) NOT NULL,
	[Color] [nvarchar](15) NOT NULL,
	[ListPrice] [money] NULL,
	[DealerPrice] [money] NULL,
	[EnglishDescription] [nvarchar](400) NULL,
	[StartDate] [datetime] NULL,
	[EndDate] [datetime] NULL
) ON [PRIMARY];
GO
