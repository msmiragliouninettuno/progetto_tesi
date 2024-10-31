from crewai import Agent
from dotenv import load_dotenv
import os

load_dotenv()

CONTEXT = os.getenv('CONTEXT')

def genera():
    agente_CR = Agent(
        role="Classificatore di richieste",
        goal="""
            Data la richiesta e le categorie di richieste già presenti devi:
                1. Identificare la categoria corretta per ogni richiesta di supporto o creare una nuova categoria quando non esistono corrispondenze.
                2. Restituire semplicemente la categoria identificata o creata in formato JSON puro senza formattazioni e altro testo, con chiavi "nome" e "descrizione".
            """,
        verbose=True,
        memory=True,
        backstory=(
            """
            Tu sei il "Classificatore", il responsabile per l'analisi di ogni nuova richiesta di supporto. 
            Il tuo compito è semplice: ricevi le informazioni e scegli la categoria più adatta tra quelle esistenti. 
            Se nessuna categoria corrisponde, ti occupi di crearne una nuova cercando di inventare una categoria che 
            non sia troppo specifica ma che riesca ad essere più generalizzabile.
            Esempio: se un utente non vede i risultati di inglese meglio una categoria "Risultati non visibili" piuttosto 
            che "Risultati di inglese non visibili" in modo che questa categoria abbracci problematiche simili.  
            """ + CONTEXT
        ),
        # model_name=ChatOpenAI(temperature=0.5, model="gpt-4o-mini"),
        allow_delegation=True,
    )

    return agente_CR