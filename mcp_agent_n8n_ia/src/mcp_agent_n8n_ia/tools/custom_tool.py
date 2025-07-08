from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str):
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."



class ConsultaProcessosExecutadosTool(BaseTool):
    name: str = "Consulta de processos via api"
    description: str = (
        "Faz uma chamada a uma API externa para buscar dados."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str):
        # Exemplo com uma API pública, adapte para sua
        # http://172.16.128.133:5678/webhook/execute-python?processo=processos_error
        # http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados
        url = f"http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  # ou response.text se preferir
        except Exception as e:
            return f"Erro ao buscar API: {e}"

class ConsultaProcessosErrorTool(BaseTool):
    name: str = "Consulta de processos"
    description: str = (
        "Faz uma chamada a uma API externa para buscar dados."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str):
        # Exemplo com uma API pública, adapte para sua
        # http://172.16.128.133:5678/webhook/execute-python?processo=processos_error
        # http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados
        url = f"http://172.16.128.133:5678/webhook/execute-python?processo=processos_error"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  # ou response.text se preferir
        except Exception as e:
            return f"Erro ao buscar API: {e}"        