# Tous les imports nécessaires à l'exécution du script
import json
import os
import msal
import requests
import logging
import webbrowser 
import pyperclip

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, 'docImportant/expiringCertificate.log')
# Configuration des paramètres importants
tenantId = ''
clientId = ''
teamId = ''
channelId = ''
cacheFile = './docImportant/TokenCache.json'
scopes = ['https://graph.microsoft.com/ChannelMessage.Send', 
          'https://graph.microsoft.com/Group.ReadWrite.All']

logging.basicConfig(
    filename=logFile,             # Chemin du fichier de log en cas d'erreur
    level=logging.INFO,           # Pour plus de détails
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

# Récupération du contenu du fichier JSON avec les applications expirées/expirantes
with open('./docImportant/ExpiringApps.json', 'r', encoding='utf-8') as expiringFile:
    items = json.load(expiringFile)
    messageContent = ""
    if items == []:
        messageContent += "<b> Aucun secrets ou certificats n'ont expiré. </b>"
    else : # Création du message à envoyer dans Teams avec les informations des applications
        messageContent += "<b> Secrets et certificats expirés :</b> <br> <br>"
        for item in items: # Formalisation du message en HTML pour faciliter la lecture dans Teams
            if item['Status'] != 'Expiré':
                continue  # Ne montrer que les éléments expirés
            else : 
                messageContent += f"<p> Application: {item['Application']}</p>"
                messageContent += f"<p> ID de l'application: {item['AppID']}</p>"
                messageContent += f"<p> Type: {item['Type']}</p>"
                messageContent += f"<p> Date de fin: {item['EndDate']}</p>"
                messageContent += f"<p> Statut: {item['Status']}</p>"
                messageContent += f"<p> {"-" * 40}</p>"

# Classe qui va gérer l'authentification complète avec MSAL
class MSALAuthenticationProvider:
    def __init__(self, msalApp, scopes, cacheFile):
        self.msalApp = msalApp
        self.scopes = scopes
        self.cacheFile = cacheFile

    # Méthode pour obtenir le token d'accès    
    def get_token(self):
        accounts = self.msalApp.get_accounts()
        if accounts: # Si un compte se trouve en cache, on le récupère
            result = self.msalApp.acquire_token_silent(self.scopes, account=accounts[0])
            if result and "access_token" in result: # Si le token est valide, on le retourne
                if self.msalApp.token_cache.has_state_changed: # Si le token a changé, on met à jour le cache
                    with open(self.cacheFile, 'w') as f:
                        f.write(self.msalApp.token_cache.serialize())
                return result["access_token"]
        
        # Sinon, on génère un nouveau token via le flux device code
        # L'utilisateur doit suivre les instructions affichées pour s'authentifier et enregistrer un nouveau token
        flow = self.msalApp.initiate_device_flow(scopes=self.scopes)
        # Troncage du message pour ne garder que le code
        flow["message"] = flow["message"].replace('To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ', '')
        flow["message"] = flow["message"].replace(' to authenticate.', '')
        
        pyperclip.copy(flow["message"])                         # Copie du code dans le presse-papier pour faciliter l'authentification
        webbrowser.open('https://microsoft.com/devicelogin')    # Ouverture automatique de la page d'authentification dans le navigateur
        logging.info(f"{os.path.basename(__file__)} : Code d'authentification copié dans le presse-papier : {flow['message']}")

        # Attente de l'authentification de l'utilisateur
        result = self.msalApp.acquire_token_by_device_flow(flow)
        
        if "access_token" in result: # Si le token est obtenu avec succès, on le retourne
            if self.msalApp.token_cache.has_state_changed: # Mise à jour du cache si le token a changé
                with open(self.cacheFile, 'w') as f:
                    f.write(self.msalApp.token_cache.serialize())
            return result["access_token"]
        else: # Sinon, on renvoie une exception d'échec d'authentification
            logging.error(f"{os.path.basename(__file__)} : Échec de l'authentification: {result.get('error_description', 'Erreur inconnue')}")

# Initialisation du cache MSAL pour récupérer les tokens
cache = msal.SerializableTokenCache()
if os.path.exists(cacheFile):
    with open(cacheFile, 'r') as f:
        cache.deserialize(f.read())

# Initialisation de l'application MSAL et du client Graph pour envoyer le message
msalApp = msal.PublicClientApplication(
    client_id=clientId,
    authority=f"https://login.microsoftonline.com/{tenantId}",
    token_cache=cache
)

# Initialisation du fournisseur d'authentification et du client Graph
authProvider = MSALAuthenticationProvider(msalApp, scopes, cacheFile)

# Fonction pour obtenir le token d'accès
def get_access_token():
    return authProvider.get_token()
# Fonction pour envoyer le message dans le canal Teams spécifié
def send_message():
    token = get_access_token()
    
    # Configuration des headers pour l'appel API
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # URL pour envoyer le message dans le bon canal Teams
    url = f"https://graph.microsoft.com/v1.0/teams/{teamId}/channels/{channelId}/messages"
    # Payload du message avec le contenu formaté en HTML
    payload = {
        "body": {
            "contentType": "html",
            "content": messageContent
        }
    }
    
    # Envoi de la requête POST pour envoyer le message
    response = requests.post(url, json=payload, headers=headers)
    
    # Vérification du succès de l'envoi
    if response.status_code == 201:
        logging.info(f"{os.path.basename(__file__)} : Message envoyé avec succès")
    else:
        logging.error(f"{os.path.basename(__file__)} : Erreur lors de l'envoi: {response.status_code} - {response.text}")

# Exécution de la fonction pour envoyer le message
send_message()