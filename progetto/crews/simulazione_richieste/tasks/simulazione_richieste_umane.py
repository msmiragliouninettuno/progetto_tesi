from crewai import Task

def genera():
    revisiona_risposta_task = Task(
        description=(
            """
            Dato un json in ingresso dal task precedente umanizza le richieste in esso contenute in questo modo:
            - riformula la richiesta scegliendo se rimuovere alcuni dati relativi allo studente; non mantenere sempre tutte le informazioni
            - mantieni sempre il codice sidi
            - rendi le richieste più reali introducendo errori di battitura o distrazione nel riportare i dati 
                (esempio sbagliando a digitare il nominativo, sbagliare la classe o la sezione o l'indirizzo)
            - rendi le richieste diverse
            - NON INVENTARE MAI UN CODICE SIDI FALSO
            
            Restituisci solo il JSON senza frasi aggiuntive.
            """
        ),
        expected_output=(
            """
            Il JSON in ingresso con le richieste riformulate in questo modo:
            - riformula la richiesta scegliendo se rimuovere alcuni dati relativi allo studente; non mantenere sempre tutte le informazioni
            - mantieni sempre il codice sidi
            - rendi le richieste più reali introducendo errori di battitura o distrazione nel riportare i dati 
                (esempio sbagliando a digitare il nominativo, sbagliare la classe o la sezione o l'indirizzo)
            - rendi le richieste diverse
            - aggiungi nel json la voce "modifiche" per indicare ciò che hai modificato rispetto alla richiesta originale
            - NON INVENTARE MAI UN CODICE SIDI FALSO

            Restituisci solo il JSON senza frasi aggiuntive.
            """
        ),
    )

    return revisiona_risposta_task