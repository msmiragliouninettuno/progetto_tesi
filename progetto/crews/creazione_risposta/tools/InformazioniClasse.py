from typing import Optional
from crewai_tools import tool
import json
import os
import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)

from progetto.database.database import db


@tool("Informazioni classe (IC)")
def informazioni_classe(classe: int, anno: int) -> str:
    """
        Estrae i dati dettagliati di una particolare classe, ovvero l'elenco degli studenti;
        PASSARE ALLO STRUMENTO i seguenti parametri:
    - classe: int, un codice classe di 12 cifre
    - anno: int, parametro opzionale contenente l'anno di riferimento, se non necessario passare -1

    esempio parametri:
    {
        classe: "312040071302",
        anno: 2024
    }

    altro esempio parametri:
    {
        classe: "312040071304",
        anno: -1
    }
    """

    try:
        conn = db.connect()

        # se non mi viene passato l'anno allora prendo i dati con l'ultimo anno disponibile
        if anno == -1:
            SQL_QUERY = f""" 
						SELECT	b.anno
						FROM	istituti.istituti a JOIN
								istituti.studenti_gruppi b ON a.meccanografico = b.istituto
						WHERE	b.id = %s
						ORDER BY b.anno DESC
                        LIMIT 1
						"""

            cursor = conn.cursor(dictionary=True)
            cursor.execute(SQL_QUERY, (classe,))
            record = cursor.fetchone()

            anno = record['anno']

            # VERSIONE SQL SERVER
            # SQL_QUERY = f"""
            # 			SELECT	b.istituto, a.nome AS nome_istituto, b.anno, b.id AS codice_classe, b.grado, b.sezione, b2.nome AS indirizzo,
            # 					d.cod_sidi AS cod_sidi_riferimento, e.cod_SIDI AS cod_sidi, e.cod_sidi_new, c.attivo AS studente_attivo,
            # 					d2.nome, d2.cognome, d2.nascita_giorno, d2.nascita_mese, d2.nascita_anno
            # 			FROM	istituti.istituti a JOIN
            # 					istituti.studenti_gruppi b ON a.meccanografico = b.istituto JOIN
            # 					istituti.indirizzi b2 ON b.indirizzo = b2.codice JOIN
            # 					studenti.studenti c ON b.id = c.studenti_gruppo AND b.anno = c.anno JOIN
            # 					anagrafica.sidi d ON c.studente = d.studente JOIN
            # 					anagrafica.anagrafica d2 ON c.studente = d2.studente
            # 					CROSS APPLY anagrafica.crea_storico_studente_da_sidi(d.cod_sidi) e
            # 			WHERE	b.id = ? AND b.anno = ?
            # 			ORDER BY b.anno, b.grado, b.sezione, c.studenti_gruppo, c.attivo DESC
            # 			"""

        SQL_QUERY = f""" 
				WITH RECURSIVE correlated_entities AS (
					-- Selezione iniziale del sottoinsieme di record (ad esempio con una condizione su id)
					SELECT b.istituto, a.nome AS nome_istituto, b.anno, b.id AS codice_classe, b.grado, b.sezione, b2.nome AS indirizzo,
							d.cod_sidi AS cod_sidi_riferimento, d.cod_sidi, d.cod_sidi_new, c.attivo AS studente_attivo,
							d2.nome, d2.cognome, d2.nascita_giorno, d2.nascita_mese, d2.nascita_anno, CAST(d.cod_sidi AS CHAR(300)) AS visited 
						FROM istituti.istituti a JOIN
							istituti.studenti_gruppi b ON a.meccanografico = b.istituto JOIN
							istituti.indirizzi b2 ON b.indirizzo = b2.codice JOIN
							studenti.studenti c ON b.id = c.studenti_gruppo AND b.anno = c.anno JOIN
							anagrafica.sidi d ON c.studente = d.studente JOIN
							anagrafica.anagrafica d2 ON c.studente = d2.studente
						WHERE	b.id = %s AND b.anno = %s
						
					UNION ALL

					-- Recursivamente recupera i record correlati tramite id_new
					SELECT ce.istituto, ce.nome_istituto, ce.anno, ce.codice_classe, ce.grado, ce.sezione, ce.indirizzo,
							ce.cod_sidi_riferimento, e.cod_SIDI AS cod_sidi, e.cod_sidi_new, ce.studente_attivo,
							ce.nome, ce.cognome, ce.nascita_giorno, ce.nascita_mese, ce.nascita_anno, CONCAT(ce.visited, ',', e.cod_sidi) AS visited
					FROM anagrafica.sidi e
					INNER JOIN correlated_entities ce ON e.cod_sidi = ce.cod_sidi_new
					WHERE FIND_IN_SET(e.cod_sidi, ce.visited) = 0
						
					UNION ALL

					-- Recursivamente recupera i record correlati tramite id_new
					SELECT ce.istituto, ce.nome_istituto, ce.anno, ce.codice_classe, ce.grado, ce.sezione, ce.indirizzo,
							ce.cod_sidi_riferimento, e.cod_SIDI AS cod_sidi, e.cod_sidi_new, ce.studente_attivo,
							ce.nome, ce.cognome, ce.nascita_giorno, ce.nascita_mese, ce.nascita_anno, CONCAT(ce.visited, ',', e.cod_sidi) AS visited
					FROM anagrafica.sidi e
					INNER JOIN correlated_entities ce ON e.cod_sidi_new = ce.cod_sidi
					WHERE FIND_IN_SET(e.cod_sidi, ce.visited) = 0

				)

				-- Raggruppa i risultati per ogni record iniziale e crea un array JSON con tutti i correlati
				SELECT *
				FROM correlated_entities
				ORDER BY anno, grado, sezione, codice_classe, cod_sidi_riferimento, studente_attivo DESC;
				"""

        #cursor = conn.cursor()
        #cursor.execute(SQL_QUERY, classe, anno)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY, (classe, anno))
        records = cursor.fetchall()

        db.closeConnection()

        if len(records) > 0:
            classe = {}
            colonne_classe = [
                "codice_classe",
                "anno",
                "grado",
                "sezione",
                "indirizzo",
                "istituto",
                "nome_istituto",
            ]
            colonne_studente = [
                "studente_attivo",
                "nome",
                "cognome",
                "nascita_giorno",
                "nascita_mese",
                "nascita_anno",
            ]

            da_uniformare = ["cod_sidi", "cod_sidi_new", "cod_sidi_riferimento"]

            sidi_lavorati = []

            for record in records:
                for column in da_uniformare:
                    #if getattr(record, column) is not None:
                    #    setattr(record, column, str(getattr(record, column)))
                    # print(column[0])
                    if record[column] is not None:
                        record[column] = str(record[column])

                classe = classe | {
                    #column: getattr(record, column, "") for column in colonne_classe
                    column: record.get(column, "") for column in colonne_classe
                }
                studente = {
                    #column: getattr(record, column, "") for column in colonne_studente
                    column: record.get(column, "") for column in colonne_studente
                } | {"altri_sidi_dello_studente": []}
                #cod_sidi_riferimento = record.cod_sidi_riferimento
                cod_sidi_riferimento = record['cod_sidi_riferimento']

                #if cod_sidi_riferimento in sidi_lavorati: #EVENTUALI PROBLEMI DI CICLI? MA PER MARCO BIGNANTE BISOGNA METTERLO
                    #continue

                #if record.cod_sidi != cod_sidi_riferimento:
                if record['cod_sidi'] != cod_sidi_riferimento:
                    #sidi_lavorati.append(record.cod_sidi)
                    sidi_lavorati.append(record['cod_sidi'])

                classe.setdefault("sidi_studenti", {}).setdefault(
                    cod_sidi_riferimento, studente
                )

                #if record.cod_sidi != cod_sidi_riferimento:
                if record['cod_sidi'] != cod_sidi_riferimento:
                    classe["sidi_studenti"][cod_sidi_riferimento][
                        "altri_sidi_dello_studente"
                    ].append(
                        {
                            #"cod_sidi": record.cod_sidi,
                            #"cod_sidi_new": record.cod_sidi_new,
                            "cod_sidi": record['cod_sidi'],
                            "cod_sidi_new": record['cod_sidi_new'],
                        }
                    )

            return json.dumps(classe, indent=4)

        return f"Errore: nessun dato trovato per la classe {classe} e anno {anno}"
    except Exception as inst:
        db.closeConnection()
        return """Errore generico: Questo tool accetta in ingresso il codice della classe e opzionalmente l'anno di riferimento""" + str(inst)


#print(informazioni_classe(312040050901, 2023))
