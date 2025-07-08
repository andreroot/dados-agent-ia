--> NOVA QUERY PARA GERAR AS INFORMAÇÕES SOBRE OS ALERTAS
--> DATA 26/03 
SELECT tipo_erro, Thunders, COUNT(code) erros, COUNT(DISTINCT code) boletas 
FROM [modelo].[BaseErroOperacional].[AlertasDetalhes] 
WHERE Thunders IN ('Safira','Comercial')
and convert(date,data_insert_alert, 103) >= '2025-03-25'
and code is not null
and YEAR(DataFornecimento) >= 2025
GROUP BY tipo_erro, Thunders