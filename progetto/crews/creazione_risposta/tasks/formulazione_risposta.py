from crewai import Task
from dotenv import load_dotenv
import os

load_dotenv()

STOP_MESSAGE = os.getenv('STOP_MESSAGE')

def genera():
    formulazione_risposta_task = Task(
        description=(
            f"""
            Se arriva "{STOP_MESSAGE}" allora restituisci la frase "Non è possibile accedere ai dati richiesti".
            Altrimenti svolgere i punti seguenti:
            - Analisi delle Informazioni Raccolte:
            Ricevi e analizza i dati aggregati forniti dall'agente AER.
            Comprendi il contesto e il contenuto delle informazioni raccolte.
            
            - Interpretazione della Richiesta:
            Rifletti sul motivo possibile alla base della richiesta dell'utente, considerando anche aspetti che potrebbero non essere esplicitamente menzionati.
            Anticipa eventuali problemi o dettagli che l'utente potrebbe non aver notato o compreso appieno.
            
            - Elaborazione e Sintesi:
            Organizza le informazioni in modo logico e coerente.
            Formula una risposta chiara e risolutiva, andando oltre la semplice risposta alla domanda, includendo spiegazioni o avvertenze utili.
            
            - Formulazione di Ipotesi e Interpretazioni:
            Se necessario, fai ipotesi informate non solo per colmare eventuali lacune nei dati, ma anche per spiegare il perché della richiesta o per evidenziare potenziali problematiche o opportunità che l'utente potrebbe non aver considerato.
            
            - Preparazione della Risposta Finale:
            Redigi una risposta ben strutturata che non solo risponda alla richiesta, ma offra anche valore aggiunto tramite interpretazioni e suggerimenti.
            Presenta la risposta in modo chiaro e comprensibile, con eventuali ipotesi e interpretazioni ben argomentate.
            NON RIPORTARE NELLA RISPOSTA eventuali codici classe (codice numerico di 12 caratteri) perché è un identificativo interno che l'utente non deve conoscere.
            NON dare soluzioni o suggerimenti che riguardano il sito web su cui non hai alcuna conoscenza in merito: basati solo sui dati reali che ti sono stati forniti.
        
            - Revisione e Consegna:
            Rivedi la risposta per garantire accuratezza, chiarezza e valore aggiunto.
            Consegna la risposta finale, assicurandoti che sia completa e risolutiva, affrontando anche aspetti impliciti o meno evidenti.
            """+
            """
            Questa è la richiesta:
            <richiesta_supporto>
            {support_request}
            </richiesta_supporto>
            """
        ),
        expected_output=(
            """
            Risposta accurata e chiara alla richiesta di assistenza formulata dall'utente.
            """
        ),
    )

    return formulazione_risposta_task