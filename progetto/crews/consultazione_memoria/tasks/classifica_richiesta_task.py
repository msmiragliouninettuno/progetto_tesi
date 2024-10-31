from crewai import Task

def genera():
    classifica_richiesta_task = Task(
        description=(
            """
            Analizza il contenuto della richiesta confrontandola con uno storico di categorie preesistenti. 
            Se la richiesta corrisponde a una categoria esistente, assegna la richiesta a quella categoria. 
            Se non ci sono corrispondenze, crea una nuova categoria che rappresenti al meglio la richiesta.
            Una categoria è composta da un titolo con qualche parola chiave e una breve descrizione.
                        
            Questo è il ruolo dell'utente:
            <ruolo_utente>
            {user_informations}
            </ruolo_utente>
            
            La richiesta è la seguente:
            <richiesta_supporto>
            {support_request}
            </richiesta_supporto>

            Queste sono le categorie già esistenti:
            <categorie_esistenti>
            {request_categories}
            </categorie_esistenti>
            """
        ),
        expected_output=(
            """
            La categoria scelta o una nuova categoria in formato JSON puro senza formattazioni e altro testo, con chiavi "nome" (qualche parola chiave) e "descrizione" (breve descrizione del problema affrontato).
            """
        ),
    )

    return classifica_richiesta_task
