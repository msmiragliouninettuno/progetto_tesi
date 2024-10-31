from crewai import Task

def genera():
    revisiona_risposta_task = Task(
        description=(
            """
            Valutare i suggerimenti forniti dall'agente revisore della risposta. 
            L'obiettivo è esaminare ciascun suggerimento e garantire che esso possa essere eseguito dall'agente incaricato dell'esecuzione del piano.
            Tale agente può svolgere solo queste mansioni:
            - reperire informazioni specifiche su uno studente, una classe o un istituto
            - non ha accesso a siti esterni
            - non può incrociare dati da fonti diverse. Dovrai inoltre identificare e scartare i suggerimenti ridondanti, preferendo suggerimenti già forniti 
            nel passato per evitare duplicazioni nel database.

            Utilizza il tool "Suggerimenti di categoria" in dotazione per reperire le informazioni su tutti i suggerimenti già esistenti.
            
            In questo modo dovrai:
            - scartare i suggerimenti dati dal revisore che contengono dati troppo specifici ad una richiesta (codici sidi espliciti, nominativi, materie, ecc...)
            - scartare i suggerimenti dati dal revisore che siano ridondanti tra loro 
            - scartare i suggerimenti dati dal revisore che rispecchino suggerimenti passati con punteggio inferiore a 0.5.
            - se un nuovo suggerimento (un suggerimento senza id) ha lo stesso contenuto informativo di un suggerimento già esistente devi rimpiazzarlo con l'id di quest'ultimo
            
            Ecco la categoria della domanda per cui il revisore ha fornito suggerimenti:
            <category>
            {request_category}
            </category>
            """
        ),
        expected_output=(
            """
            L'output atteso sarà SOLAMENTE un array semplice, senza chiavi, in formato JSON e dovrà contentere:
            - solamente l'id per i suggerimenti riutilizzati dal passato applicabili dall'agente esecutore del piano, oppure
            - solamente la stringa dei suggerimenti nuovi che ritieni validi (non ridondanti e applicabili dall'agente esecutore del piano).
            L'array finale dovrà includere solo suggerimenti da aggiungere al piano di esecuzione e che possono essere direttamente eseguiti dall'agente esecutore.
            
            Tale agente può svolgere solo queste mansioni:
            - reperire informazioni specifiche su uno studente, una classe o un istituto
            - non ha accesso a siti esterni
            - non può incrociare dati da fonti diverse. Dovrai inoltre identificare e scartare i suggerimenti ridondanti, preferendo suggerimenti già forniti 
            nel passato per evitare duplicazioni nel database. 

            Non aggiungere testo oltre al JSON.

            Esempio di output:
            [12, 1, "Suggerimento nuovo 1", 55, "Suggerimento nuovo 2"]
            """
        ),
    )

    return revisiona_risposta_task