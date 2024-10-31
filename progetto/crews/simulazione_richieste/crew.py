from langchain_openai import ChatOpenAI

class CrewSimulazioneRichieste:
    def __init__(self):
        self.crew = None
        self.agents = {}
        self.tasks = {}

    def genera(self):
        # agenti
        import crews.simulazione_richieste.agents.creatore_richieste_standard as creatore_richieste_standard
        import crews.simulazione_richieste.agents.simulatore_richieste_umane as simulatore_richieste_umane

        agente_CRS = creatore_richieste_standard.genera()
        agente_SRU = simulatore_richieste_umane.genera()

        # anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
        openai_llm = ChatOpenAI(temperature=0.5, model="gpt-4o")

        agente_CRS.llm = openai_llm
        agente_SRU.llm = openai_llm

        self.agents = {
            "creatore_richieste_standard": agente_CRS,
            "simulatore_richieste_umane": agente_SRU,
        }

        # task
        import crews.simulazione_richieste.tasks.creazione_richieste_standard as creazione_richieste_standard
        import crews.simulazione_richieste.tasks.simulazione_richieste_umane as simulazione_richieste_umane

        task_CRS = creazione_richieste_standard.genera()
        task_CRS.agent = agente_CRS

        task_SRU = simulazione_richieste_umane.genera()
        task_SRU.agent = agente_SRU

        self.tasks = {
            "creazione_richieste_standard_task": task_CRS,
            "simulazione_richieste_umane_task": task_SRU,
        }

        # crew
        from crewai import Crew

        crew = Crew(
            agents=[agente_CRS, agente_SRU],
            tasks=[task_CRS, task_SRU],
            # process=Process.hierarchical,
            # manager_agent=assistente_capo,
            # manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"),
        )

        self.crew = crew
