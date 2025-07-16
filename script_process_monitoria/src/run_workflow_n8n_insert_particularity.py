
import pandas as pd

import datetime
from json.decoder import JSONDecodeError
import numpy as np
import sys

from resource.utilitarios import Utils
from conectores.conectar_sql_server import ConectSqlServer


# CONSULTA BOLETAS COM ERROS OPERACIONAIS
def marcarBoletasParticularidadeViaTabelaAlertas(msg, dataenvio, tipo_erro, boleta, operador, flag_insert=True):

    serversql = ConectSqlServer()
    engine = serversql.get_engine_sqlalchemy() 

    # QUERY QUE RETORNA OS ERROS E PARTICULARIDADES DO ALERTA
    utils = Utils()
    # LÊ O ARQUIVO SQL QUE CONTÉM A QUERY
    sql_alert = utils.read_file("sqlserver_alerta_powerbi_v4.sql")

    # TRATAR O DATAFRAME RETORNO DA QUERY DO ALERTA
    df = pd.DataFrame()
    df = pd.read_sql_query(sql_alert, engine)
    
    # tipo_erro recebe algum valor
    if tipo_erro:
        # FILTRO POR TIPO DE ERRO E OPERADOR
        if operador=='All':
            # FILTRO POR TIPO DE ERRO
            df = df[ (df['tipo_erro']==tipo_erro)  ].copy()
        else:
            df = df[ (df['tipo_erro']==tipo_erro) & (df['userOperatorName']==operador) & (df['code']==boleta)].copy()
    else:
        # FILTRO POR OPERADOR
        if operador=='All':
            df = df.copy()
        else:
            df = df[ (df['userOperatorName']==operador) ].copy()
    
    df_ex = df[['Thunders','code','sequence','DataFornecimento','classifications','startDate','tipo_erro']].copy()
    # df_ex=df_ex.rename({"Codigo":"code","Entrega":"sequence","Classificacao":"classificacao"}, axis=1)
                
    df_ex=df_ex.rename({"classifications":"classificacao"}, axis=1)
    
    df_ex['DataInsert']=None
    df_ex['Observacao']=msg
    df_ex['DataEmailEnviado']=dataenvio
    df_ex['DataEmailRespondido']=dataenvio
    df_ex['tipoErro']='Particularidade'
    df_ex['Registro']=None
    df_ex['Alerta']=df_ex['tipo_erro']        

    if flag_insert:
        # INSERIR DADOS NA TABELA SQL
        result = insert_particularidades(df_ex[['Thunders', 'code', 'sequence', 'DataFornecimento', 'classificacao','DataInsert','Observacao', 'DataEmailEnviado','DataEmailRespondido', 'tipoErro', 'Registro', 'Alerta']])
        print(result)
    else:
        # NÃO INSERIR DADOS NA TABELA SQL
        print("Não foi inserido dados na tabela ErrosParticularidadesBoletas_v2")
        #  --- IGNORE ---
        # result = insert_particularidades(df_ex[['Thunders', 'code', 'sequence', 'DataFornecimento', 'classificacao','tipo_erro', 'DataInsert', 'Observacao', 'DataEmailEnviado','DataEmailRespondido', 'tipoErro', 'Registro', 'Alerta']])
        #  --- IGNORE ---
        # print(result) --- IGNORE ---
    # result = insert_particularidades(df_ex[['Thunders', 'code', 'sequence', 'DataFornecimento', 'classificacao','tipo_erro', 'DataInsert', 'Observacao', 'DataEmailEnviado','DataEmailRespondido', 'tipoErro', 'Registro', 'Alerta']])

    # Garantir que NaN virem None
    df_ex = df_ex.where(df_ex.notnull(), None)  # Garante que NaN virem None
    # Converter DataInsertTable para o formato adequado
    # df_ex['DataInsertTable'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]    
    # Converter todas as colunas para string
    # Converter DataFornecimento para o formato adequado
    df_ex['DataFornecimento'] = df_ex.apply(lambda x: pd.to_datetime(x['DataFornecimento']).date().strftime('%Y-%m-%d') if x['DataFornecimento'] is not None else "None", axis=1)
    # Converter DataInsert para o formato adequado
    df_ex['DataInsert'] = df_ex.apply(lambda x: pd.to_datetime(x['DataInsert'], format='%Y-%m-%d').date().strftime('%Y-%m-%d') if x['DataInsert'] is not None else "None", axis=1)
    # Converter DataEmailEnviado para o formato adequado
    df_ex['DataEmailEnviado'] = df_ex.apply(lambda x: pd.to_datetime(x['DataEmailEnviado'], format='%Y-%m-%d').date().strftime('%Y-%m-%d') if x['DataEmailEnviado'] is not None else "None", axis=1)
    # Converter DataEmailRespondido para o formato adequado
    df_ex['DataEmailRespondido'] = df_ex.apply(lambda x: pd.to_datetime(x['DataEmailRespondido'], format='%Y-%m-%d').date().strftime('%Y-%m-%d') if x['DataEmailRespondido'] is not None else "None", axis=1)
    df_ex = df_ex.astype(str) 

    lista_dicts = df_ex.to_dict(orient='records')

    return lista_dicts          

