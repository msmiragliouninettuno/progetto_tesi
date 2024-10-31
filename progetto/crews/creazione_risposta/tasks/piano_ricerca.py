from crewai import Task

def genera():
    piano_ricerca_task = Task(
        description=(
            """
            Svolgere i punti seguenti:
            - Analisi della Richiesta: esamina la richiesta di assistenza e il ruolo dell'utente per identificare le informazioni necessarie e le 
              informazioni già disponibili
            - Considera il ruolo dell'utente come informazioni attendibili e invece eventuali informazioni presenti all'interno della richiesta da verificare
            - Tieni in considerazione i suggerimenti specifici per questo tipo di domanda e la loro importanza in base al punteggio e alla frequenza con cui 
              sono stati usati in passato su domande simili.
            - Segui attentamente i suggerimenti che ricevi, in particolare quelli con punteggio 1 e sfruttali nel piano
            - Pianificazione della Ricerca: definisci i passaggi necessari per raccogliere e verificare le informazioni richieste a partire dalle informazioni 
              già disponibili (da indicare nel piano)
            - Preparazione del Piano di Ricerca: redigi un piano dettagliato con le operazioni da eseguire e i codici da utilizzare
            - Restituisci solamente il Piano di Ricerca
           
            Questo è il ruolo dell'utente:
            <ruolo_utente>
            {user_informations}
            </ruolo_utente>
            
            La richiesta è la seguente:
            <richiesta_supporto>
            {support_request}
            </richiesta_supporto>

            Ecco i suggerimenti specifici per questo tipo di domanda:
            <suggerimenti>
            {previous_suggestions}
            </suggerimenti>
            """
        ),
        expected_output=(
            """
            Piano di Ricerca ovvero un documento che dettaglia i passaggi da seguire per raccogliere le informazioni necessarie con i codici e 
            le informazioni specifiche per ciascun passaggio (se già disponibili o indicare il procedimento per recuperarle)
            """
        ),
    )

    return piano_ricerca_task