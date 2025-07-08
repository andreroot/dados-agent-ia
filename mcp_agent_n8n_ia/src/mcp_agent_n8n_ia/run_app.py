from typing import Union

from fastapi import FastAPI, Query, Request
from mcp_agent_n8n_ia.crew import McpAgentN8NIa
from pydantic import BaseModel

app = FastAPI()
crew_instance = McpAgentN8NIa()

class Process(BaseModel):
    nome: str
    pergunta: Union[str, None] = None
    # price: float
    # tax: Union[float, None] = None

@app.post("/executar-crew/")
def executar_crew(nome: str = Query(..., description="Nome do processo")):
    # Executa o crew com o input recebido
    result = crew_instance.crew().kickoff(inputs={"nome": nome})
    return {"resultado": result}

@app.post("/executar-crew-data/")
async def executar_crew_data(process: Process):
    # Executa o crew com o input recebido
    # data = await request.json()  # Recebe o JSON enviado no corpo
    result = crew_instance.crew().kickoff(inputs=process.dict())
    return {"resultado": result}

# @app.post("/treinar-crew")
# def treinar_crew(n_iterations: int = Query(..., description="Número de iterações para treinar"),
#                  filename: str = Query(..., description="Nome do arquivo para salvar o modelo")):
#     pass