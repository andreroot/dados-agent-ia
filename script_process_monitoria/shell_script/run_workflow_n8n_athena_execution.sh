#!/bin/bash

# Activa el entorno virtual
source /home/administrador/projetos/dados-agent-ia/.venv/bin/activate

cd /home/administrador/projetos/dados-agent-ia/script_process_monitoria/src/

python /home/administrador/projetos/dados-agent-ia/script_process_monitoria/src/run_workflow_n8n_athena.py execution

exit