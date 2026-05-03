import matplotlib.pyplot as plt
import os
import logging
import pylab

path = "./docImportant/documentPDF/"  # Chemin du répertoire d'export 
dictExt = {}

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, './docImportant/exportData.log')
logging.basicConfig(
    filename=logFile,             # Chemin du fichier de log
    level=logging.INFO,           # Pour plus de détails
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

def contenuRep(directory, levelMax=0, levelDep=1):
    """Cette méthode parcourt récursivement le contenu d'un répertoire et de ses sous-répertoires pour compter le nombre de fichiers par extension.
    Elle prend en paramètres :
    - dir = le chemin du répertoire à parcourir ;
    - levelMax = le nombre maximum de niveaux de sous-répertoires à parcourir (0 pour parcourir tous les niveaux) ;
    - levelDep = le niveau de sous-répertoire actuel (1 pour le répertoire de départ)."""
    # Récupérer le contenu du répertoire racine dir
    entry = os.listdir(directory)
    entry.sort(key=lambda v: v.upper()) # Trier le contenu du répertoire en mettant tout en majuscules pour éviter la casse
    subDir = [] # Contenir les sous-répertoires
    subFile = [] # Contenir les fichiers

    for entree in entry:
        if os.path.isdir(os.path.join(directory, entree)):
            subDir.append(entree)
        else:
            subFile.append(entree)
    
    # Récupérer les fichiers et leurs extensions
    for file in subFile:
        extension = os.path.splitext(file)[1].lower() # Récupérer l'extension du fichier
        if extension == "":
            pass
        elif extension in dictExt:
            dictExt[extension] += 1
        else:
            dictExt[extension] = 1

    # Appeler la fonction récursivement si les paramètres levelMax et levelDep le permettent       
    if levelMax==0 or levelDep<levelMax:
        for dir in subDir:
            contenuRep(os.path.join(directory, dir), levelMax, levelDep+1)

    
def graphProportion(dictExt):
    """ Cette méthode crée un graphique à barres représentant la proportion de fichiers concernés en fonction de leur extension.
    Elle prend en paramètre :
    - dictExt = un dictionnaire contenant les extensions de fichiers et leur nombre d'occurrences. """
    # On convertit les données en pourcentage    
    sumValues = sum(dictExt.values())
    for key, value in dictExt.items():
        dictExt[key] = value / sumValues * 100

    # Création du graphiques à barres avec les données calculées
    fig, ax = plt.subplots() 
    bar_container = ax.bar(dictExt.keys(), dictExt.values(), # Définition du style du graphique et de ses axes
                           color="blue")
    ax.set(ylabel='Proportion de fichiers concernés (en %)',
           xlabel='Extension de fichier', # Titre des axes et du graphique
           title='Répartition des fichiers en fonction de leur extension\n', 
           ylim=(0,100)) # Définition des limites de l'axe y
    # Affichage des valeurs au-dessus de chaque barre du graphique pour une meilleure lisibilité
    ax.bar_label(bar_container, fmt='{:,.2f}')
    fig.set_size_inches(10, 5)

    # Définition de la limite et des labels de l'axe x
    x = [i for i in range(len(dictExt))]
    pylab.xticks(x, dictExt.keys(), rotation=40)

    # Ajustement de la fenêtre pour obtenir le graphique dans sa totalité lors de l'enregistrement
    plt.tight_layout()
    # Enregistrement du graphique
    fig.savefig('./docImportant/.fileProportion.png')

# Lancement du programme et gestion des erreurs
try : 
    contenuRep(path)
    graphProportion(dictExt)
    logging.info(f"{os.path.basename(__file__)} : Graphique de la proportion de fichiers par extension créé avec succès.")
except Exception as e:
    logging.error(f"{os.path.basename(__file__)} : Erreur : {str(e)}")