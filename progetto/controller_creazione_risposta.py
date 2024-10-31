import copy
import json
from typing import Any, Dict
import warnings
from dotenv import load_dotenv
import os

warnings.filterwarnings("ignore")

from crews.consultazione_memoria.crew import CrewConsultazioneMemoria
from crews.creazione_risposta.crew import CrewCreazioneRisposta
from crews.revisione_risposta.crew import CrewRevisioneRisposta

import sys
parent_directory = os.path.abspath(".")
sys.path.append(parent_directory)
from progetto.database.database import db

load_dotenv()
SELFREFLECTION = (os.getenv('SELFREFLECTION', 'False') == 'True')
TRAINING = (os.getenv('TRAINING', 'False') == 'True')


class ControllerCreazioneRisposta:
   def __init__(self):
      self.category_list = []
      self.category_info = []
      self.crew_consultazione_memoria = None
      self.crew_creazione_risposta = None
      self.crew_revisione_risposta = None

   def execute(self, domanda):
      print("SELFREFLECTION: " + str(SELFREFLECTION))
      print("TRAINING: " + str(TRAINING))
      # ========= RECUPERO I SUGGERIMENTI DEL PASSATO =========

      if SELFREFLECTION:
         # recupero le categorie delle esperienze passate già esistenti
         self.retrieve_categories()

         self.crew_consultazione_memoria = CrewConsultazioneMemoria()

         # consulto la memoria classificando la domanda secondo una qualche categoria già esistente
         self.crew_consultazione_memoria.genera()
         crew_memoria = self.crew_consultazione_memoria.crew

         # sistemo gli input e lancio la crew per la classificazione della domanda e il recupero dei suggerimenti di domande simili
         inputs_memoria = self.add_category_list_to_inputs(domanda)
         result = crew_memoria.kickoff(inputs=inputs_memoria)

         print("\n\n===classifica_richiesta===\n\n")
         print(self.crew_consultazione_memoria.tasks['classifica_richiesta_task'].output.raw)
         print("\n\n===seleziona_esperienze===\n\n")
         print(self.crew_consultazione_memoria.tasks['seleziona_esperienze_task'].output.raw)
         print("\n\n===estrazione_suggerimenti===\n\n")
         print(self.crew_consultazione_memoria.tasks['estrazione_suggerimenti_task'].output.raw)

         categoria = self.get_selected_category()
         print('\nÈ stata selezionata la categoria "' + str(categoria) + '"')


      # ========= GENERAZIONE DELLA RISPOSTA =========

      # genero la risposta aiutandomi con suggerimenti già usati in esperienze passate simili (domande della stessa categoria e selezionate opportunamente)
      self.crew_creazione_risposta = CrewCreazioneRisposta()
      self.crew_creazione_risposta.genera()
      crew_risposta = self.crew_creazione_risposta.crew

      # aggiungo i suggerimenti al prompt
      inputs_risposta = self.add_suggestions_to_inputs(domanda)

      print("\n\nTEST:\n" + str(inputs_risposta) + "\n\n")

      result = crew_risposta.kickoff(inputs=inputs_risposta)
      print("Ho realizzato il piano di esecuzione con questo prompt:\n" + str(self.crew_creazione_risposta.tasks['piano_ricerca_task'].prompt()) + "\n\n")

      plan = self.crew_creazione_risposta.tasks['piano_ricerca_task'].output.raw
      execution = self.crew_creazione_risposta.tasks['esecuzione_piano_ricerca_task'].output.raw

      print("\n\n===piano_ricerca_task===\n\n")
      print(plan)
      print("\n\n===esecuzione_piano_ricerca_task===\n\n")
      print(execution)

      risposta = result
      #print(risposta)

      # ========= REVISIONE DELLA RISPOSTA PER MIGLIORAMENTO DELLA TRAIETTORIA =========

      if SELFREFLECTION and TRAINING:
         self.crew_revisione_risposta = CrewRevisioneRisposta()
         self.crew_revisione_risposta.genera()
         crew_revisione = self.crew_revisione_risposta.crew

         # aggiungo tutti gli input utili
         inputs_revisione = copy.deepcopy(domanda)
         inputs_revisione['support_reasoning'] = plan
         inputs_revisione['support_execution'] = execution
         from crews.creazione_risposta.agents.pianificazione_ricerca import backstory
         inputs_revisione['planning_agent_prompt'] = backstory
         # non voglio solo i suggerimenti molto vicini alla domanda ma voglio tutti i suggerimenti di categoria perché aiutano a scartare soluzioni non buone che rispuntano fuori
         inputs_revisione['request_category'] = categoria
         inputs_revisione = self.add_suggestions_to_inputs(inputs_revisione)
         
         result = crew_revisione.kickoff(inputs=inputs_revisione)

         #print("===STAMPO IL RISULTATO===")
         #print(result)

         #print(self.crew_revisione_risposta.tasks['classifica_richiesta_task'].output.raw)
         #print("\n\n===\n\n")
         #print(self.crew_revisione_risposta.tasks['revisiona_risposta_task'].output.raw)

         self.save_experience(categoria, domanda['user_informations'], domanda['support_request'], plan, execution, self.get_new_suggestions())

      print('fine')

      return risposta


   def retrieve_categories(self):
      conn = db.connect()
      conn.autocommit = True

      SQL_QUERY = f""" 
                  SELECT	nome, descrizione, MAX(b.data_inserimento) AS recente, a.macro_categoria
                  FROM	   memoria.categorie a JOIN
                           memoria.esperienze_passate b ON a.nome = b.categoria
                  WHERE   b.obsoleta = 0
                  GROUP BY nome, descrizione
                  ORDER BY recente DESC, nome
                  LIMIT   50;
                  """

      cursor = conn.cursor(dictionary=True)
      cursor.execute(SQL_QUERY)
      records = cursor.fetchall()
      db.closeConnection()


      categorie_lista = []
      categorie = []
      for record in records:
         categorie_lista.append(record["nome"])
         categorie.append(
               {"categoria": record["nome"], "descrizione": record["descrizione"], "macro_categoria": record["macro_categoria"]}
         )

      self.category_list = categorie_lista
      self.category_info = categorie

   def add_category_list_to_inputs(self, inputs):
      inputs_modificati = copy.deepcopy(inputs)

      # aggiungo all'input le informazioni che mi servono
      inputs_modificati["request_categories"] = json.dumps(self.category_info)
      
      return inputs_modificati
   
   def get_selected_category(self):
      categoria = self.crew_consultazione_memoria.tasks['classifica_richiesta_task'].output.raw

      # Applichiamo tutte le sostituzioni usando un ciclo
      replacements = [("```json", ""), ("```", "")]
      for old, new in replacements:
         categoria = categoria.replace(old, new)

      obj = json.loads(categoria)
      if "nome" not in obj or "descrizione" not in obj:
         raise Exception('Categoria non trovata o generata correttamente: manca nome o descrizione; ' + str(obj))
      
      return obj
   
   def get_selected_suggestions(self):
      if self.crew_consultazione_memoria is None: return '"Nessun suggerimento passato"'
      suggestions = self.crew_consultazione_memoria.tasks.get('estrazione_suggerimenti_task', {}).output.raw or '"Nessun suggerimento passato"'

      # Applichiamo tutte le sostituzioni usando un ciclo
      replacements = [("```json", ""), ("```", "")]
      for old, new in replacements:
         suggestions = suggestions.replace(old, new)

      obj = json.loads(suggestions)
      return obj
   
   def add_suggestions_to_inputs (self, inputs):
      inputs_modificati = copy.deepcopy(inputs)

      # aggiungo all'input le informazioni che mi servono
      suggestions = self.get_selected_suggestions()

      inputs_modificati["previous_suggestions"] = json.dumps(suggestions)
      
      return inputs_modificati
   
   def get_new_suggestions(self):
      suggestions = self.crew_revisione_risposta.tasks['controlla_suggerimenti_task'].output.raw

      # Applichiamo tutte le sostituzioni usando un ciclo
      replacements = [("```json", ""), ("```", "")]
      for old, new in replacements:
         suggestions = suggestions.replace(old, new)

      obj = json.loads(suggestions)
      
      return obj

   def save_experience(self, category, user, request, plan, execution, suggestions):
      print("\n\n\n===SALVO L'ESPERIENZA===\n\n\n")
      conn = db.connect()
      conn.autocommit = True

      # memorizzo la categoria se è nuova
      if category["nome"] not in self.category_list:
         SQL_QUERY = f""" 
                  INSERT INTO memoria.categorie (nome, descrizione)
                  VALUES (%s, %s)
                  """

         cursor = conn.cursor()
         cursor.execute(SQL_QUERY, (category["nome"], category["descrizione"]))


      # memorizzo l'esperienza
      SQL_QUERY = f""" 
               INSERT INTO memoria.esperienze_passate(categoria, utente, domanda, pianificazione, esecuzione_pianificazione) 
               VALUES (%s, %s, %s, %s, %s)
               """

      cursor = conn.cursor()
      cursor.execute(SQL_QUERY, (category["nome"].strip(), user.strip(), request.strip(), plan.strip(), execution.strip()))
      experience_id = cursor.lastrowid


      # memorizzo i suggerimenti
      for suggestion in suggestions:
         if(type(suggestion) == int or (type(suggestion) == str and suggestion.isnumeric())):            
            # è un suggerimento già presente sul DB
            suggestion_id = suggestion
         else:
            # è un nuovo suggerimento, lo memorizzo
            SQL_QUERY = f""" 
                     INSERT INTO memoria.suggerimenti_passati(suggerimento) 
                     VALUES (%s)
                     """

            cursor = conn.cursor()
            cursor.execute(SQL_QUERY, (suggestion,))
            suggestion_id = cursor.lastrowid


         # memorizzo la correlazione del suggerimento con l'esperienza inserita in precedenza
         SQL_QUERY1 = f""" 
                     SET @media_punteggio = IFNULL((SELECT AVG(punteggio) FROM memoria.suggerimenti_esperienze WHERE suggerimento = %s), 0.5);
                     """
         
         SQL_QUERY2 = f""" 
                     INSERT INTO memoria.suggerimenti_esperienze (esperienza, suggerimento, punteggio)
                     VALUES (%s, %s, @media_punteggio);
                     """

         cursor = conn.cursor()
         cursor.execute(SQL_QUERY1, (suggestion_id,))
         cursor.execute(SQL_QUERY2, (experience_id, suggestion_id))


      db.closeConnection()


