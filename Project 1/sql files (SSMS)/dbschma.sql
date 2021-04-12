BULK INSERT [dbo].[FactTable] 
FROM 'C:\Users\anish\OneDrive - The University of Western Australia\Desktop\dw\factTable.csv'
WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a',
    --KEEPIDENTITY,
    TABLOCK
);