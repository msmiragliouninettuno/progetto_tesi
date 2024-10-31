from crewai import Agent
from dotenv import load_dotenv
import os

from crews.consultazione_memoria.tools.EsperienzePassate import esperienze_passate
ep_tool = esperienze_passate

load_dotenv()

CONTEXT = os.getenv('CONTEXT')

def genera():
    agente_SR = Agent(
        role="Selezionatore di esperienze simili",
        goal="Identificare e restituire domande precedenti della stessa categoria che risultano più simili a quella attuale.",
        verbose=True,
        memory=True,
        backstory=(
            """
            Sei un agente esperto nel recuperare esperienze precedenti. Il tuo compito principale è esaminare tutte le richieste 
            di supporto passate appartenenti alla stessa categoria della domanda attuale. Sei specializzato nel trovare quelle che 
            contengono problematiche simili, così da facilitare l'uso delle conoscenze acquisite in situazioni analoghe.

            Hai a disposizione il tool "Esperienze passate" che prende in ingresso una categoria e ti restituisce un JSON con un 
            elenco di domande della stessa categoria.
            """ + CONTEXT
        ),
        # model_name=ChatOpenAI(temperature=0.5, model="gpt-4o-mini"),
        allow_delegation=True,
        tools=[ep_tool],

    )

    return agente_SR