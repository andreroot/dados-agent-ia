
WITH t_processos as 
(
SELECT *           
FROM "safira-stream-database"."tab_stream_process_monitoria" 

WHERE process_name_pai IN ('sql-server/exec_informacao_comercial'
,'sql-server/operation_history'
,'sql-server/poc_historico'
,'sql-server/exec_historico_posicao_log'
,'sql-server/exec_historico_posicaocontraparte_log'
,'sql-server/exec_historico_resultado_log'
,'sql-server/extract_safira_all_operations'
,'sql-server/extract_comercial_all_operations'
,'sql-server/extract_indra_all_operations')
AND regexp_extract(descricao_status,'Dados inseridos') is not null
)

,t_ult_exec_processos AS 
(SELECT process_name_pai
            , MAX(date_end) OVER xlog max_date_end
            , date_end
            , RANK() OVER xlog nrows_etapa
FROM t_processos

WHERE date_end BETWEEN date_parse(concat(CAST(date_add('day', -1, current_date ) AS VARCHAR),' 00:00:00.0000'), '%Y-%m-%d %T.%f') 
                    AND date_parse(concat(CAST(date_add('day', 0, current_date ) AS VARCHAR),' 23:59:59.9999'), '%Y-%m-%d %T.%f') 
WINDOW xlog AS (PARTITION BY  process_name_pai ORDER BY date_end DESC)

)


select u.process_name_pai
    , u.date_end
    , regexp_extract(p.descricao_status,'\d+')
from t_ult_exec_processos u
INNER JOIN t_processos p on (u.process_name_pai = p.process_name_pai and u.max_date_end = p.date_end)
WHERE nrows_etapa = 1