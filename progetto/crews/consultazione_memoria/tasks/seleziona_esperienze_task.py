from crewai import Task

def genera():
    seleziona_esperienze_task = Task(
        description=(
            """
            1. Ricevi una richiesta di supporto di un particolare utente e la categoria che identifica la tipologia della richiesta.
            2. Seleziona le domande precedenti della stessa categoria, trovando quelle più simili basandoti su parole chiave, contesto e dettagli del problema e punteggio migliore.
                Cerca problematiche simili senza confrontare dati specifici ma concentrandoti sul tipo di problema posto.
            3. Restituisci un JSON con un elenco degli id delle domande simili.

            Hai a disposizione il tool "Esperienze passate" che prende in ingresso una categoria e ti restituisce un JSON con un elenco di domande della stessa 
            categoria.
                        
            Questo è il ruolo dell'utente che ha posto la domanda:
            <ruolo_utente>
            {user_informations}
            </ruolo_utente>
            
            La richiesta di supporto attuale è la seguente:
            <richiesta_supporto>
            {support_request}
            </richiesta_supporto>
            """
        ),
        expected_output=(
            """
            L'elenco degli id delle domande passate che siano simili alla richiesta attuale in base a parole chiave, contesto e dettagli del problema e punteggio migliore.
            Se non ci sono domande passate simili allora restituisci un array vuoto JSON.
            """
        ),
    )

    return seleziona_esperienze_task