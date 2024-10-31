import json

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

class CrewCreazioneRisposta:
    def __init__(self):
        self.crew = None
        self.agents = {}
        self.tasks = {}

    def genera(self):
        # agenti
        import crews.creazione_risposta.agents.verifica_supporto as agente_verifica_supporto
        import crews.creazione_risposta.agents.pianificazione_ricerca as agente_pianificazione_ricerca
        import crews.creazione_risposta.agents.esecuzione_ricerca as agente_esecuzione_ricerca
        import crews.creazione_risposta.agents.sintesi_risposta as agente_sintesi_risposta

        agente_AVS = agente_verifica_supporto.genera()
        agente_APRI = agente_pianificazione_ricerca.genera()
        agente_AER = agente_esecuzione_ricerca.genera()
        agente_ASR = agente_sintesi_risposta.genera()

        anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
        openai_llm = ChatOpenAI(temperature=0.4, model="gpt-4o")


        agente_AVS.llm = anthropic_llm
        agente_APRI.llm = anthropic_llm
        agente_AER.llm = openai_llm
        agente_ASR.llm = openai_llm

        self.agents = {
            "verifica_supporto": agente_AVS,
            "pianificazione_ricerca": agente_APRI,
            "esecuzione_ricerca": agente_AER,
            "sintesi_risposta": agente_ASR,
        }

        # task
        import crews.creazione_risposta.tasks.piano_ricerca as task_piano_ricerca
        import crews.creazione_risposta.tasks.esecuzione_piano_ricerca as task_esecuzione_piano_ricerca
        import crews.creazione_risposta.tasks.verifica_restituzione as task_verifica_restituzione
        import crews.creazione_risposta.tasks.formulazione_risposta as task_formulazione_risposta

        task_PR = task_piano_ricerca.genera()
        task_PR.agent = agente_APRI

        task_EPR = task_esecuzione_piano_ricerca.genera()
        task_EPR.agent = agente_AER

        task_VR = task_verifica_restituzione.genera()
        task_VR.agent = agente_AVS

        task_FR = task_formulazione_risposta.genera()
        task_FR.agent = agente_ASR

        self.tasks = {
            "piano_ricerca_task": task_PR,
            "esecuzione_piano_ricerca_task": task_EPR,
            "verifica_restituzione_task": task_VR,
            "formulazione_risposta_task": task_FR,
        }

        # crew
        from crewai import Crew

        crew = Crew(
            agents=[agente_AVS, agente_APRI, agente_AER, agente_ASR],
            tasks=[
                task_PR,
                task_EPR,
                task_VR,
                task_FR,
            ],
            # process=Process.hierarchical,
            # manager_agent=assistente_capo,
            # manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"),
        )

        self.crew = crew
