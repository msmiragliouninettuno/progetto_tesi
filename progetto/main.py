
from controller_creazione_risposta import ControllerCreazioneRisposta

import json
import random

from dotenv import load_dotenv
import os

load_dotenv()
SELFREFLECTION = (os.getenv('SELFREFLECTION', 'False') == 'True')
TRAINING = (os.getenv('TRAINING', 'False') == 'True')

print(str(os.getenv('SELFREFLECTION', 'False')) + ' - ' + str(os.getenv('TRAINING', 'False')))

data = []

with open("./tests/studenti_mancanti/01-cambio_sidi.json", "r") as file1:
    cambio_sidi = json.load(file1)
    
with open("./tests/studenti_mancanti/02-usciti_sidi.json", "r") as file2:
    usciti_sidi = json.load(file2)

with open("./tests/prove_mancanti/raw/selezionati_db_cambio_tipo.json", "r") as file3:
    prove_mancanti1 = json.load(file3)

with open("./tests/prove_mancanti/raw/selezionati_db_cambio_sidi.json", "r") as file4:
    prove_mancanti2 = json.load(file4)


#data = usciti_sidi

data = prove_mancanti1[30:35]

random.seed(1390)  
random.shuffle(data)

print(str(data) + "\n\n")

start = 0
steps = 10
for request in data[start:(start+steps)]:
    domanda = {
        "support_request": request["richiesta"],
        "user_informations": request["ruolo"],
    }

    controller_creazione_risposte = ControllerCreazioneRisposta()
    controller_creazione_risposte.execute(domanda)

