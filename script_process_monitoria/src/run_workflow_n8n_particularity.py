
import pandas as pd

import datetime
from json.decoder import JSONDecodeError
import numpy as np

from resource.utilitarios import Utils
from conectores.conectar_sql_server import ConectSqlServer


# CONSULTA BOLETAS COM ERROS OPERACIONAIS
def marcarBoletasParticularidadeViaTabelaAlertas(msg, dataenvio, tipo_erro, operador):

    serversql = ConectSqlServer()
    engine = serversql.get_engine_sqlalchemy() 

    # QUERY QUE RETORNA OS ERROS E PARTICULARIDADES DO ALERTA
    utils = Utils()
    # LÊ O ARQUIVO SQL QUE CONTÉM A QUERY
    sql_alert = sql_query = utils.read_file("sqlserver_alerta_powerbi_v4.sql")

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
            df = df[ (df['tipo_erro']==tipo_erro) & (df['userOperatorName']==operador) ].copy()
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

    result = insert_particularidades(df_ex[['Thunders', 'code', 'sequence', 'DataFornecimento', 'classificacao','tipo_erro', 'DataInsert', 'Observacao', 'DataEmailEnviado','DataEmailRespondido', 'tipoErro', 'Registro', 'Alerta']])

    return result            

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

        df['DataFornecimento']=df.apply(lambda x: pd.to_datetime(x['DataFornecimento']).date().strftime('%Y-%m-%d') if x['DataFornecimento']!=None else None,axis=1)
        
        df['DataInsert']=df.apply(lambda x: pd.to_datetime(x['DataInsert'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataInsert']!=None else None,axis=1)
        
        df['DataEmailEnviado']=df.apply(lambda x: pd.to_datetime(x['DataEmailEnviado'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataEmailEnviado']!=None else None,axis=1) #, format="%d/%m/%y").date().strftime('%Y-%m-%d')
        
        df['DataEmailRespondido']=df.apply(lambda x: pd.to_datetime(x['DataEmailRespondido'], format='%d/%m/%Y').date().strftime('%Y-%m-%d') if x['DataEmailRespondido']!=None else None,axis=1)
        
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

        return f"Inseridos {len(df)} boleta marcadas como particularidade!!!"

    except TypeError as e:
        # Captura cualquier excepción de SQLAlchemy
        return f"Error Json:{e}"

    except JSONDecodeError as e:
        return f"JSON can't decode: {e}"


def consultarparticularidadesBoletas(code):
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

    # FILTRO POR TIPO DE ERRO
    # df = df[ (df['tipo_erro']=='erros_boleta_inflacao_futuro') ].copy()

    return df[ (df['code']==code) ].drop_duplicates().values.tolist()

# INSERT
def insertManualDataFrame(thunders, code, seq, classif, msg, dataenvio, alerta):
    df = pd.DataFrame()

    # df=pd.DataFrame({
    #     'Thunders':[thunders], #  for txt in range(0,12)
    #     'code':[code],
    #     'sequence':[seq],
    #     'DataFornecimento':[None],
    #     'classificacao':[''],
    #     'DataInsert':[None, None],
    #     'Observacao':[msg, msg],
    #     'DataEmailEnviado':['03/10/2024','03/10/2024'],
    #     'DataEmailRespondido':['03/10/2024','03/10/2024'],
    #     'tipoErro':['Particularidade','Particularidade'],
    #     'Registro':[None,None],#'C:\Users\lcacciatori\Safira Energia\Risco e Dados - Documentos\Risco\Erros Operacionais\VRJ\VC091-24'
    #     'Alerta':['erros_boleta_preco_baixo','erros_boleta_inflacao_futuro']
    # })    

    df=pd.DataFrame({
        'Thunders':[thunders], #  for txt in range(0,12)
        'code':[code],
        'sequence':[seq],
        'DataFornecimento':[None],
        'classificacao':[classif],
        'DataInsert':[None],
        'Observacao':[msg],
        'DataEmailEnviado':[dataenvio],
        'DataEmailRespondido':[dataenvio],
        'tipoErro':['Particularidade'],
        'Registro':[None],#'C:\Users\lcacciatori\Safira Energia\Risco e Dados - Documentos\Risco\Erros Operacionais\VRJ\VC091-24'
        'Alerta':[alerta]
    }) 
        
    return df

if __name__ == '__main__':
    # 
    # Executa a consulta
    msg = 'Boleta duplicada encontrada. Favor verificar.'

    #results = marcarBoletasParticularidadeViaTabelaAlertas( msg, '30/06/2025', 'erros_boleta_inflacao_futuro', 'Rafael Campos')

    results = consultarparticularidadesBoletas('erros_boleta_inflacao_futuro')

    print(f"Resultados da operação: {results}")    