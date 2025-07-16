#!/bin/bash

# Activa el entorno virtual
source /home/administrador/projetos/dados-agent-ia/.venv/bin/activate

cd /home/administrador/projetos/dados-agent-ia/script_process_monitoria/src/

#exemplo: python /home/administrador/projetos/dados-agent-ia/script_process_monitoria/src/run_workflow_n8n_insert_particularity.py  'via teams Luis - 11/07' '2025-07-11' 'erros_boleta_inflacao_futuro' 'IC-CC022-26' 'Rafael Campos'

python /home/administrador/projetos/dados-agent-ia/script_process_monitoria/src/run_workflow_n8n_insert_particularity.py  "$@"

exit
