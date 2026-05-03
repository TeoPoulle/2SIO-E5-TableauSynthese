import json
import matplotlib.pyplot as plt

# Définition des variables importantes pour le graphique camembert
labels = ["Ordinateur", "Ecran", "Equipement Réseau", "Imprimante", "Téléphone"]
sizes = [0, 0, 0, 0, 0]
categories = ["Computer", "Monitor", "NetworkEquipment", "Printer", "Phone"]

# On récupère les données de chaque catégorie et on incrémente le nombre correspondant
for categorie in categories:
    with open(f"./docImportant/jsonData/Export{categorie}.json", "r") as dataFile:
        datas = json.load(dataFile) # On ouvre le fichier JSON de la catégorie en cours et on charge les données
    for data in datas['data'] : 
        if categorie == "Computer" :
            sizes[0] += 1 # Si l'élément est un ordinateur, on incrémente la première valeur de la liste sizes
        elif categorie == "Monitor" :
            sizes[1] += 1 # Si l'élément est un écran, on incrémente la deuxième valeur de la liste sizes
        elif categorie == "NetworkEquipment" :
            sizes[2] += 1 # Si l'élément est un équipement réseau, on incrémente la troisième valeur
        elif categorie == "Printer" :
            sizes[3] += 1 # Si l'élément est une imprimante, on incrémente la quatrième valeur
        else : 
            sizes[4] += 1 # Si l'élément est un téléphone, on incrémente la cinquième valeur

def autopctValue(value): 
    """Cette fonction permet de récupérer le nombre d'équipement réel à partir de sa valeur en pourcentage. 
    Elle prend en paramètre : 
    - value : la valeur en pourcentage de la part du camembert"""
    return f"{value/100 * sum(sizes):.0f}"

# Création et enregistrement du graphique circulaire
plt.pie(sizes, labels=labels, autopct=autopctValue)
plt.title("Graphique circulaire représentant la quantité \nd'équipements par catégorie")
plt.savefig('./docImportant/graphMateriel.png')