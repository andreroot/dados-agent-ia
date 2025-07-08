# dados-agent-ia

objetivo> uma biblioteca de exemplos de construção de agents, que podem ser aplicaveis e integrar com serviços

> contem poc com crewAI e pydantic

> poc usando fast api

### CrewAI Pydantic FastApi | construção dos agents

utilizando plataforma crewia

> pip install crewia crewia[tools] langchian pydantic

- agents: necessitam de informações role(função/especialidade),  goal(), backstory()

- tasks: necessitam de um fluxo de contexto para ter mais precisão na respostas

1. virtualenv

2. instalação dos pacotes: crewai, crewai-tools, 

3. execução dos comandos
    crewai create mcp-agent-n8n-ia
    cd mcp-agent-n8n-ia
    crewai install

4. fiz adaptações e gerar o resultado, a IA utilizou o endpoint para responder as perguntas
*no crew.py, usando a api no N8N e usando @tool crie as ferramentas dentro do agent e das tasks*

5. agent especialista em enge nahria de dados e responsavel pelos processo de pipeline

6. tasks que responde duvidas sobre os processos usando o endpoint na n8n
http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados
http://172.16.128.133:5678/webhook/execute-python?processo=boletas

[CREWAI]
na pasta mcp_agent_n8n_ia
mcp_agent_n8n_ia$ crewai run

[FastApi]
na pasta mcp_agent_n8n_ia/src
uvicorn mcp_agent_n8n_ia.run_app:app --reload

criar um fluxo com n8n

    usando 🧱 Node "Execute Command"

teste com curl

    curl -X POST "http://localhost:8000/executar-crew?nome=processos_error" -H "Content-Type: application/json" -d '{"pergunta": "quantos processos estão com erros"}'

[docker-fastapi-crew]
na pasta mcp_agent_n8n_ia

arquivos usados:
*docker-compose
*Dockerfile

comando:
*docker-compose up -d

subir com docker e liberar porta de acesso
    curl -X POST "http://172.16.128.133:8000/executar-crew?nome=processos_error" -H "Content-Type: application/json" -d '{"pergunta": "qual processo esta com maior numero de linhas?"}'


> scripts com shell script que executam query e retornam a workflow na n8n

### CrewAI Pydantic FastApi | construção 
