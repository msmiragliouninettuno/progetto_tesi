import os
import sys
from langchain_openai import ChatOpenAI

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db

class CrewRevisioneRisposta:
    def __init__(self):
        self.crew = None
        self.agents = {}
        self.tasks = {}

    def genera(self):
        # agenti
        import crews.revisione_risposta.agents.revisore_risposta as revisore_risposta
        import crews.revisione_risposta.agents.controllore_suggerimenti as controllore_suggerimenti

        agente_RR = revisore_risposta.genera()
        agente_CS = controllore_suggerimenti.genera()

        # anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
        openai_llm = ChatOpenAI(temperature=0.4, model="gpt-4o")

        agente_RR.llm = openai_llm
        agente_CS.llm = openai_llm

        self.agents = {
            "revisore_risposta": agente_RR,
            "controllore_suggerimenti": agente_CS,
        }

        # task
        import crews.revisione_risposta.tasks.revisiona_risposta_task as revisiona_risposta_task
        import crews.revisione_risposta.tasks.controlla_suggerimenti as controlla_suggerimenti

        task_RR = revisiona_risposta_task.genera()
        task_RR.agent = agente_RR

        task_CS = controlla_suggerimenti.genera()
        task_CS.agent = agente_RR

        self.tasks = {
            "revisiona_risposta_task": task_RR,
            "controlla_suggerimenti_task": task_CS,
        }

        # crew
        from crewai import Crew

        crew = Crew(
            agents=[agente_RR, agente_CS],
            tasks=[task_RR, task_CS],
            # process=Process.hierarchical,
            # manager_agent=assistente_capo,
            # manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"),
        )

        self.crew = crew
