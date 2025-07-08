from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from mcp_agent_n8n_ia.tools.custom_tool import MyCustomToolInput, ConsultaProcessosErrorTool, ConsultaProcessosExecutadosTool
from crewai.tools import tool
import requests

from pydantic import BaseModel

class ProcessosResponse(BaseModel):
    status: str
    resultado: dict  # ou list, ou campos específicos conforme seu retorno

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


# # Create a knowledge source
# content = "Users name is John. He is 30 years old and lives in San Francisco."
# string_source = StringKnowledgeSource(content=content)

llm = LLM(
    model="gpt-4o-mini",
    temperature=0
)

@CrewBase
class McpAgentN8NIa:
    """McpAgentN8NIa crew"""
    def __init__(self, nome: str = "processos_executados"):
        self.nome = nome

    # agents: List[BaseAgent]
    # tasks: List[Task]
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    @tool
    def consulta_processos_executados(nome: str):
        """A simple tool that returns a greeting."""
        # nome = self.nome
        # ConsultaProcessosExecutadosTool(name="Consulta Processos Executados com sucesso", description="Consulta os processos executados com sucesso.", args_schema=MyCustomToolInput)
        if not nome:
            return "Por favor, forneça um nome para consulta."
        if nome not in ["processos_executados", "processos_error"]:
            return "Nome inválido. Use 'processos_executados' ou 'processos_com_erro'."
        # Exemplo com uma API pública, adapte para sua
        # http://172.16.128.133:5678/webhook/execute-python?processo=processos_error
        # http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados
        url = f"http://172.16.128.133:5678/webhook/execute-python?processo={nome}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            # Validação Pydantic
            validated = ProcessosResponse(status="ok", resultado=dados)
            return validated.model_dump()  # ou validated.model_dump() no Pydantic v2
        except Exception as e:
            validated = ProcessosResponse(status="erro", resultado={"erro": str(e)})
            return validated.model_dump()
        
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def especialista_em_monitoramento_remoto(self):
        return Agent(
            config=self.agents_config['especialista_em_monitoramento_remoto'], # type: ignore[index]
            llm=llm,
            # tools=[self.saudacao],
            tools=[self.consulta_processos_executados],
            verbose=True
        )

    # @agent
    # def reporting_analyst(self):
    #     return Agent(
    #         config=self.agents_config['reporting_analyst'], # type: ignore[index]
    #         verbose=True
    #     )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def processos_executados_tasks(self):
        return Task(
            config=self.tasks_config['processos_executados_tasks'], # type: ignore[index]
            agent=self.especialista_em_monitoramento_remoto(), # type: ignore[index]
            markdown=True,  # Enable markdown formatting for the final output
            output_file="report.md",
            tools=[self.consulta_processos_executados],             
        )

    # @task
    # def processos_erro_tasks(self):
    #     return Task(
    #         config=self.tasks_config['processos_error_tasks'], # type: ignore[index]
    #         agent=self.especialista_em_monitoramento_remoto(), # type: ignore[index]
    #         markdown=True,  # Enable markdown formatting for the final output
    #         output_file="report.md",
    #         tools=[self.consulta_processos_error],         
    #     )

    # @task
    # def reporting_task(self):
    #     return Task(
    #         config=self.tasks_config['especialista_em_monitoramento_remoto_task'], # type: ignore[index]
    #         output_file='report.md'
    #     )

    @crew
    def crew(self):
        """Creates the McpAgentN8NIa crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.especialista_em_monitoramento_remoto()], # Automatically created by the @agent decorator
            tasks=[self.processos_executados_tasks()], # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # knowledge_sources=[string_source], # Enable knowledge by adding the sources here
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    # result = crew.kickoff(inputs={"question": "What city does John live in and how old is he?"})
