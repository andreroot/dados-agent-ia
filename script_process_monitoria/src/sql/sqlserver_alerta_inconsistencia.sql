SELECT code, netFinalVolumeMwm posicao, Resultado resultado --sum(cast(netFinalVolumeMwm  as float)) 
FROM [modelo].[BaseErroOperacional].[AlertasDetalhes] 
WHERE Thunders IN ('Safira','Comercial')
and convert(date,data_insert_alert, 103) >= '2025-03-25'
and code is not null
and tipo_erro = 'erros_boletas_inconsistencia_posicao'
and YEAR(DataFornecimento) >= 2025