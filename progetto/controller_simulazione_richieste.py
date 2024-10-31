import copy
import json
from typing import Any, Dict
import warnings
from dotenv import load_dotenv
import os

warnings.filterwarnings("ignore")

from crews.simulazione_richieste.crew import CrewSimulazioneRichieste

import sys

parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)
from progetto.database.database import db

load_dotenv()
SELFREFLECTION = os.getenv("SELFREFLECTION", "False") == "True"


class ControllerSimulazioneRichieste:
    def __init__(self):
        self.crew_simulazione_richieste = None

    def execute(self, type):
        if type == "missing_students":
            data = self.retrieve_missing_students()
            goal = """
                    Ti vengono passati dei dati di studenti e devi creare un array json in cui per ogni elemento ci sia "richiesta" e "ruolo".
                    
                    Ogni "richiesta" deve essere realizzata come fosse una richiesta da parte di un utente che chiede informazioni riguardo la mancanza in elenco di uno 
                    studente su un sito istituzionale:
                    - preleva le informazioni dal record che stai esaminando; 
                    - crea una richiesta di delucidazioni sulla mancanza di questo studente in un elenco sul sito indicando le informazioni che hai

                    Il "ruolo" dell'utente può essere "Dirigente scolastico dell'istituto XXX" oppure "Segreteria scolastica dell'istituto XXX" e devi sostituire XXX con 
                    il corretto istituto del record che stai lavorando.
                    """
            backstory = """
                    Sei un creatore di richieste: sei in grado di convertire dei record di dati in richieste come fossero da parte di utenti reali.
                    Sei un ottimo simulatore umano e sai inserire le informazioni di ogni record nel giusto modo in una richiesta di assistenza simulata.
                    """
            task_description = """
                    Converti i dati che seguono in un array json contenente elementi con al loro interno "richiesta" e "ruolo" usando i dati di ogni record e
                    simulando un utente che richiede supporto. L'utente può essere "Dirigente scolastico dell'istituto XXX" oppure "Segreteria scolastica dell'istituto XXX" 
                    e devi sostituire XXX con il corretto istituto del record che stai lavorando.
                    La richiesta deve chiedere informazioni riguardo ad uno studente che non è presente in un elenco su un sito istituzionale.
                    """
            task_expected_output = """
                    Un array json in cui ogni elemento abbia "richiesta" e "ruolo".
                    Devi convertire i dati in ingresso in modo che ogni elemento dell'array contenga la "richiesta" come fosse una richiesta di supporto simulata 
                    da parte di un utente che chiede delucidazioni riguardo all'assenza di uno studente in un elenco su un sito istituzionale.
                    La richiesta deve contenere i dati relativi ad uno dei record passati in ingresso.
                    Il "ruolo" può essere "Dirigente scolastico dell'istituto XXX" oppure "Segreteria scolastica dell'istituto XXX" e devi sostituire XXX con 
                    il corretto istituto del record che stai lavorando.
                    """
        else:
            data = self.retrieve_missing_test()
            goal = """
                    Ti vengono passati dei dati di studenti e devi creare un array json in cui per ogni elemento ci sia "richiesta" e "ruolo".
                    
                    Ogni "richiesta" deve essere realizzata come fosse una richiesta da parte di un utente che chiede informazioni riguardo la mancanza in elenco  
                    di una certa prova svolta da studente su un sito istituzionale:
                    - preleva le informazioni dal record che stai esaminando; 
                    - crea una richiesta di delucidazioni sulla mancanza di questa prova di una certa materia sul sito indicando le informazioni che hai
                    - usa sempre il codice sidi, è molto importante

                    Il "ruolo" dell'utente può essere "Dirigente scolastico dell'istituto XXX" oppure "Segreteria scolastica dell'istituto XXX" e devi sostituire XXX con 
                    il corretto istituto del record che stai lavorando.
                    """
            backstory = """
                    Sei un creatore di richieste: sei in grado di convertire dei record di dati in richieste come fossero da parte di utenti reali.
                    Sei un ottimo simulatore umano e sai inserire le informazioni di ogni record nel giusto modo in una richiesta di assistenza simulata.
                    """
            task_description = """
                    Converti i dati che seguono in un array json contenente elementi con al loro interno "richiesta" e "ruolo" usando i dati di ogni record e
                    simulando un utente che richiede supporto. L'utente può essere "Dirigente scolastico dell'istituto XXX" oppure "Segreteria scolastica dell'istituto XXX" 
                    e devi sostituire XXX con il corretto istituto del record che stai lavorando.
                    La richiesta deve chiedere informazioni riguardo ad una prova di una certa materia che non risulta svolta da uno studente in un elenco su un sito istituzionale.
                    """
            task_expected_output = """
                    Un array json in cui ogni elemento abbia "richiesta" e "ruolo".
                    Devi convertire i dati in ingresso in modo che ogni elemento dell'array contenga la "richiesta" come fosse una richiesta di supporto simulata 
                    da parte di un utente che chiede delucidazioni riguardo all'assenza di informazioni riguardo una prova su una certa materia da parte di uno studente 
                    all'interno di un sito istituzionale.
                    La richiesta deve contenere i dati relativi ad uno dei record passati in ingresso.
                    Usa sempre il codice sidi, è molto importante
                    Il "ruolo" può essere "Dirigente scolastico dell'istituto XXX" oppure "Segreteria scolastica dell'istituto XXX" e devi sostituire XXX con 
                    il corretto istituto del record che stai lavorando.
                    """

        print(data)
        step = 7
        start = 0

        results = []

        while start < len(data):
            print("\n\nstart: " + str(start) + " e stop: " + str(start + step) + "\n\n")
            new_data = data[start : (start + step)]
            start = start + step
            json_data = json.dumps(new_data)
            inputs_simulazione = {
                "data": json_data,
                "goal": goal,
                "backstory": backstory,
                "task_description": task_description,
                "task_expected_output": task_expected_output,
            }

            self.simulazione_richieste = CrewSimulazioneRichieste()

            self.simulazione_richieste.genera()
            crew_simulazione = self.simulazione_richieste.crew

            # sistemo gli input e lancio la crew per la classificazione della domanda e il recupero dei suggerimenti di domande simili
            result = crew_simulazione.kickoff(inputs=inputs_simulazione)
            results = results + self.json_loads(result.raw)

        # print("\n\n===classifica_richiesta===\n\n")
        # print(self.crew_consultazione_memoria.tasks['classifica_richiesta_task'].output.raw)
        print("\n\n\nFINALE\n\n\n")
        print(json.dumps(results))
        print("fine")

    def retrieve_missing_students(self):
        conn = db.connect()
        conn.autocommit = True

        SQL_QUERY = f""" 
                        SELECT 	istituto, 
                                    CASE 
                                        WHEN grado > 8 THEN grado - 8 
                                            WHEN grado > 6 THEN grado - 6
                                            ELSE grado
                                    END classe,
                                    sezione, b2.nome AS indirizzo, sidi_old, a.nome, cognome, sidi_new, anno_new, gruppo_new, attivo_new
                        FROM 
                            (
                                SELECT 	b.istituto, b.grado, b.sezione, b.indirizzo, c.cod_sidi AS sidi_old, c2.nome, c2.cognome, d.cod_sidi AS sidi_new, e.anno AS anno_new, e.studenti_gruppo AS gruppo_new, e.attivo AS attivo_new
                                FROM	   studenti.studenti a JOIN
                                            istituti.studenti_gruppi b ON a.studenti_gruppo = b.id AND a.anno = b.anno JOIN
                                            anagrafica.sidi c ON a.studente = c.studente LEFT JOIN
                                            anagrafica.anagrafica c2 ON a.studente = c2.studente LEFT JOIN
                                            anagrafica.sidi d ON c.cod_sidi_new = d.cod_sidi LEFT JOIN
                                            studenti.studenti e ON d.studente = e.studente
                                WHERE	   a.anno = 2024 AND a.attivo = 0
                                LIMIT 2500
                            ) a LEFT JOIN
                            istituti.indirizzi b2 ON a.indirizzo = b2.codice
                        WHERE    sidi_new IS NULL /*eliminare*/
                        ORDER BY sidi_new DESC, nome
                        LIMIT 100
                        """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()
        db.closeConnection()

        data = []
        for record in records:
            data.append(
                {
                    "istituto": record["istituto"],
                    "classe": record["classe"],
                    "sezione": record["sezione"],
                    "indirizzo": record["indirizzo"],
                    "sidi": record["sidi_old"],
                    "nome": record["nome"],
                    "cognome": record["cognome"],
                }
            )

        return data

    def retrieve_missing_test(self):
        conn = db.connect()
        conn.autocommit = True

        SQL_QUERY = f""" 
                      SELECT 	istituto, 
                                    CASE 
                                        WHEN b.grado > 8 THEN b.grado - 8 
                                            WHEN b.grado > 6 THEN b.grado - 6
                                            ELSE b.grado
                                    END classe,
                                    sezione, b2.nome AS indirizzo, cod_sidi, c2.nome, cognome, a.anno, a.studenti_gruppo, a.attivo, 
                                    CASE
                                        WHEN a0.materia_mancante = 'LIN' THEN 'Italiano'
                                        WHEN a0.materia_mancante = 'MAT' THEN 'Matematica'
                                        WHEN a0.materia_mancante = 'ERE' THEN 'Inglese Reading'
                                        WHEN a0.materia_mancante = 'ELI' THEN 'Inglese Listening'
                                    END AS materia_mancante
                        FROM 
                            (
                                # studenti che hanno svolto una prova ma poi hanno cambiato tipo di prova e quindi non risulta svolta al dirigente
                                SELECT a.studente, b.materia AS materia_mancante
                                FROM 
                                    (
                                        SELECT studente
                                        FROM 
                                            (
                                            SELECT DISTINCT a.studente, a.materia
                                            FROM 
                                                (
                                                        SELECT * FROM studenti.attivita WHERE tipo = 1
                                                ) a JOIN
                                                (
                                                        SELECT * FROM studenti.attivita WHERE tipo = 2
                                                ) b ON a.studente = b.studente AND a.materia = b.materia
                                            WHERE a.data < b.data
                                        ) a
                                        GROUP BY studente
                                        HAVING COUNT(*) = 1
                                        ) a JOIN
                                        studenti.attivita b ON a.studente = b.studente AND b.tipo = 1 JOIN
                                        studenti.attivita c ON a.studente = c.studente AND c.tipo = 2 AND b.materia = c.materia AND b.data < c.data

                                UNION

                                # studenti che hanno svolto una prova con il vecchio sidi e le altre sul nuovo
                                SELECT b.studente, aa.materia as materia_mancante
                                FROM anagrafica.sidi a JOIN
                                        anagrafica.sidi b ON a.cod_sidi_new = b.cod_sidi JOIN
                                        studenti.attivita aa ON a.studente = aa.studente AND aa.tipo = 1 JOIN
                                        studenti.attivita ba ON b.studente = ba.studente AND ba.tipo = 1 
                                GROUP BY a.studente, b.studente
                                HAVING COUNT(DISTINCT aa.materia) + COUNT(DISTINCT ba.materia) = 4
                            ) a0 JOIN
                            studenti.studenti a ON a0.studente = a.studente AND a.anno = 2024 JOIN
                            istituti.studenti_gruppi b ON a.studenti_gruppo = b.id AND a.anno = b.anno JOIN
                            anagrafica.sidi c ON a.studente = c.studente LEFT JOIN
                            anagrafica.anagrafica c2 ON a.studente = c2.studente LEFT JOIN
                            istituti.indirizzi b2 ON b.indirizzo = b2.codice
                        """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()
        db.closeConnection()

        data = []
        for record in records:
            data.append(
                {
                    "istituto": record["istituto"],
                    "classe": record["classe"],
                    "sezione": record["sezione"],
                    "indirizzo": record["indirizzo"],
                    "sidi": record["cod_sidi"],
                    "nome": record["nome"],
                    "cognome": record["cognome"],
                    "materia_mancante": record["materia_mancante"],
                }
            )

        return data

    def json_loads(self, stringa):
        arr = stringa.split("```json")
        if len(arr) > 1:
            stringa = arr[1]
            arr = stringa.split("```")
            stringa = arr[0]

        # il pezzo di sopra rimpiezza questi replace perché rimuove eventuali scritte in più e quindi è meglio
        replacements = [("```json", ""), ("```", "")]
        for old, new in replacements:
            stringa = stringa.replace(old, new)

        obj = json.loads(stringa)
        return obj


controllore = ControllerSimulazioneRichieste()
controllore.execute("missing_test")
