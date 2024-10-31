from crewai import Task

def genera():
    esecuzione_piano_ricerca_task = Task(
        description=(
            """
            Svolgere i punti seguenti:
            - Ricezione e Analisi del Piano di Ricerca: considera il piano di ricerca preparato nel task precedente e analizzalo per comprendere i passaggi da seguire
            - Raccolta dati: raccogli le informazioni ottenute, integra i dati e verifica la loro accuratezza prima di preparare il risultato finale
            - Redigi un Report Finale con le informazioni complete e aggregate per dare una visione generale
            """
        ),
        expected_output=(
            """
            Report Finale ovvero un JSON di riepilogo pronto con le informazioni aggregate ma complete che risultino utili per formulare una risposta alla richiesta.
            Restituisci tutte le informazioni potenzialmente utili per rispondere alla richiesta MA ASTIENITI DAL FARE CONSIDERAZIONI.
            Restituisci un quantitativo di dati che non sia troppo esteso ma comunque sufficiente per fare anche valutazioni più generali.
            Racchiudi il Report Finale tra i tag <report> e </report>.

            Inoltre, aggiungi in coda una breve lista di tutte le operazioni che hai dovuto compiere compresi eventuali errori, problemi riscontrati e se sei
            riuscito a completare con successo il piano oppure non hai trovato i dati sperati.
            Racchiudi questa lista con i tag <execution_details> e </execution_details>
            """
        ),
    )

    return esecuzione_piano_ricerca_task