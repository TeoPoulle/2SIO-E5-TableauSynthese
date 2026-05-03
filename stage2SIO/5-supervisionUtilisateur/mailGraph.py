import matplotlib.pyplot as plt
import json
import pylab
from PIL import Image
import os
import logging

# Données d'initialisation
labels = ["0-9%", "10-19%", "20-29%", "30-39%", "40-49%", "50-59%", "60-69%", "70-79%", "80-89%", "90-100%"]
values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Récupération des données à partir du fichier JSON généré par le script infoMailbox.py
with open('./fichierImportant/MailboxInfo.json', 'r', encoding='utf-8') as jsonFile:
    datas = json.load(jsonFile)

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, './fichierImportant/mailbox.log')

logging.basicConfig(
    filename=logFile,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def convertImage(imageDeb, imageFin, moreIf="1==1", gray=False):
    """Cette méthode permet de convertir une image en une autre avec un fond transparent, en fonction d'une condition définie par moreIf. Si gray est à True, l'image finale sera convertie en niveaux de gris.
    Elle prend en paramètres :
    - imageDeb : le chemin de l'image à convertir ; 
    - imageFin : le chemin de l'image convertie à enregistrer ; 
    - moreIf : une condition à respecter pour que les pixels soient rendus transparents (par défaut, tous les pixels ayant la même valeur pour les trois composantes de couleur seront rendus transparents) ; 
    - gray : un booléen qui permet de convertir l'image finale en niveaux de gris (par défaut, False). 
    
    * moreIf doit être une expression arbitraire, par défaut "1==1" (signifie aussi True) pour qu'aucune influence ne soit exercée.
    La méthode eval() permet d'évaluer des expressions arbitraires à partir d'une entrée basée sur des chaînes de caractères ou un code compilé. Cette fonction peut être pratique lorsque l'on essaye d'évaluer dynamiquement les expressions Python.
    * gray doit être à True pour que l'image finale soit convertie en niveaux de gris. Dans ce cas, les pixels rendus transparents seront blancs (255) et les autres pixels seront convertis en niveaux de gris (entre 0 et 255). 
    Si gray est à False (valeur par défaut), les pixels rendus transparents seront transparents (0) et les autres pixels conserveront leur couleur d'origine.
    """
    # Ouverture de l'image à convertir et récupération de ses données
    image = Image.open(imageDeb).convert("RGBA")
    datas = image.get_flattened_data()

    newData = [] # Pour chaque tuple de données de l'image : (R, G, B, A)
    for item in datas:
        if item[0] == item[1] == item[2] and eval(moreIf): # Si les trois composantes de couleur sont égales et que la condition définie par moreIf (par défaut, elle est toujours respectée) est respectée
            newData.append((255, 255, 255, 0)) # Le pixel est rendu transparent
        else: # Sinon, le pixel conserve sa couleur d'origine
            if gray == True :
                item = (175, 175, 175, item[3]) # Si gray est à True, les pixels non transparents sont convertis en gris (entre 0 et 255)
            newData.append(item)
    # On met à jour les données de l'image avec les nouvelles données et on enregistre l'image convertie
    image.putdata(newData)
    image = image.convert("RGBA")
    image.save(imageFin)

    if gray == True: # Si gray est à True, on convertit l'image en niveaux de gris
        image = Image.open(imageFin).convert("L")
        plt.imsave(imageFin, image, cmap="gray", vmin=0, vmax=255)


def convertDatas(datas):
    """Cette méthode permet de convertir les données du fichier JSON en pourcentages de boîtes mail concernées pour chaque tranche de pourcentage de stockage utilisé. 
    Elle prend en paramètre :
    - datas : les données du fichier JSON à convertir (une liste de dictionnaires contenant les informations sur les boîtes mail). 
    """
    # A chaque fois que l'on détecte un pourcentage, on incrémente le compteur correspondant dans la liste sizes
    for data in datas:
        if data['usedPercentage'] >= 0 and data['usedPercentage'] < 10:
            values[0] += 1 # Compteur pour les boîtes mail avec un pourcentage de stockage utilisé entre 0 et 9,99% (inclus)
        elif data['usedPercentage'] >= 10 and data['usedPercentage'] < 20:
            values[1] += 1 # Compteur pour les boîtes mail utilisées entre 10 et 19,99% (inclus) de leur stockage maximum
        elif data['usedPercentage'] >= 20 and data['usedPercentage'] < 30:
            values[2] += 1 # 20 et 29,99% (inclus)
        elif data['usedPercentage'] >= 30 and data['usedPercentage'] < 40:
            values[3] += 1 # 30 et 39,99% (inclus)
        elif data['usedPercentage'] >= 40 and data['usedPercentage'] < 50:
            values[4] += 1 # 40 et 49,99% (inclus)
        elif data['usedPercentage'] >= 50 and data['usedPercentage'] < 60:
            values[5] += 1 # 50 et 59,99% (inclus)
        elif data['usedPercentage'] >= 60 and data['usedPercentage'] < 70:
            values[6] += 1 # 60 et 69,99% (inclus)
        elif data['usedPercentage'] >= 70 and data['usedPercentage'] < 80:
            values[7] += 1 # 70 et 79,99% (inclus)
        elif data['usedPercentage'] >= 80 and data['usedPercentage'] < 90:
            values[8] += 1 # 80 et 89,99% (inclus)
        else:
            values[9] += 1 # 90 et 100% 

    # On convertit les données en pourcentage        
    for i in range(len(values)):
        values[i] = values[i] / len(datas) * 100

def createGraph(labels, values):
    """Cette méthode permet de créer un graphique à barres avec les données converties : 
        - en définissant le style du graphique et de ses axes ; 
        - en affichant les valeurs au-dessus de chaque barre du graphique pour une meilleure lisibilité ; 
        - en définissant la limite et les labels de l'axe x ;
        - en ajustant la fenêtre pour obtenir le graphique dans sa totalité lors de l'enregistrement ; 
        - et en enregistrant le graphique.
    Elle prend en paramètres :
    - labels : les labels de l'axe x du graphique ; 
    - values : les valeurs de l'axe y du graphique. 
    """
    # Création du graphiques à barres avec les données calculées
    fig, ax = plt.subplots() 
    bar_container = ax.bar(labels, values, # Définition du style du graphique et de ses axes
                           color=['darkgreen', 'green', '#67cb57', '#d2e33c', 'yellow', 'gold', 'orange', 'orangered', 'red', 'darkred'])
    ax.set(ylabel='Proportion de boîtes mail concernées (en %)',
           xlabel='Pourcentage de stockage utilisé', # Titre des axes et du graphique
           title='Répartition des boîtes mail (en %) en fonction\n du pourcentage de stockage utilisé\n', 
           ylim=(0,100)) # Définition des limites de l'axe y
    # Affichage des valeurs au-dessus de chaque barre du graphique pour une meilleure lisibilité
    ax.bar_label(bar_container, fmt='{:,.2f}', color='#000000')

    # Définition de la limite et des labels de l'axe x
    x = [i for i in range(0,10)]
    pylab.xticks(x, labels, rotation=40)

    # Ajustement de la fenêtre pour obtenir le graphique dans sa totalité lors de l'enregistrement
    plt.tight_layout()
    # Enregistrement du graphique
    fig.savefig('./fichierImportant/graphique.png')
    logging.info(f"{os.path.basename(__file__)} : Graphique créé et enregistré avec succès : graphique.png")

try : # Création des graphiques et traitement des données pour l'affichage final
    convertDatas(datas)
    if not os.path.exists('./fichierImportant/graphique.png') :
        createGraph(labels, values)
    convertImage("./fichierImportant/graphique.png", "./fichierImportant/grayScale.png", gray=True)
    createGraph(labels, values)
    convertImage("./fichierImportant/graphique.png", "./fichierImportant/graphDiffere.png", moreIf="item[0] > 240")
    # Création du graphique d'affichage final en superposant le graphique avec fond transparent sur le graphique en niveaux de gris
    image = Image.open("./fichierImportant/graphDiffere.png")
    graph = Image.open("./fichierImportant/grayScale.png")
    graph.paste(image, (7, 0), image)
    graph.save("./fichierImportant/graphDiffere.png")
    logging.info(f"{os.path.basename(__file__)} : Graphique final créé et enregistré avec succès : graphDiffere.png")

except Exception as e: # Gestion des exceptions
    logging.error(f"{os.path.basename(__file__)} : Une erreur est survenue lors de la création des graphiques : %s", str(e))