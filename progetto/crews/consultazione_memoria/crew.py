import os
import sys
from langchain_openai import ChatOpenAI

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)
from progetto.database.database import db


class CrewConsultazioneMemoria:
    def __init__(self):
        self.crew = None
        self.agents = {}
        self.tasks = {}

    def genera(self):
        # agenti
        import crews.consultazione_memoria.agents.classificatore_richiesta as classificatore_richiesta
        import crews.consultazione_memoria.agents.selezionatore_esperienze as selezionatore_esperienze
        import crews.consultazione_memoria.agents.estrattore_suggerimenti as estrattore_suggerimenti

        agente_CR = classificatore_richiesta.genera()
        agente_SES = selezionatore_esperienze.genera()
        agente_ESU = estrattore_suggerimenti.genera()

        # anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
        openai_llm = ChatOpenAI(temperature=0.4, model="gpt-4o")

        agente_CR.llm = openai_llm
        agente_SES.llm = openai_llm
        agente_ESU.llm = openai_llm

        self.agents = {
            "classificatore_richiesta": agente_CR,
            "selezionatore_esperienze": agente_SES,
            "estrattore_suggerimenti": agente_ESU,
        }

        # task
        import crews.consultazione_memoria.tasks.classifica_richiesta_task as classifica_richiesta_task
        import crews.consultazione_memoria.tasks.seleziona_esperienze_task as seleziona_esperienze_task
        import crews.consultazione_memoria.tasks.estrazione_suggerimenti_task as estrazione_suggerimenti_task

        task_CR = classifica_richiesta_task.genera()
        task_CR.agent = agente_CR

        task_SES = seleziona_esperienze_task.genera()
        task_SES.agent = agente_SES

        task_ESU = estrazione_suggerimenti_task.genera()
        task_ESU.agent = agente_ESU


        self.tasks = {
            "classifica_richiesta_task": task_CR,
            "seleziona_esperienze_task": task_SES,
            "estrazione_suggerimenti_task": task_ESU,
        }

        # crew
        from crewai import Crew

        crew = Crew(
            agents=[agente_CR, agente_SES, agente_ESU],
            tasks=[
                task_CR, task_SES, task_ESU
            ],
            # process=Process.hierarchical,
            # manager_agent=assistente_capo,
            # manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"),
        )
      
        self.crew = crew

