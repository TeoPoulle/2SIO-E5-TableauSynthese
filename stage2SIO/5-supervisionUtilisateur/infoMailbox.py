import os
import logging
import requests
import json

# Configuration des valeurs importantes
clientId = ''          # ID de l'application qui permet au programme d'accéder aux applications
clientSecret = ''  # Secret qui apparaîtra en même temps que l'ID
tenantName = ''                          # Domaine liée à Microsoft Entra
jsonAffiche = []

# URLs qui seront utilisées pour les appels API
loginUrl = 'https://login.microsoftonline.com'
graphUrl = 'https://graph.microsoft.com'
userUrl = f"{graphUrl}/v1.0/users/"

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, './fichierImportant/mailbox.log')

logging.basicConfig(
    filename=logFile,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def getAccessToken(loginUrl, clientId, clientSecret, tenantName):
    """Cette fonction permet d'obtenir un token d'accès pour l'API Microsoft Graph.
    Elle prend en paramètres : 
    - loginUrl = l'URL de connexion à Microsoft ;
    - clientId = l'ID de l'application répertorié dans Microsoft Entra ;
    - clientSecret = le secret de l'application aussi trouvable dans Microsoft Entra ;
    - tenantName = le nom de domaine lié à Microsoft Entra."""

    tokenUrl = f"{loginUrl}/{tenantName}/oauth2/v2.0/token"
    data = { # Données nécessaires pour obtenir le token
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(tokenUrl, data=data)

    if response.status_code != 200: # Si la demande de token a échoué, on met un message d'erreur dans les logs
        logging.error(f"{os.path.basename(__file__)} : Erreur lors de la demande de token: %s", response.status_code)
        logging.error(f"{os.path.basename(__file__)} : Réponse: %s", response.text)
    
    return response.json()


def infoUser(userUrl, headers):
    """Cette fonction récupère la liste des utilisateurs de l'organisation via l'API Microsoft Graph.
    Elle prend en paramètres : 
    - userUrl = l'URL de l'API Graph qui permet de lister les utilisateurs ;
    - headers = les headers nécessaires pour l'appel API (avec notamment le token d'accès)."""
    jsons = []

    while userUrl:
        # Appel API pour lister les utilisateurs
        response = requests.get(userUrl, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Pour chaque utilisateur, on récupère les informations de base
        for user in data.get('value', []):
            mailboxInfo = {
                'displayName': user.get('displayName'),
                'mail': user.get('mail'),
                'userPrincipalName': user.get('userPrincipalName'),
                'id': user.get('id')
            }

            # Petit filtre pour éviter les utilisateurs externes
            if mailboxInfo['mail'][1] == '.' or mailboxInfo['mail'][2] == '.' :
                if mailboxInfo['mail'].find('adresseValide.fr') != -1 :
                    jsons.append(mailboxInfo)

        # Pagination pour récupérer les utilisateurs suivants
        userUrl = data.get('@odata.nextLink', None)

    return jsons


def infoMailbox(mailboxes, headers):
    """Cette méthode récupère les informations de stockage des boîtes mail des utilisateurs.
    Elle prend en paramètres : 
    - mailboxes = la liste des utilisateurs avec leurs informations de base ;
    - headers = les headers nécessaires pour l'appel API (avec notamment le token d'accès)."""

    # Pour chaque utilisateur, on récupère les informations de stockage de sa boîte mail
    for mailbox in mailboxes:
        mailUrl = f"{graphUrl}/v1.0/users/{mailbox['id']}/mailFolders/"
        responseMail = requests.get(mailUrl, headers=headers)
        mailData = responseMail.json()

        # Calcul du pourcentage de stockage utilisé
        calculatePercentage(mailData, mailbox)


def calculatePercentage(jsonMailInfo, user):
    """Cette méthode calcule le pourcentage de stockage utilisé dans la boîte mail d'un utilisateur.
    Elle prend en paramètres : 
    - jsonMailInfo = les informations des dossiers de la boîte mail de l'utilisateur ;
    - user = le dictionnaire contenant les informations de l'utilisateur."""

    stockageMax = 49.5 * 1024**3      # Le stockage maximale des boîtes mails (49,5 Go)
    # La valeur utilisée pour le stockage est le byte (ou octet en français)
    usedPercentage = 0              # Pourcentage de stockage utilisé (réinitialisé à 0)
    stockageBytes = 0               # Initialisation de la taille utilisée en bytes

    # Pour chaque dossier de la boîte mail, on récupère la taille utilisée et on la calcule en pourcentage
    for data in jsonMailInfo.values():
        if type(data) == list :
            for folder in data :
                for key, value in folder.items():
                    if key == 'sizeInBytes' :
                        stockageBytes += value
    usedPercentage = (stockageBytes / stockageMax) * 100
    
    if usedPercentage == 0 : # Si la boîte mail n'est pas utilisée, on ne l'affiche pas dans le tableau
        pass
    else: 
        jsonAffiche.append({
            'userName' : user['displayName'],
            'userMail' : user['mail'],
            'usedPercentage' : float(format(usedPercentage, ".2f"))
        })

    return jsonAffiche

def classement(dict):
    """Cette fonction permet de trier les dictionnaires en fonction du pourcentage de stockage utilisé.
    Elle prend en paramètres : 
    - dict = le dictionnaire à trier."""
    return dict['usedPercentage']

try : 
    # Obtenir le token
    oauth = getAccessToken(loginUrl, clientId, clientSecret, tenantName)
    accessToken = oauth['access_token']
    tokenType = oauth['token_type']

    # Headers pour les appels API
    headers = {
        'Authorization': f"{tokenType} {accessToken}",
        'Content-Type': 'application/json'
    }

    # Lancement des fonctions
    users = infoUser(userUrl, headers)
    logging.info(f"{os.path.basename(__file__)} : Nombre d'utilisateurs récupérés : {len(users)}")
    infoMailbox(users, headers)
    logging.info(f"{os.path.basename(__file__)} : Informations de stockage des boîtes mail récupérées avec succès.")
    
    jsonAffiche = sorted(jsonAffiche, key=classement, reverse=True)

    with open('./fichierImportant/MailboxInfo.json', 'w', encoding='utf-8') as jsonFile:
        json.dump(jsonAffiche, jsonFile, indent=4, ensure_ascii=False)
    logging.info(f"{os.path.basename(__file__)} : Fichier JSON créé avec succès : MailboxInfo.json")
    logging.info("")

except Exception as e: # Gestion des erreurs avec un message générique dans les logs
    logging.error(f"{os.path.basename(__file__)} : Une erreur est survenue : {str(e)}")
