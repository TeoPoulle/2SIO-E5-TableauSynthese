import requests
import json
import os
import logging
import csv 
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Valeurs à modifier en fonction de la machine / user
url = 'http://localhost:8080/apirest.php'
apiToken = ''
userToken = ''
listeMateriel = {"Computer":1, "Monitor":2, "NetworkEquipment":3, "Printer":4, "Phone":5} # A modifier

# Création d'un fichier de log
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, './docImportant/infoMateriel.log')
logging.basicConfig(
    filename=logFile,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

def exportAllMaterials(urlAPI, appToken, userToken):
    """Cette méthode exporte tout le matériel contenu dans GLPI grâce à un API.
    Elle prend en paramètres : 
    - urlAPI = l'URL de l'API GLPI ;
    - apiToken = le token de l'application ;
    - userToken = le token de l'utilisateur."""
    
    # Initialisation de la session
    sessionUrl = f'{urlAPI}/initSession'
    headersToken = {
        'App-Token': appToken,
        'Authorization': f'user_token {userToken}'
    }
    sessionResponse = requests.get(sessionUrl, headers=headersToken)

    # Si la session a été initialisée
    if sessionResponse.status_code == 200:
        sessionToken = sessionResponse.json()['session_token']
        headersSession = {
            'App-Token': appToken,
            'Session-Token': sessionToken 
        }
        
        # Pour chaque type de matériel
        for materiel, searchId in listeMateriel.items():
            completeData = {"data": []}
            
            # On récupère les champs grâce à SavedSearch
            searchUrl = f'{urlAPI}/search/{materiel}'
            params = {"savedsearches_id": searchId, "forcedisplay[0]": "1", "forcedisplay[1]": "3", "forcedisplay[2]": "4", 
                      "forcedisplay[3]": "5", "forcedisplay[4]": "23", "forcedisplay[5]": "31", "forcedisplay[6]": "40",
                      "forcedisplay[7]": "49", "forcedisplay[8]": "50", "forcedisplay[9]": "76666", "forcedisplay[10]": "76667", # A modifier
                      "forcedisplay[11]": "76668"}
            searchResults = requests.get(searchUrl, headers=headersSession, params=params).json()
            
            # Pour chaque résultat, on récupère l'ID et les données Infocom
            if 'data' in searchResults and searchResults['data']:
                for item in searchResults['data']:
                    itemName = item.get('1', '')
                    
                    try: 
                        allItemsResponse = requests.get(f'{urlAPI}/{materiel}', headers=headersSession).json()
                        itemId = None
                        
                        # Si la réponse existe et est une liste, on cherche l'objet avec le même nom
                        if isinstance(allItemsResponse, list):
                            for obj in allItemsResponse:
                                if obj.get('name') == itemName:
                                    itemId = obj.get('id')
                                    break
                        if not itemId: # Si on n'a pas trouvé l'ID, on passe au suivant
                            continue
                        
                        # Récupérer les données des dates depuis Infocom
                        warrantyExpiration = ''
                        try:
                            infocomResponse = requests.get(f'{urlAPI}/{materiel}/{itemId}/Infocom', headers=headersSession).json()
                            if isinstance(infocomResponse, list) and len(infocomResponse) > 0:
                                infocom = infocomResponse[0]
                            elif isinstance(infocomResponse, dict):
                                infocom = infocomResponse
                            else:
                                infocom = {}
                            
                            # On récupère les dates importantes
                            warrantyDate = infocom.get('warranty_date', '')
                            warrantyDuration = infocom.get('warranty_duration', 0)
                            
                            # S'il y a une date de garantie et une durée, on calcule la date d'expiration
                            if warrantyDate and warrantyDuration:
                                warrantyDate = datetime.strptime(warrantyDate, '%Y-%m-%d')
                                expirationDate = warrantyDate + relativedelta(months=int(warrantyDuration))
                                warrantyExpiration = expirationDate.strftime('%Y-%m-%d')
                        
                        except Exception as e: # En cas d'erreur, on ajoute dans les logs un avertissement
                            logging.error(f"Erreur Infocom pour {materiel}/{itemId}: {str(e)}")
                        
                        # Construire l'objet avec toutes ses informations
                        completeItem = {
                            "1": item.get('1', ''), 
                            "3": item.get('3', ''),
                            "4": item.get('4', ''),
                            "5": item.get('5', ''),
                            "49": infocom.get('buy_date', ''),
                            "50": warrantyExpiration,
                            "23": item.get('23', ''),
                            "31": item.get('31', ''),
                            "40": item.get('40', ''),               # Pour trouver les IDs des champs supplémentaires
                            "76666": item.get('76666', ''),         # listSearchUrl = f'{urlAPI}/listSearchOptions/Phone'
                            "76667": item.get('76667', ''),         # response = requests.get(listSearchUrl, headers=headersSession).json()
                            "76668": item.get('76668', '')          # print(json.dumps(response, indent=2))
                        }
                        completeData['data'].append(completeItem)
                        
                    except Exception as e: # En cas d'erreur, on ajoute dans les logs une erreur
                        logging.error(f"{os.path.basename(__file__)} : Erreur pour {materiel}/{itemName}: {str(e)}")
            
            # On exporte les données complètes en JSON
            with open(f'./docImportant/jsonData/Export{materiel}.json', 'w', encoding='utf-8') as jsonFile:
                json.dump(completeData, jsonFile, indent=4, ensure_ascii=False)
            logging.info(f"{os.path.basename(__file__)} : Export '{materiel}' terminé ({len(completeData['data'])} objets).")
    else:
        logging.error(f"{os.path.basename(__file__)} : Erreur session : {sessionResponse.text}")


def createCsv(pathToJsons, pathToCsv):
    """Cette méthode crée un fichier .csv contenant tout le matériel informatique de l'organisation.
    Elle prend en paramètres : 
    - pathToJsons = le chemin absolu du répertoire dans lequel les fichiers .json avec les données à formater ;
    - pathToCsv = le chemin absolu du répertoire dans lequel va se télécharger le fichier .csv final.
    """

    # Création du fichier CSV et définition des colonnes
    with open(pathToCsv, 'w', newline='', encoding='utf-8') as csvFile:
        colonne = ['ID ligne', 'Catégorie', 'Nom', 'Entité', 'Statut', 'Type', 'Fabricant', 'Modèle', 'Numéro de série', "Date d'achat", "Date d'expiration de la garantie", "Conso annuelle (kWh/an)", "Conso annuelle (kg CO2e/an)", "Fabrication + transport (kg CO2e)"]
        csvWriter = csv.DictWriter(csvFile, fieldnames=colonne)
        csvWriter.writeheader()
        
        ligneId = 1
        # Pour chaque catégorie de matériel
        for categorie in listeMateriel.keys():
            jsonPath = os.path.join(pathToJsons, f'Export{categorie}.json')
            try: # Lecture du fichier JSON
                with open(jsonPath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                categorieName = "Ordinateur" if categorie == "Computer" else "Écran" if categorie == "Monitor" else "Équipement réseau" if categorie == "NetworkEquipment" else "Imprimante" if categorie == "Printer" else "Téléphone" if categorie == "Phone" else categorie
                
                # Si des données existent dans le fichier JSON, on les écrit dans le CSV
                if 'data' in data and data['data']:
                    for item in data['data']:
                        row = {
                            'ID ligne': ligneId,
                            'Catégorie': categorieName,
                            'Nom': item.get('1', ''),
                            'Entité': item.get('3', ''),
                            'Statut': item.get('31', ''),
                            'Type': item.get('4', ''),
                            'Fabricant': item.get('23', ''),
                            'Modèle': item.get('40', ''),
                            'Numéro de série': item.get('5', ''),
                            "Date d'achat": item.get('49', ''),
                            "Date d'expiration de la garantie": item.get('50', ''),
                            "Conso annuelle (kWh/an)": item.get('76668', ''),
                            "Conso annuelle (kg CO2e/an)": item.get('76667', ''),
                            "Fabrication + transport (kg CO2e)": item.get('76666', '')
                        }
                        csvWriter.writerow(row)
                        ligneId += 1

            except Exception as e: # En cas d'erreur, on ajoute dans les logs une erreur
                logging.error(f"{os.path.basename(__file__)} : Erreur lecture {jsonPath}: {str(e)}")
    logging.info(f"{os.path.basename(__file__)} : Fichier CSV créé avec succès.")

try: # Lancement de l'export et de la création du CSV
    exportAllMaterials(url, apiToken, userToken)
    createCsv('./docImportant/jsonData/', './docImportant/ExportMateriel.csv')
    logging.info("")

except Exception as e:
    logging.error(f"{os.path.basename(__file__)} : Erreur: {str(e)}")