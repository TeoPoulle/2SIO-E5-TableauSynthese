import json
import glpi_api
import logging 
import os
import requests
from reportlab.lib.pagesizes import letter                                              # | Remplaçable par la seule ligne :
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle                    # |    import reportlab
from reportlab.lib.units import cm                                                      # |  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer  # | Pour éviter des imports trop gourmants en ressources
from reportlab.lib import colors                                                        # | La bonne pratique est d'importer seulement ce qui est nécessaire
from reportlab.lib.enums import TA_CENTER                                               # | 

url = 'http://localhost:8080/apirest.php'                   # URL de l'API GLPI
apiToken = ''       # Token de l'API
userToken = ''      # Token de l'utilisateur

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, './docImportant/exportData.log')
logging.basicConfig(
    filename=logFile,             # Chemin du fichier de log
    level=logging.INFO,           # Pour plus de détails
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)


def downloadAllDocuments(numberIdJumped, glpiObject, pathToSave):
    """Cette méthode télécharge tous les documents PDF contenus dans la section Management>Documents de GLPI grâce à un API REST.
    Elle prend en paramètres : 
    - numberIdJumped = un nombre d'IDs consécutifs sans document à ignorer au maximum (permet de continuer le téléchargement même si des documents ont été supprimés) ;
    - glpiObject = l'objet de connexion à l'API GLPI ;
    - pathToSave = le chemin absolu où l'utilisateur souhaite sauvegarder les documents."""
    
    reachLimit, iteration = 0, 0
    while reachLimit != numberIdJumped:
        try:
            glpiObject.download_document(iteration, pathToSave)
            reachLimit = 0
            iteration += 1
        except glpi_api.GLPIError:
            reachLimit += 1
            iteration += 1
    logging.info(f"{os.path.basename(__file__)} : Téléchargement des documents dans le répertoire docImportant/documentPDF terminé.")


def exportAllContacts(urlAPI, appToken, userToken):
    """Cette méthode exporte tous les contacts depuis l'API GLPI.
    Elle prend en paramètres : 
    - urlAPI = l'URL de l'API GLPI ;
    - apiToken = le token de l'application ;
    - userToken = le token de l'utilisateur."""
    
    # Obtention d'un token de connexion
    sessionUrl = f'{urlAPI}/initSession'
    headersToken = {
        'App-Token': appToken,
        'Authorization': f'user_token {userToken}'
    }
    sessionResponse = requests.get(sessionUrl, headers=headersToken)

    # En cas de succès de la connexion, on crée une session et on exporte les contacts
    if sessionResponse.status_code == 200:
        sessionToken = sessionResponse.json()['session_token']
        headersSession = {
            'App-Token': appToken,
            'Session-Token': sessionToken 
        }
        contactsUrl = f'{urlAPI}/Contact'
        contacts = requests.get(contactsUrl, headers=headersSession)
        with open('./docImportant/ExportContacts.json', 'w', encoding='utf-8') as jsonFile:
            json.dump(contacts.json(), jsonFile, indent=4, ensure_ascii=False)
        logging.info(f"{os.path.basename(__file__)} : Export des contacts terminé.")
    else:
        logging.error(f"{os.path.basename(__file__)} : Erreur lors de l'initialisation de la session : {sessionResponse.text}")


def downloadContactPDF(jsonFilePath, pdfFilePath):
    """Cette méthode convertit un fichier JSON de contacts en document PDF.
    Elle prend en paramètres : 
    - jsonFilePath = le chemin absolu du fichier JSON des contacts ;
    - pdfFilePath = le chemin absolu du document PDF à créer."""

    with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
        contacts = json.load(jsonFile)

    # Créer le document PDF
    doc = SimpleDocTemplate(pdfFilePath, pagesize=letter, topMargin=1*cm, bottomMargin=1*cm)
    
    # Liste pour stocker les éléments du PDF
    contactData = []
    
    # Titre
    styles = getSampleStyleSheet()
    titleStyle = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.black, spaceAfter=20, alignment=TA_CENTER)
    title = Paragraph("Données des contacts exportés", titleStyle)
    contactData.append(title)
    
    # Style pour le contenu des cellules
    contentStyle = ParagraphStyle('CellContent', parent=styles['Normal'], fontSize=9, leading=10)
    tableStyle = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ])

    # Traitement de chaque contact
    for contact in contacts:
        data = [
            Paragraph(f"<b>Nom :</b> {contact.get('name')}", contentStyle),
            Paragraph(f"<b>Prénom :</b> {contact.get('firstname')}", contentStyle),
            Paragraph(f"<b>Téléphone 1 :</b> {contact.get('phone')}", contentStyle),
            Paragraph(f"<b>Téléphone 2 :</b> {contact.get('phone2')}", contentStyle),
            Paragraph(f"<b>Mobile :</b> {contact.get('mobile')}", contentStyle),
        ]
        width = [3.5*cm for i in range(5)]
        table = Table([data], colWidths=width)
        table.setStyle(tableStyle)
        contactData.append(table)
        
        adresseComplete = f"{contact.get('address')} - {contact.get('postcode')} - {contact.get('town')} - {contact.get('country')}"
        data = [
            Paragraph(f"<b>Email :</b> {contact.get('email')}", contentStyle),
            Paragraph(f"<b>Adresse :</b> {adresseComplete}", contentStyle),
        ]
        width = [5*cm, 12.5*cm]
        table = Table([data], colWidths=width)
        table.setStyle(tableStyle)
        contactData.append(table)
        contactData.append(Spacer(1, 0.5*cm))
    
    # Construction du PDF
    doc.build(contactData)
    logging.info(f"{os.path.basename(__file__)} : Téléchargement des contacts en document PDF terminé.")


try: # Lancement du script
    with glpi_api.connect(url, apiToken, userToken) as glpi:
        logging.info(f"{os.path.basename(__file__)} : Connexion à l'API GLPI réussie.")
        downloadAllDocuments(10, glpi, './docImportant/documentPDF/')
        exportAllContacts(url, apiToken, userToken)
        downloadContactPDF('./docImportant/ExportContacts.json', './docImportant/documentPDF/contactPDF.pdf')

# Gestion des erreurs
except glpi_api.GLPIError as err:
    logging.error(f"{os.path.basename(__file__)} : {str(err)}")
except Exception as e:
    logging.error(f"{os.path.basename(__file__)} : Une erreur inattendue est survenue : {str(e)}")