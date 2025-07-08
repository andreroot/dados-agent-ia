# Dockerfile
FROM python:3.11-slim

# Instala dependências do sistema (ajuste conforme necessário)
RUN apt-get update && apt-get install -y build-essential

# Cria diretório de trabalho
WORKDIR /app/src

# Copia os arquivos do projeto
# COPY ./src /app/src
# COPY ./pyproject.toml /app/pyproject.toml
# COPY ./uv.lock /app/uv.lock


# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install crewai fastapi uvicorn pydantic requests pyyaml

# Expõe a porta do FastAPI
EXPOSE 8000

# RUN sysctl fs.inotify.max_user_watches=524288

# Comando para rodar o FastAPI com reload desabilitado (produção)
CMD ["uvicorn", "mcp_agent_n8n_ia.run_app:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["ls -all /app/src/"]