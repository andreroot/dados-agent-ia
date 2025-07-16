SELECT Thunders, DataFornecimento, netFinalVolumeMwm as valor , tipo_erro
FROM [modelo].[BaseErroOperacional].[AlertasDetalhes] 
WHERE Thunders IN ('Grupo_Safira')
and convert(date,data_insert_alert, 103) >= '2025-03-25'
and tipo_erro = 'erros_volume'
and YEAR(DataFornecimento) >= 2025
union all
SELECT Thunders, DataFornecimento, Resultado  as valor , tipo_erro 
FROM [modelo].[BaseErroOperacional].[AlertasDetalhes] 
WHERE Thunders IN ('Grupo_Safira')
and convert(date,data_insert_alert, 103) >= '2025-03-25'
and tipo_erro = 'erros_resultado'
and YEAR(DataFornecimento) >= 2025