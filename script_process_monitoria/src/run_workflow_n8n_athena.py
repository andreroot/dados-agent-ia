# import boto3
import time
import sys
import pandas as pd


from resource.utilitarios import Utils
from conectores.conectar_aws import ConectAWS

def return_query(database, query, output_location):

    # Inicializa o cliente Athena
    con = ConectAWS()
    boto_session = con.get_svc_user_credentials()

    athena = boto_session.client('athena', region_name='us-east-1')

    # Inicia a execução da consulta
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': output_location}
    )

    # Pega o ID da execução
    query_execution_id = response['QueryExecutionId']

    return athena, query_execution_id

def execute_athena_query(database, query, output_location, process):
    """
    Executa uma consulta no Amazon Athena e retorna os resultados.
    
    :param database: Nome do banco de dados no Athena.
    :param query: Consulta SQL a ser executada.
    :param output_location: Localização no S3 para armazenar os resultados da consulta.
    :return: Resultados da consulta ou mensagem de erro.
    """
    try:
        df = pd.DataFrame()
        
        athena, query_execution_id = return_query(database, query, output_location)

        # Espera a consulta terminar
        while True:
            result = athena.get_query_execution(QueryExecutionId=query_execution_id)
            status = result['QueryExecution']['Status']['State']
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(2)

        # Se a consulta foi bem sucedida, pega os resultados
        if status == 'SUCCEEDED':
            results = athena.get_query_results(QueryExecutionId=query_execution_id)
            list_results = []
            # Extrai os dados dos resultados
            if 'Rows' in results['ResultSet']:
                # Retorna os dados como uma lista de dicionários
                data_rows = results['ResultSet']['Rows'][1:]  # Ignora o cabeçalho
                # print( data_rows[0]['Data'])
                for row in data_rows:
                    row_data = [col['VarCharValue'] if 'VarCharValue' in col else None for col in row['Data']]
                    list_results.append(row_data)

            if process=='error':
                # Defina os nomes das colunas
                colunas = ['processo', 'data', 'linhas', 'status']

                # Crie o DataFrame
                df = pd.DataFrame(list_results, columns=colunas)
            if process=='execution':
                # Defina os nomes das colunas
                colunas = ['processo', 'data', 'linhas']

                # Crie o DataFrame
                df = pd.DataFrame(list_results, columns=colunas)

            lista_dicts = df.to_dict(orient='records')
            return  lista_dicts
        else:
            return f"Resultados da consulta: {status}"

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Inicializa a classe Utils para ler arquivos
    utils = Utils()

    # Configurações
    database = 'safira-stream-database'
    query = 'SELECT * FROM sua_tabela LIMIT 10'

    args = sys.argv  # <--- Adicione esta linha

    if args[1] == 'error':
        sql_query = utils.read_file("script_athena_process_error.sql")

        output_location = 's3://aws-athena-query-results-967201331463-us-east-1/'
        # Executa a consulta
        results = execute_athena_query(database, sql_query, output_location, process='error')

        print(f"Resultados da consulta:{results}")

    elif args[1] == 'execution':
        sql_query = utils.read_file("script_athena_process_executados.sql")

        output_location = 's3://aws-athena-query-results-967201331463-us-east-1/'
        # Executa a consulta
        results = execute_athena_query(database, sql_query, output_location, process='execution')

        print(f"Resultados da consulta:{results}")