from typing import Any, Optional
from pydantic import Field

from crewai_tools import tool
import json
import os
import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db


@tool("Informazioni istituto (II)")
def informazioni_istituto(istituto: str, anno: int) -> str:
    """
    Estrae i dati dettagliati di un particolare istituto, ovvero l'elenco delle classi e principali informazioni;

    Lo strumento accetta in ingresso i seguenti parametri:
    - istituto: str, il meccanografico di istituto
    - anno: int, parametro opzionale contenente l'anno di riferimento, se non necessario passare -1

    esempio parametri:
    {
        istituto: "CZIS000000",
        anno: 2024
    }

    altro esempio parametri:
    {
        istituto: "CZIC000000",
        anno: -1
    }
    """

    try:
        meccanografico = istituto

        conn = db.connect()

        # se non mi viene passato l'anno allora prendo i dati con l'ultimo anno disponibile
        if anno == -1:
            SQL_QUERY = f""" 
                        SELECT	b.anno AS anno
                        FROM	istituti.istituti a JOIN
                                istituti.studenti_gruppi b ON a.meccanografico = b.istituto
                        WHERE	b.istituto = %s
                        ORDER BY b.anno DESC
                        LIMIT 1
                        """

            cursor = conn.cursor(dictionary=True)
            cursor.execute(SQL_QUERY, (meccanografico,))
            record = cursor.fetchone()
            if record is None:
                return f"L'istituto {meccanografico} non sembra avere dati disponibili in alcun anno"
            anno = record['anno']

        SQL_QUERY = f""" 
                    SELECT	b.istituto, a.nome AS nome_istituto, b.anno, b.id AS codice_classe, 
                            b.grado, 
                            CASE 
                                WHEN b.grado = 1 THEN 'Classe Prima Scuola Primaria'
                                WHEN b.grado = 2 THEN 'Classe Seconda Scuola Primaria'
                                WHEN b.grado = 3 THEN 'Classe Terza Scuola Primaria'
                                WHEN b.grado = 4 THEN 'Classe Quarta Scuola Primaria'
                                WHEN b.grado = 5 THEN 'Classe Quinta Scuola Primaria'
                                WHEN b.grado = 6 THEN 'Classe Prima Scuola Secondaria di I grado'
                                WHEN b.grado = 7 THEN 'Classe Seconda Scuola Secondaria di I grado'
                                WHEN b.grado = 8 THEN 'Classe Terza Scuola Secondaria di I grado'
                                WHEN b.grado = 9 THEN 'Classe Prima Scuola Secondaria di II grado'
                                WHEN b.grado = 10 THEN 'Classe Seconda Scuola Secondaria di II grado'
                                WHEN b.grado = 11 THEN 'Classe Terza Scuola Secondaria di II grado'
                                WHEN b.grado = 12 THEN 'Classe Quarta Scuola Secondaria di II grado'
                                WHEN b.grado = 13 THEN 'Classe Quinta Scuola Secondaria di II grado'
                            END AS descrizione_grado,
                            b.sezione, b2.nome AS indirizzo
                    FROM	istituti.istituti a JOIN
                            istituti.studenti_gruppi b ON a.meccanografico = b.istituto JOIN
                            istituti.indirizzi b2 ON b.indirizzo = b2.codice 
                    WHERE	b.istituto = %s AND b.anno = %s
                    ORDER BY b.anno, b.grado, b.sezione, codice_classe
                    """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY, (meccanografico, anno))
        records = cursor.fetchall()

        db.closeConnection()

        if len(records) > 0:
            istituto = {}
            colonne_istituto = ["istituto", "nome_istituto", "anno"]
            colonne_classe = ["codice_classe", "grado", "descrizione_grado", "sezione", "indirizzo"]

            ultimo_codice_classe = ""

            for record in records:
                istituto = istituto or {
                    #column: getattr(record, column, "") for column in colonne_istituto
                    column: record.get(column, "") for column in colonne_istituto
                }
                #codice_classe = record.codice_classe
                codice_classe = record['codice_classe']
                classe = {
                    #column: getattr(record, column, "") for column in colonne_classe
                    column: record.get(column, "") for column in colonne_classe
                }
                
                if ultimo_codice_classe != str(codice_classe):
                    ultimo_codice_classe = str(codice_classe)


                istituto.setdefault("classi", {}).setdefault(codice_classe, classe)

            return json.dumps(istituto, indent=4)

        return (
            f"Errore: nessun dato trovato per l'istituto {meccanografico} e anno {anno}"
        )
    except Exception as inst:
        db.closeConnection()
        return f"""Errore generico: Questo tool accetta in ingresso un parametro "istituto" e un parametro opzionale "anno"."""+str(inst)

#print(informazioni_istituto('RMIS00900E'))