--> NOVA QUERY PARA GERAR AS INFORMAÇÕES SOBRE OS ALERTAS
--> DATA 26/03 
--> GERADO VIA PACOTE DYNAMICALLY
SELECT * 
   , REPLACE(Resultado, '.', ',') AS ResultadoFormat
   , REPLACE(netFinalVolumeMwm, '.', ',') AS netFinalVolumeMwmFormat

FROM [modelo].[BaseErroOperacional].[AlertasDetalhes] 
WHERE Thunders IN ('Safira','Comercial')
and convert(date,data_insert_alert, 103) >= '2025-03-25'
and code is not null
and YEAR(DataFornecimento) >= 2025