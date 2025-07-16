
import pandas as pd
import sys

import datetime
from json.decoder import JSONDecodeError
import numpy as np

from resource.utilitarios import Utils
from conectores.conectar_sql_server import ConectSqlServer


# CONSULTA BOLETAS COM ERROS OPERACIONAIS
def consulta_alertas(nome_consulta):

    serversql = ConectSqlServer()
    engine = serversql.get_engine_sqlalchemy() 

    # QUERY QUE RETORNA OS ERROS E PARTICULARIDADES DO ALERTA
    utils = Utils()
    # LÊ O ARQUIVO SQL QUE CONTÉM A QUERY
    if nome_consulta == 'alertas_operacionais':
        sql_alert = utils.read_file("sqlserver_alertas_erros_operacionais.sql")        

    elif nome_consulta == 'resultado':
        sql_alert = utils.read_file("sqlserver_alertas_erros_resultados.sql") 

    elif nome_consulta == 'posicao':
        sql_alert = utils.read_file("sqlserver_alertas_erros_volumes.sql") 

    elif nome_consulta == 'particularity':
        sql_alert = utils.read_file("sqlserver_alerta_boletas_particulary.sql")


    # TRATAR O DATAFRAME RETORNO DA QUERY DO ALERTA
    df = pd.DataFrame()
    df = pd.read_sql_query(sql_alert, engine)
        
    lista_dicts = df.to_dict(orient='records')
    return lista_dicts 

if __name__ == '__main__':
    # Exemplo de uso da função consulta_alertas
    # Você pode passar o nome da consulta que deseja executar

    args = sys.argv  # <--- Adicione esta linha
    if len(args) < 2:
        print("Uso: python run_workflow_n8n_alertas_boletas.py <nome_consulta>")
        sys.exit(1)
        
    if args[1] == 'alertas_operacionais':
        nome_consulta = 'alertas_operacionais'
    elif args[1] == 'resultado':
        nome_consulta = 'resultado'    
    elif args[1] == 'posicao':  
        nome_consulta = 'posicao'
    elif args[1] == 'inconsistencia':  
        nome_consulta = 'inconsistencia'        
    elif args[1] == 'particularity':
        nome_consulta = 'particularity'
    results = consulta_alertas(nome_consulta)

    print(f"Resultados da operação: {results}")    