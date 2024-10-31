from crewai_tools import tool
import json
import os
import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db


@tool("Informazioni sulle attività svolte dallo studente (IASS)")
def informazioni_studente(sidi: str) -> str:
    """
    Restituisce tutte le informazioni relative ad un codice SIDI: informazioni anagrafiche, classe frequentate nei vari anni, istituti, attività svolte.
    Accetta in ingresso il codice SIDI di uno studente.
    """

    try:
        conn = db.connect()

        SQL_QUERY = f""" 
                    WITH RECURSIVE crea_storico_studente_da_sidi AS (
                        -- Seleziona il sottoinsieme iniziale di record (ad esempio con una condizione su id)
                        SELECT studente, cod_sidi, cod_sidi_new, CAST(cod_sidi AS CHAR(100)) AS visited
                            FROM anagrafica.sidi
                            WHERE cod_sidi = %s

                        UNION ALL

                        -- Trova i record correlati in avanti (dove id_new punta a un altro id)
                        SELECT e.studente, e.cod_sidi, e.cod_sidi_new, CONCAT(ce.visited, ',', e.cod_sidi) AS visited  -- Aggiungiamo l'id corrente alla lista di visitati
                        FROM anagrafica.sidi e
                        INNER JOIN crea_storico_studente_da_sidi ce ON e.cod_sidi = ce.cod_sidi_new
                        WHERE FIND_IN_SET(e.cod_sidi, ce.visited) = 0  -- Evita di visitare di nuovo lo stesso id

                        UNION ALL

                        -- Trova i record correlati indietro (dove altri record puntano all'id corrente tramite id_new)
                        SELECT e.studente, e.cod_sidi, e.cod_sidi_new, CONCAT(ce.visited, ',', e.cod_sidi) AS visited  -- Aggiungiamo l'id corrente alla lista di visitati
                        FROM anagrafica.sidi e
                        INNER JOIN crea_storico_studente_da_sidi ce ON e.cod_sidi_new = ce.cod_sidi
                        WHERE FIND_IN_SET(e.cod_sidi, ce.visited) = 0  -- Evita di visitare di nuovo lo stesso id
                    )


					SELECT	a.studente, a0.cod_sidi, a0.cod_sidi_new, b.nome, cognome, nascita_giorno, nascita_mese, nascita_anno, sesso,
							c.anno, b2.nome AS stato, c.attivo, studenti_gruppo AS codice_classe, c.grado, d.sezione, f.nome AS indirizzo, 
							d.istituto, e.nome AS nome_istituto, e.lingua, e.gruppo
					FROM	crea_storico_studente_da_sidi a0 JOIN
							anagrafica.sidi a ON a0.studente = a.studente JOIN
							anagrafica.anagrafica b ON a.studente = b.studente JOIN
							studenti.studenti c ON a.studente = c.studente JOIN
							studenti.stati b2 ON c.stato = b2.codice JOIN
							istituti.studenti_gruppi d ON c.studenti_gruppo = d.id AND c.anno = d.anno JOIN
							istituti.istituti e ON d.istituto = e.meccanografico JOIN
							istituti.indirizzi f ON d.indirizzo = f.codice
					ORDER BY /*record_num DESC, */c.anno DESC, c.attivo DESC
					"""

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY, (sidi,))
        records = cursor.fetchall()

        if len(records) > 0:
            studente = {}
            colonne_studente = [
                "studente",
                "cod_sidi",
                "nome",
                "cognome",
                "nascita_giorno",
                "nascita_mese",
                "nascita_anno",
                "sesso",
            ]
            colonne_frequenza = colonne_studente + [
                "stato",
                "attivo",
                "codice_classe",
                "grado",
                "sezione",
                "indirizzo",
                "istituto",
                "nome_istituto",
                "lingua",
                "gruppo",
            ]

            colonne_studente = []

            for record in records:
                studente = studente or {
                    column: record.get(column, "") for column in colonne_studente
                }
                frequenza = {
                    column: record.get(column, "") for column in colonne_frequenza
                }

                studente.setdefault("raccolta_informazioni", {}).setdefault(
                    # record.anno, []
                    record["anno"],
                    [],
                ).append(frequenza)

            SQL_QUERY = f""" 
					WITH RECURSIVE crea_storico_studente_da_sidi AS (
                        -- Seleziona il sottoinsieme iniziale di record (ad esempio con una condizione su id)
                        SELECT studente, cod_sidi, cod_sidi_new, CAST(cod_sidi AS CHAR(100)) AS visited
                            FROM anagrafica.sidi
                            WHERE cod_sidi = %s

                        UNION ALL

                        -- Trova i record correlati in avanti (dove id_new punta a un altro id)
                        SELECT e.studente, e.cod_sidi, e.cod_sidi_new, CONCAT(ce.visited, ',', e.cod_sidi) AS visited  -- Aggiungiamo l'id corrente alla lista di visitati
                        FROM anagrafica.sidi e
                        INNER JOIN crea_storico_studente_da_sidi ce ON e.cod_sidi = ce.cod_sidi_new
                        WHERE FIND_IN_SET(e.cod_sidi, ce.visited) = 0  -- Evita di visitare di nuovo lo stesso id

                        UNION ALL

                        -- Trova i record correlati indietro (dove altri record puntano all'id corrente tramite id_new)
                        SELECT e.studente, e.cod_sidi, e.cod_sidi_new, CONCAT(ce.visited, ',', e.cod_sidi) AS visited  -- Aggiungiamo l'id corrente alla lista di visitati
                        FROM anagrafica.sidi e
                        INNER JOIN crea_storico_studente_da_sidi ce ON e.cod_sidi_new = ce.cod_sidi
                        WHERE FIND_IN_SET(e.cod_sidi, ce.visited) = 0  -- Evita di visitare di nuovo lo stesso id
                    )
                    
                    SELECT	a.studente, a.cod_sidi, a.cod_sidi_new,
								CASE 
									WHEN b.materia = 'LIN' THEN 'ITALIANO'
									WHEN b.materia = 'MAT' THEN 'MATEMATICA'
									WHEN b.materia = 'ERE' THEN 'INGLESE LETTURA'
									WHEN b.materia = 'ELI' THEN 'INGLESE ASCOLTO'
								END AS attivita_materia, 
								c.descrizione AS attivita_descrizione, b.data AS attivita_data
						FROM	crea_storico_studente_da_sidi a
								LEFT JOIN studenti.attivita b ON a.studente = b.studente
								LEFT JOIN studenti.attivita_tipi c ON c.id = b.tipo
						ORDER BY /*record_num DESC, */b.data DESC
						"""

            cursor = conn.cursor(dictionary=True)
            cursor.execute(SQL_QUERY, (sidi,))
            records = cursor.fetchall()

            db.closeConnection()

            distinct_sidi = {}
            for record in records:
                # distinct_sidi[record.cod_SIDI] = {
                #     "cod_sidi": record.cod_SIDI,
                #     "rimpiazzato_da": record.cod_SIDI_new,
                #     "attuale": record.cod_SIDI_new is None,
                #     "attivita_svolte": [],
                # }
                distinct_sidi[record["cod_sidi"]] = {
                    "cod_sidi": record["cod_sidi"],
                    "rimpiazzato_da": record["cod_sidi_new"],
                    "attuale": record["cod_sidi_new"] is None,
                    "attivita_svolte": [],
                }

            for record in records:
                # if record.attivita_descrizione is None:
                if record["attivita_descrizione"] is None:
                    continue

                # distinct_sidi[record.cod_SIDI]["attivita_svolte"].append(
                #     {
                #         "attivita_descrizione": record.attivita_descrizione,
                #         "attivita_materia": record.attivita_materia,
                #         "attivita_data": str(record.attivita_data),
                #     }
                # )

                distinct_sidi[record["cod_sidi"]]["attivita_svolte"].append(
                    {
                        "attivita_descrizione": record["attivita_descrizione"],
                        "attivita_materia": record["attivita_materia"],
                        "attivita_data": str(record["attivita_data"]),
                    }
                )

            studente["tutti_i_sidi_dello_studente"] = distinct_sidi

            return json.dumps(studente, indent=4)

        return "Errore: nessun dato trovato per lo studente con codice sidi " + sidi
    except Exception as inst:
        db.closeConnection()
        return (
            "Errore generico: passare un codice SIDI per ottenere le informazioni di uno studente"
            + str(inst)
        )


# print(informazioni_studente("22036962"))
