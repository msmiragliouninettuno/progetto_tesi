from crewai import Task

def genera():
    revisiona_risposta_task = Task(
        description=(
            """
            1. Analizza il piano di esecuzione generato dall'agente pianificatore in risposta alla richiesta di supporto attuale.
            2. Analizza il report di esecuzione del piano per individuare eventuali problemi emersi tra la pianificazione e l'effettiva esecuzione degli step.
            3. Esamina i suggerimenti forniti in precedenza relativi a domande simili valutando in particolare il loro punteggio; tendi a scartare i suggerimenti
               con punteggio inferiore a 0,5.
            4. Dopo aver selezionato i suggerimenti precedenti, valuta se aggiungere ulteriori suggerimenti per affinare la struttura e la logica del piano, 
                tenendo conto del report di esecuzione. I nuovi suggerimenti NON DEVONO INCLUDERE DETTAGLI SPECIFICI come codici, nominativi, materie legati 
                alla domanda, ma piuttosto offrire passaggi utili per situazioni simili ma non identiche. Se ritieni che i suggerimenti esistenti siano già sufficienti, 
                non è necessario crearne di nuovi.
            5. Assicurati che i suggerimenti che fornisci restino all'interno delle capacità dell'agente che eseguirà il piano, senza richiedere, quindi, nuove 
                funzionalità o interventi esterni nello svolgere i vari passi del piano.
                Escludi qualsiasi suggerimento che menzioni problemi tecnici, errori di sistema o fattori esterni (es. inserimento ritardato dei dati o dimenticanze 
                degli sviluppatori): il piano viene eseguito da un agente che ha solo accesso ai dati di istituti, classi e studenti e non ha altri strumenti a 
                sua disposizione, quindi evita di suggerire modifiche che vadano oltre queste possibilità.
                Non suggerire azioni che prevedano la verifica dei dati tramite persone o gestionali esterni.
            6. Crea un output che integri i tuoi suggerimenti specifici con i suggerimenti usati in passato che ritieni rilevanti, restituendo un array in 
               formato JSON con:
                - eventuali suggerimenti elaborati non presenti in precedenza 
                - i suggerimenti riutilizzati
            7. L'output finale verrà aggiunto al prompt dell'agente pianificatore, migliorandone la performance per risolvere future richieste simili.
            
                        
            Questo è il ruolo dell'utente che ha posto la domanda:
            <ruolo_utente>
            {user_informations}
            </ruolo_utente>
            
            La richiesta di supporto è la seguente:
            <richiesta_supporto>
            {support_request}
            </richiesta_supporto>

            Il piano di esecuzione sviluppato è questo:
            <piano_esecuzione>
            {support_reasoning}
            </piano_esecuzione>

            Il risultato dell'esecuzione del piano:
            <esecuzione_piano>
            {support_execution}
            </esecuzione_piano>

            Ecco i suggerimenti dati in passato per domande simili:
            <suggerimenti_domande_simili>
            {previous_suggestions}
            </suggerimenti_domande_simili>

            Prompt dell'agente che redige il piano dell'esecuzione:
            <planning_agent_prompt>
            {planning_agent_prompt}
            </planning_agent_prompt>
            """
        ),
        expected_output=(
            """
            L'output atteso sarà SOLAMENTE un array in formato JSON, dove ciascun elemento rappresenta un suggerimento.
            Non aggiungere testo oltre al JSON.
            Ogni elemento dell'array può essere:
            - Un suggerimento nuovo: rappresentato da una stringa di testo che descrive il suggerimento specifico da aggiungere al piano di esecuzione.
            - Un suggerimento ripreso da esperienze passate: tutto l'oggetto che lo rappresenta in formato JSON.

            I suggerimenti nuovi NON DEVONO INCLUDERE DETTAGLI SPECIFICI come codici, nominativi, materie legati alla domanda, ma piuttosto offrire passaggi utili per situazioni simili ma non identiche.
            """
        ),
    )

    return revisiona_risposta_task