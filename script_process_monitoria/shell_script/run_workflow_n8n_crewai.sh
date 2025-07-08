#!/bin/bash

# Ative o ambiente virtual, se necessário
source /home/administrador/projetos/dados-agent-ia/mcp_agent_n8n_ia/.venv/bin/activate

# Caminho do script Python que executa o crew
SCRIPT_PATH="/home/administrador/projetos/dados-agent-ia/mcp_agent_n8n_ia/src/mcp_agent_n8n_ia/run_app.py"

# Parâmetro para o crew (exemplo: processos_executados ou processos_error)
NOME_PROCESSO="$1"

# Executa o script Python passando o parâmetro
python "$SCRIPT_PATH" "$NOME_PROCESSO"