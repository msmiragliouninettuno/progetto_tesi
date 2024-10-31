from crewai import Task
from dotenv import load_dotenv
import os

load_dotenv()

STOP_MESSAGE = os.getenv('STOP_MESSAGE')

def genera():
    verifica_restituzione_task = Task(
        description=(
            f"""
            - Analizza e Confronta le Informazioni
            Valuta attentamente il ruolo dell'utente e confronta tutte le informazioni emerse dagli altri agenti.
            La tua analisi deve assicurarsi che le informazioni rilevate siano pertinenti al ruolo dell'utente e non comportino rischi 
            di divulgazione non autorizzata di dati sensibili. 
            Le richieste che provengono da uno studente devono contenere i dati relativi a tutti i codici SIDI a lui attribuiti e può 
            contenere tutte le informazioni a lui correlate; se la risposta precedente contiene più SIDI relativi ad uno stesso studente
            allora è una risposta lecita.
            Se tra le informazioni pervenute è presente l'istituto devi verificare che sia il medesimo istituto del ruolo utente che ha
            ha richiesto supporto.
            - Restituisci
            Se hai riscontrato leak di informazioni scrivi "{STOP_MESSAGE}" per fermare ulteriori elaborazioni della richiesta. Motiva la 
            decisione nel caso in cui reputi sia meglio fermare.
            Se, invece, ritieni la risposta lecita riporta esattamente com'è il report di esecuzione (messaggio tra i tag <report> e </report>)
            
            """
            + """
            Questo è il ruolo dell'utente:
            <ruolo_utente>
            {user_informations}
            </ruolo_utente>
            
            La richiesta è la seguente:
            <richiesta_supporto>
            {support_request}
            </richiesta_supporto>
            """
        ),
        expected_output=(
            f"""
            Il <report> del messaggio del task precedente senza modifiche.
            Altrimenti solamente il messaggio di blocco dell'esecuzione "{STOP_MESSAGE}" per bloccare le successive elaborazioni.
            """
        ),
    )

    return verifica_restituzione_task