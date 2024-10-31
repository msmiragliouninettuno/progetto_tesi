from crewai import Agent
from dotenv import load_dotenv
import os

from crews.consultazione_memoria.tools.SuggerimentiPassati import suggerimenti_passati
sp_tool = suggerimenti_passati

load_dotenv()

CONTEXT = os.getenv('CONTEXT')

def genera():
    agente_SR = Agent(
        role="Estrattore suggerimenti dalle esperienze passate",
        goal="Prelevare i suggerimenti dalle esperienze simili e fornire un report con i suggerimenti più comuni e la loro frequenza.",
        verbose=True,
        memory=True,
        backstory=(
            """
            Sei uno specialista nell'estrarre i suggerimenti dalle esperienze passate. Avendo la lista delle domande simili identificate, 
            sei responsabile di estrarre i suggerimenti forniti in quelle circostanze, prestando particolare attenzione a quelli che sono 
            stati utilizzati più frequentemente o con successo.
            
            Hai a disposizione il tool "Suggerimenti passati" che prende in ingresso una lista di id di domande e restituisce un JSON con 
            l'elenco di tutti i suggerimenti di quelle domande ordinandoli per frequenza decrescente.
            """ + CONTEXT
        ),
        # model_name=ChatOpenAI(temperature=0.5, model="gpt-4o-mini"),
        allow_delegation=True,
        tools=[sp_tool],

    )

    return agente_SR