
SELECT distinct Thunders, code, Alerta, DataFornecimento, max(DataInsertTable) DataInsertTable
  FROM [modelo].[BaseErroOperacional].[ErrosParticularidadesBoletas_v2] 
 WHERE cast(DataInsertTable as date) >= (SELECT DATEADD(DAY,-1, max(DataInsertTable)) FROM [modelo].[BaseErroOperacional].[ErrosParticularidadesBoletas_v2] )
 GROUP BY Thunders, code, Alerta, DataFornecimento