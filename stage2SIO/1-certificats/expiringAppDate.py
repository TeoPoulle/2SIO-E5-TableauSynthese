import requests
import json
from datetime import datetime, timedelta
import logging
import os

# Configuration des valeurs importantes
clientId = ''          # ID de l'application qui permet au programme d'accéder aux applications
clientSecret = ''  # Secret qui apparaîtra en même temps que l'ID
tenantName = ''                          # Domaine liée à Microsoft Entra
months = 6                                                  # Nombre de mois avant expiration des certificats/secrets
path = './ExpiringApps.json'                                # Chemin vers le fichier de sortie (à changer suivant l'appareil)

# URLs
loginUrl = 'https://login.microsoftonline.com'
graphUrl = 'https://graph.microsoft.com'
appsUrl = f"{graphUrl}/v1.0/applications/"                 # URL initiale pour les applications
jsons = []                                                  # Liste pour stocker les données des applications

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, 'docImportant/expiringCertificate.log')

logging.basicConfig(
    filename=logFile,             # Chemin du fichier de log en cas d'erreur
    level=logging.INFO,           # Pour plus de détails
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

# Fonction pour obtenir un token d'accès
def getAccessToken(loginUrl, clientId, clientSecret, tenantName):
    tokenUrl = f"{loginUrl}/{tenantName}/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(tokenUrl, data=data)
    if response.status_code != 200:
        pass
        logging.error(f"{os.path.basename(__file__)} : Erreur lors de la demande de token : {response.status_code}")
        logging.error(f"{os.path.basename(__file__)} : Réponse : {response.text}")
    response.raise_for_status()  # En cas d'erreur, renvoie une exception
    return response.json()

# Obtenir le token
oauth = getAccessToken(loginUrl, clientId, clientSecret, tenantName)
accessToken = oauth['access_token']
tokenType = oauth['token_type']

# Headers pour les appels API
headers = {
    'Authorization': f"{tokenType} {accessToken}",
    'Content-Type': 'application/json'
}

while appsUrl:
    # Appel API pour lister les applications
    response = requests.get(appsUrl, headers=headers)
    response.raise_for_status()
    data = response.json()
    applications = data.get('value', [])
    expire, urgent, alert, ok = 0, 0, 0, 0
    
    # Pour chaque application, on vérifie les secrets et certificats
    for app in applications:
        appName = app['displayName']
        appClientId = app['appId']
        
        # Traiter les secrets (passwordCredentials) et certificats (keyCredentials)
        items = app.get('passwordCredentials', []) + app.get('keyCredentials', [])
        for item in items:
            startDateStr = item.get('startDateTime')
            endDateStr = item.get('endDateTime')
            if not startDateStr or not endDateStr:
                continue
                
            # Déterminer le type (Secret ou Certificate)
            if item in app.get('passwordCredentials', []):
                appType = 'Secret'
            else:
                appType = 'Certificat'

            # Convertir les dates pour qu'elles soient traitables par python
            startDate = datetime.fromisoformat(startDateStr.split('T')[0])
            endDate = datetime.fromisoformat(endDateStr.split('T')[0])
            optimalDate = datetime.now() + timedelta(days=months * 30)
            criticDate = datetime.now() + timedelta(days=30)
            
            # Déterminer le statut de l'expiration (Expiré, Très proche, Proche)
            if endDate < datetime.now():
                statusState = 'Expiré'
                expire += 1
            elif endDate < optimalDate:
                if endDate < criticDate:
                    statusState = "Expire bientôt (moins d'un mois)"
                    urgent += 1
                else:
                    statusState = f'Expire dans moins de {months} mois'
                    alert += 1
            else :
                statusState = 'Valide'
                ok += 1
                
            # Ajouter l'entrée au json
            json_entry = {
                'Application': appName,
                'AppID': appClientId,
                'Type': appType,
                'Name': item.get('displayName', 'N/A'),
                'StartDate': startDate.strftime('%Y-%m-%d'),
                'EndDate': endDate.strftime('%Y-%m-%d'),
                'Status': statusState
            }
            jsons.append(json_entry)
    
    # Gestion de la pagination
    appsUrl = data.get('@odata.nextLink')

    logging.info(f"{os.path.basename(__file__)} : Vérification des applications terminée. Nombre total d'entrées: {len(jsons)}")
    logging.info(f"{os.path.basename(__file__)} : Statistiques - Expiré : {expire}, Expire dans moins d'un mois : {urgent}, Expire dans moins de {months} mois : {alert}, Valide : {ok}")

# Écrire dans un fichier JSON
if jsons:
    with open('./docImportant/ExpiringApps.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(jsons, jsonfile, indent=4, ensure_ascii=False)