# FUNCTION: CHAMDA PARA PROC QUE INSERE DADOS NA TABELA SQL
def insert_particularidades( df):

    """Gravar json na tabela via proc
    """

    try:
        # MUDAR NOME DA COLUNA
        df=df.rename(columns={"[sequence]":"sequence"})

        # ALTERAR CAMPOS NAN PARA NONE
        df=df.replace({np.nan: None})

        # TRATAMENTO DE DATAS PARA FORMATO ADEQUADO PARA INSERÇÃO
        df['DataInsertTable']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # df['DataFornecimento']=df.apply(lambda x: pd.to_datetime(x['DataFornecimento'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataFornecimento']!=None else None,axis=1)

        # df['DataFornecimento']=df.apply(lambda x: pd.to_datetime(x['DataFornecimento']).date().strftime('%Y-%m-%d') if x['DataFornecimento']!=None else None,axis=1)
        
        # df['DataInsert']=df.apply(lambda x: pd.to_datetime(x['DataInsert'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataInsert']!=None else None,axis=1)
        
        # df['DataEmailEnviado']=df.apply(lambda x: pd.to_datetime(x['DataEmailEnviado'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataEmailEnviado']!=None else None,axis=1) #, format="%d/%m/%y").date().strftime('%Y-%m-%d')
        
        # df['DataEmailRespondido']=df.apply(lambda x: pd.to_datetime(x['DataEmailRespondido'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataEmailRespondido']!=None else None,axis=1)
        
        # CASO HAJA ALGUM CAMPO NULO ALTERAR CAMPOS NAN PARA NONE            
        df=df.replace({np.nan: None})

        # SEPARAR COLUNAS 
        df=df[['Thunders','code','sequence','DataFornecimento','classificacao','DataInsert','Observacao','DataEmailEnviado','DataEmailRespondido','tipoErro','Registro','DataInsertTable','Alerta']]

        # creating column list for insertion
        cols = ",".join(['[' + str(i) +']' for i in df.columns.tolist()])

        print(cols)
        
        # BASE TESTE NO DATABASE MODELO
        #sql_query = "INSERT INTO [modelo].[BaseErroOperacional].[ErrosParticularidadesBoletas] (" +cols + ") VALUES (" + "?,"* int(len(df.columns)-1) + "?)"

        sql_query = "INSERT INTO [modelo].[BaseErroOperacional].[ErrosParticularidadesBoletas_v2] (" +cols + ") VALUES (" + "?,"* int(len(df.columns)-1) + "?)"

        print(sql_query)
        
        serversql = ConectSqlServer()
        
        engine = serversql.get_engine_pyodbc('modelo') 
        
        cursor = engine.cursor()
        
        cursor.executemany(sql_query, list(map(list, df.itertuples(index=False))))
        
        engine.commit()

        cursor.close()

        return f"Total de dados ({len(df)}) inseridos com sucesso na tabela ErrosParticularidadesBoletas_v2"
    except TypeError as e:
        # Captura cualquier excepción de SQLAlchemy
        return f"Error Json:{e}"

    except JSONDecodeError as e:
        return f"JSON can't decode: {e}"



if __name__ == '__main__':
    # Você pode passar o alerta e o código que deseja consultar
    args = sys.argv  # <--- Adicione esta linha

    if len(args) < 4:
        print("Uso: python run_workflow_n8n_insert_particularity.py <msg> <dataenvio> <tipo_erro> <boleta> <operador>")
        sys.exit(1)

    # msg = 'Boleta duplicada encontrada. Favor verificar.'
    # dataenvio = '2025-06-30'
    # tipo_erro = 'erros_boleta_inflacao_futuro'
    # operador = 'Rafael Campos'


    results = marcarBoletasParticularidadeViaTabelaAlertas(args[1], args[2], args[3], args[4], args[5])


    print(f"Resultados da operação: {results}")    