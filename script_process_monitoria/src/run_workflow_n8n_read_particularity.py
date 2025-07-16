
import pandas as pd

import datetime
from json.decoder import JSONDecodeError
import numpy as np
import sys

from resource.utilitarios import Utils
from conectores.conectar_sql_server import ConectSqlServer


def consultarparticularidadesBoletas(alerta, code):
    """
    Consulta as particularidades das boletas marcadas na tabela de alertas.
    """
    serversql = ConectSqlServer()
    engine = serversql.get_engine_sqlalchemy() 

    # QUERY QUE RETORNA AS PARTICULARIDADES DAS BOLETAS
    utils = Utils()
    sql_query = utils.read_file("sqlserver_alerta_boletas_particulary.sql")

    df = pd.DataFrame()
    df = pd.read_sql_query(sql_query, engine)

    df['DataFornecimento'] = df.apply(lambda x: pd.to_datetime(x['DataFornecimento']).date().strftime('%Y-%m-%d') if x['DataFornecimento'] is not None else "None", axis=1)

    df['DataInsertTable'] = df.apply(lambda x: pd.to_datetime(x['DataInsertTable']).strftime('%Y-%m-%d  %H:%M:%S') if x['DataInsertTable'] is not None else "None", axis=1)

    df = df.astype(str) 

    # FILTRO POR TIPO DE ERRO
    df = df[ (df['Alerta']==alerta) ].copy()
        
    lista_dicts = df.to_dict(orient='records')
    return lista_dicts 


if __name__ == '__main__':
    # Exemplo de uso da função consultarparticularidadesBoletas
    # Você pode passar o alerta e o código que deseja consultar
    args = sys.argv  # <--- Adicione esta linha

    if len(args) < 2:
        print("Uso: python run_workflow_n8n_particularity.py <alerta>")
        sys.exit(1)
        
    results = consultarparticularidadesBoletas(args[1],None)

    print(f"Resultados da operação: {results}")    