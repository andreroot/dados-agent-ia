
WITH t_processos as 
(
SELECT *           
FROM "safira-stream-database"."tab_stream_process_monitoria" 
WHERE status NOT IN ( 'EXECUTANDO' , 'EXECUTANDO_TESTE', 'OK' )
)

,t_ult_exec_processos AS 
(SELECT process_name_pai
            , MAX(date_end) OVER xlog max_date_end
            , date_end
            , RANK() OVER xlog nrows_etapa
FROM t_processos

WHERE date_end BETWEEN date_parse(concat(CAST(date_add('day', 0, current_date ) AS VARCHAR),' 00:00:00.0000'), '%Y-%m-%d %T.%f') 
                    AND date_parse(concat(CAST(date_add('day', 0, current_date ) AS VARCHAR),' 23:59:59.9999'), '%Y-%m-%d %T.%f') 
WINDOW xlog AS (PARTITION BY  process_name_pai ORDER BY date_end DESC)

)


select u.process_name_pai
    , u.date_end
    , 0 as linhas
    , p.status
from t_ult_exec_processos u
INNER JOIN t_processos p on (u.process_name_pai = p.process_name_pai and u.max_date_end = p.date_end)
WHERE nrows_etapa = 1