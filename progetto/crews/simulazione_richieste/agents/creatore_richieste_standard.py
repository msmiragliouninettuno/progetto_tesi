from crewai import Agent

def genera():
    agente_CRS = Agent(
        role="Creatore richieste standard",
        goal="""
            {goal}
            """,
        verbose=True,
        memory=True,
        backstory=(
            """
            {backstory}
            """
        ),
        allow_delegation=False,
    )

    return agente_CRS



