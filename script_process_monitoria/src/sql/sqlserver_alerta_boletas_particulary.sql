
SELECT	*
FROM [modelo].[BaseErroOperacional].[ErrosParticularidadesBoletas_v2] 
where cast(DataInsertTable as date) >=   DATEADD(DAY,-7, cast(getdate() as date))