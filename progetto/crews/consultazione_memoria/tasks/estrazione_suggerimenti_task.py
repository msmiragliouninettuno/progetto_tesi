from crewai import Task

def genera():
    estrazione_suggerimenti_task = Task(
        description=(
            """
            1. Ricevi dal task precedente un elenco di id di domande simili alla domanda attuale, selezionate dall'agente di consultazione esperienze passate simili.
            2. Estrai i suggerimenti forniti da tutte queste domande e analizza la loro numerosità.
            3. Restituisci il JSON contenente i suggerimenti con il loro punteggio e la loro frequenza di utilizzo.

            Hai a disposizione il tool "Suggerimenti passati" che prende in ingresso una lista di id di domande e restituisce un JSON con 
            l'elenco di tutti i suggerimenti di quelle domande ordinandoli per punteggio decrescente e frequenza di utilizzo.
                        
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
            Un JSON contenente i suggerimenti relativi agli id domanda che ti sono stati forniti e per ognuno di essi il punteggio e frequenza di utilizzo.
            Se non hai id domanda o non trovi suggerimenti allora restituisci un array vuoto JSON.
            """
        ),
    )

    return estrazione_suggerimenti_task