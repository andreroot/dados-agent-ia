from crewai import Agent
from textwrap import dedent
from langchain_groq import ChatGroq
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, WebsiteSearchTool


load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


groq_api_key = os.environ["GROQ_API_KEY"]
# groq_api_key = st.secrets["GROQ_API_KEY"]

# tools
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()


class TravelAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(
            model="openai/gpt-3.5-turbo", max_tokens=4000, temperature=0.2
        )
        self.groq = ChatGroq(
            temperature=0, groq_api_key=groq_api_key, model="groq/llama3-8b-8192"
        )

        # Instantiate the tools
        # self.search_tool = SearchTools().search_internet
        self.calculator_tool = CalculatorTools().calculate

    def expert_engeiner_data(self):
        return Agent(
            role="Especialista em Monitoramento Remoto de processos executados em máquinas remotas",
            backstory=dedent(
                """Coletar informações sobre o status dos processos internos executados em uma máquina remota por meio 
      de API, para conseguir essa informação conecta no enedereço http://172.16.128.133:5678/webhook/execute-python.
                """
            ),
            goal=dedent("""
                        Um agente altamente treinado em administração de sistemas e automação, com profundo conhecimento em processos
      internos que rodam em servidores Linux e Windows. Ele é capaz de se conectar a APIs internas seguras para buscar 
      informações em tempo real sobre status, falhas e execução dos serviços, garantindo confiabilidade e resposta rápida.
                        """),
            tools=[search_tool, web_rag_tool],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    # def city_selection_expert(self):
    #     return Agent(
    #         role="City Selection Expert",
    #         backstory=dedent(
    #             """Expert at analyzing travel data to pick ideal destinations"""
    #         ),
    #         goal=dedent(
    #             """Select the best cities based on weather, season, prices, and traveler interests"""
    #         ),
    #         tools=[search_tool, web_rag_tool],
    #         verbose=True,
    #         llm=self.OpenAIGPT35,
    #     )

    # def local_tour_guide(self):
    #     return Agent(
    #         role="Local Tour Guide",
    #         backstory=dedent("""Knowledgeable local guide with extensive information
    #     about the city, it's attractions and customs"""),
    #         goal=dedent("""Provide the BEST insights about the selected city"""),
    #         tools=[search_tool, web_rag_tool],
    #         verbose=True,
    #         llm=self.OpenAIGPT35,
    #     )