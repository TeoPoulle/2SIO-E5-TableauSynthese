import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QApplication
from interfaceConnexion import fenetreConnexion
from interfaceAppli import fenetreAppli
import sys

try :
    # Établissement de la connexion
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bddmova')
    
    # Création d'un curseur pour récupérer les données dans la BDD
    cursor = connection.cursor()

    if connection.is_connected():
        
        application = QApplication.instance() # Le pb vient toujours de là
        if not application :
            application = QApplication(sys.argv)
            fenetre = fenetreConnexion()
            appli = fenetreAppli()
            fenetre.show()
            application.exec_()

            # Initier l'ouverture de l'application
            username = fenetre.identifiant.text()
            password = fenetre.mdpSecurise(fenetre.password.text())
            if fenetre.droitConnexion(username, password) == True :
                appli.show()

except Error as e:
    print(f"Erreur : {e}")

finally:
    # Toujours fermer la connexion
    if connection.is_connected():
        cursor.close()
        connection.close()

