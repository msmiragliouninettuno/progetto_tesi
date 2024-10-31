from crewai import Task

def genera():
    creazione_richieste_standard_task = Task(
        description=(
            """
            {task_description}
            
            Ecco i dati:
            <data>
            {data}
            </data>
            """
        ),
        expected_output=(
            """
            {task_expected_output}
            """
        ),
    )

    return creazione_richieste_standard_task