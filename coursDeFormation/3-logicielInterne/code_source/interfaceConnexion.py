import mysql.connector
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
                            QLabel, QLineEdit, QComboBox, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from interfaceAppli import fenetreAppli

class fenetreConnexion(QWidget) :
    def __init__(self) :
        QWidget.__init__(self)
        
        self.resize(500, 250)
        contenuFenetre = QVBoxLayout()
        self.setLayout(contenuFenetre)

        # Gérer l'affichage des éléments sur la fenêtre
        self.label = QLabel()
        self.labelLogo = QLabel()
        
        # Logo MOVA
        self.logoMova = QPixmap('LogoMOVA.ico')
        self.labelLogo.setPixmap(self.logoMova)
        contenuFenetre.addWidget(self.labelLogo, alignment=QtCore.Qt.AlignCenter)
        
        # Identifiants
        self.labelIdentifiant = QLabel("Votre identifiant :")
        contenuFenetre.addWidget(self.labelIdentifiant)
        self.identifiant = QLineEdit()
        self.identifiant.setMaximumWidth(150)
        contenuFenetre.addWidget(self.identifiant, alignment=QtCore.Qt.AlignCenter)

        # Mots de passe
        self.labelPassword = QLabel("Votre mot de passe :")
        contenuFenetre.addWidget(self.labelPassword)
        self.password = QLineEdit()
        self.password.setMaximumWidth(150)
        self.password.setEchoMode(QLineEdit.Password)
        contenuFenetre.addWidget(self.password, alignment=QtCore.Qt.AlignCenter)

        # Bouton de connexion
        self.boutonConnexion = QPushButton("Se connecter")
        self.boutonConnexion.clicked.connect(lambda: self.droitConnexion(self.identifiant.text(), \
                                                                         self.mdpSecurise(self.password.text())))
        contenuFenetre.addWidget(self.boutonConnexion, alignment=QtCore.Qt.AlignCenter)

        # Label
        contenuFenetre.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        # Mise en forme et style de la fenêtre
        self.labelIdentifiant.setAlignment(Qt.AlignTop)
        self.labelIdentifiant.setAlignment(Qt.AlignHCenter)
        self.labelPassword.setAlignment(Qt.AlignTop)
        self.labelPassword.setAlignment(Qt.AlignHCenter)
        self.boutonConnexion.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelIdentifiant.setStyleSheet("QLabel {font-weight: bold}")
        self.labelPassword.setStyleSheet("QLabel {font-weight: bold}")

        # Nom de la fenêtre
        self.setWindowTitle("Application MOVA")

    # Eviter que le mot de passe soit en clair dans la BDD
    def mdpSecurise(self, password) :
        hashMdp = hashlib.sha512()
        hashMdp.update(password.encode("utf-8"))
        return hashMdp.hexdigest()

    # Fonction utilisée pour initier la connexion d'un utilisateur
    def droitConnexion(self, username, password) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        reponse = ""
        if connection.is_connected() :
            requete = f"SELECT nomUtilisateur, motDePasse FROM employe WHERE nomUtilisateur='{username}' ;"
            cursor.execute(requete)
            resultat = cursor.fetchall()
            if [(username,password)] == resultat :
                self.label.setText("Connexion réussie !")
                self.close()
                reponse = True
            else:
                self.label.setText("Identifiant ou mot de passe incorrect !")
                self.password.setStyleSheet("QLineEdit {background-color: #ffb4a4}")
        return reponse
