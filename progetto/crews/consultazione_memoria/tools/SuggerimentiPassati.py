from typing import Optional
from crewai_tools import tool
import json
import os
import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db


@tool("Suggerimenti passati")
def suggerimenti_passati(id_domande: list) -> str:
    """
    Elenca l'insieme di suggerimenti relativi ad un elenco di domande del passato;
    PASSARE ALLO STRUMENTO i seguenti parametri:
    - id_domande: list, una lista di id di domande passate

    esempio parametri:
    {
        id_domande: [1,5,8,33]
    }
    """

    try:
        conn = db.connect()

        
        SQL_QUERY = f""" 
                    SELECT	c.id, c.suggerimento, COUNT(*) AS occorrenze, AVG(punteggio) punteggio
                    FROM	memoria.suggerimenti_esperienze b JOIN
                            memoria.suggerimenti_passati c On b.suggerimento = c.id
                    WHERE   c.obsoleto = 0 AND b.esperienza IN ({', '.join(['%s'] * len(id_domande))})
                    GROUP BY c.id, c.suggerimento
                    HAVING AVG(punteggio) >= 0.5
                    ORDER BY punteggio DESC, occorrenze DESC
                    LIMIT   20;
                    """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY, tuple(id_domande), )
        records = cursor.fetchall()

        db.closeConnection()

        if(len(records)>0):
            return json.dumps(records, indent=4)

        return f"Non ho trovato suggerimenti disponibili"
    except Exception as inst:
        db.closeConnection()
        return """Errore generico: Questo tool accetta in ingresso una lista di domande del passato""" + str(inst)


