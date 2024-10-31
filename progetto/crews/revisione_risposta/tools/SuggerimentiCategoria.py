from typing import Optional
from crewai_tools import tool
import json
import os
import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db


@tool("Suggerimenti di categoria")
def suggerimenti_categoria(categoria: str) -> str:
    """
    Elenca l'insieme di suggerimenti relativi ad una categoria di domande del passato;
    PASSARE ALLO STRUMENTO i seguenti parametri:
    - categoria: str, la categoria della domanda

    esempio parametri:
    {
        categoria: "Studente mancante"
    }
    """

    try:
        conn = db.connect()

        
        SQL_QUERY = f""" 
                    SELECT	c.id, c.suggerimento, COUNT(*) AS occorrenze, AVG(punteggio) punteggio
                    FROM	memoria.esperienze_passate a JOIN
                            memoria.suggerimenti_esperienze b ON a.id = b.esperienza JOIN
                            memoria.suggerimenti_passati c On b.suggerimento = c.id
                    WHERE   c.obsoleto = 0 AND a.categoria = %s
                    GROUP BY c.id, c.suggerimento
                    ORDER BY punteggio DESC, occorrenze DESC
                    LIMIT   50;
                    """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY, (categoria,) )
        records = cursor.fetchall()

        db.closeConnection()

        if(len(records)>0):
            return json.dumps(records, indent=4)

        return f"Non ho trovato suggerimenti disponibili"
    except Exception as inst:
        db.closeConnection()
        return """Errore generico: Questo tool accetta in ingresso una categoria di domande del passato""" + str(inst)


