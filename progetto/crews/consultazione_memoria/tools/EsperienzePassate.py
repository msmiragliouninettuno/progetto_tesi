from typing import Optional
from crewai_tools import tool
import json
import os
import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db


@tool("Esperienze passate")
def esperienze_passate(categoria: str) -> str:
    """
    Elenca domande passate relative ad una specifica categoria;
    PASSARE ALLO STRUMENTO i seguenti parametri:
    - categoria: str, una specifica categoria

    esempio parametri:
    {
        categoria: "Problema visualizzazione risultati"
    }
    """

    try:
        conn = db.connect()

        
        # SQL_QUERY = f""" 
        #             SELECT	b.id, b.utente, b.domanda
        #             FROM	memoria.categorie a JOIN
        #                     memoria.esperienze_passate b ON a.nome = b.categoria OR a.macro_categoria = b.categoria JOIN
        #                     memoria.suggerimenti_esperienze c ON b.id = c.esperienza
        #             WHERE   b.obsoleta = 0 AND a.nome = %s
        #             ORDER BY b.data_inserimento DESC
        #             LIMIT   20;
        #             """
        
        SQL_QUERY = f""" 
                    SELECT	b.id, b.utente, b.domanda, AVG(punteggio) AS punteggio
                    FROM	memoria.categorie a JOIN
                            memoria.esperienze_passate b ON a.nome = b.categoria OR a.macro_categoria = b.categoria JOIN
                            memoria.suggerimenti_esperienze c ON b.id = c.esperienza AND c.punteggio > 0.5
                    WHERE   b.obsoleta = 0 AND a.nome = %s
                    GROUP BY b.id, b.utente, b.domanda, b.data_inserimento
                    ORDER BY punteggio DESC, b.data_inserimento DESC
                    LIMIT   20;
                    """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY, (categoria, ))
        records = cursor.fetchall()

        db.closeConnection()

        if(len(records)>0):
            return json.dumps(records, indent=4)

        return f"Non esistono ancora esperienze passate per la categoria {categoria}"
    except Exception as inst:
        db.closeConnection()
        return """Errore generico: Questo tool accetta in ingresso una categoria di domande di assistenza. """ + str(inst)


