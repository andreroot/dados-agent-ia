# 📡 projeto dados-agent-ia

Uma biblioteca de exemplos de construção de agents, que podem ser aplicaveis e integrar com serviços.
1. Utiliza CrewAI Pydantic e Langchian em teste, junto fastapi
2. Executa python que são acessados via workflow N8N para execução de query que são respostas das solicitações via agent IA N8N

### Scripts | acessados via workflow N8N 🔔
1. Todos os scripts python são acionados via ssh - script_process_monitoria/shell_script

    > consulta processos thunders executados com sucesso
    run_workflow_n8n_sqlserver_alertas_erros_operacionais.sh -> script_process_monitoria/src/run_workflow_n8n_sqlserver_alertas.py

    > consulta erros na monitoria
    run_workflow_n8n_sqlserver_alertas_erros_operacionais.sh ->  script_process_monitoria/src/run_workflow_n8n_erros_operacionais.py

    > consulta alertas
    run_workflow_n8n_athena_execution.sh ->  script_process_monitoria/src/run_workflow_n8n_athena.py

    > inserir particularidade

    teste:
    webhook teste - alterar para http://172.16.128.133:5678/webhook-test/...

    prod:
        curl -X GET 'http://172.16.128.133:5678/webhook-test/execute-python?processo=consulta_particularidade' -H "Content-Type: application/json"  -d '{ "alerta":"erros_boleta_inflacao_futuro"}'

        curl -X POST 'http://172.16.128.133:5678/webhook/trigger_erros_operacionais?processo=insert_particularidade' -H "Content-Type: application/json"  

        -d '{"chatId": "5511940147165@c.us","mensagem": "Agent, inserir essas infromações na particularidade","particularidade":{ "msg_particularidade":"via teams Luis - 11/07","data_particularidade":"2025-07-11","alerta":"erros_boleta_inflacao_futuro","boleta":"IC-CC366-25","operador":"Rafael Campos"}}'
### Agents CrewAI 🎧

1. construção dos agents crewai e excução via crewai

[CREWAI]
    na pasta mcp_agent_n8n_ia
    mcp_agent_n8n_ia$ crewai run

    1. utilizando plataforma crewia: dados-agent-ia/mcp_agent_n8n_ia

        pip install crewia crewia[tools] langchian pydantic

    - agents: necessitam de informações role(função/especialidade),  goal(), backstory()

    - tasks: necessitam de um fluxo de contexto para ter mais precisão na respostas

    2. virtualenv

    3. instalação dos pacotes: crewai, crewai-tools, 

    4. execução dos comandos
        crewai create mcp-agent-n8n-ia
        cd mcp-agent-n8n-ia
        crewai install

    5. fiz adaptações e gerar o resultado, a IA utilizou o endpoint para responder as perguntas
        *no crew.py, usando a api no N8N e usando @tool crie as ferramentas dentro do agent e das tasks*

    6. agent especialista em enge nahria de dados e responsavel pelos processo de pipeline

    7. tasks que responde duvidas sobre os processos usando o endpoint na n8n
        http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados
        http://172.16.128.133:5678/webhook/execute-python?processo=boletas


2. construção de crewai e execução via fastapi

[FastApi|CrewAI]
    na pasta mcp_agent_n8n_ia/src
    uvicorn mcp_agent_n8n_ia.run_app:app --reload

[docker-fastapi-crew]
    na pasta mcp_agent_n8n_ia
    docker-compose up -d

    subir com docker e liberar porta de acesso

        1. criar um fluxo com n8n

            usando 🧱 Node "Execute Command"

        2. teste com curl

            curl -X POST "http://localhost:8000/executar-crew?nome=processos_error" -H "Content-Type: application/json" -d '{"pergunta": "quantos processos estão com erros"}'
            curl -X POST "http://172.16.128.133:8000/executar-crew?nome=processos_error" -H "Content-Type: application/json" -d '{"pergunta": "qual processo esta com maior numero de linhas?"}'


### CrewAI Pydantic FastApi | construção 
