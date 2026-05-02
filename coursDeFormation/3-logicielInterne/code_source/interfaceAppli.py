import mysql.connector
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
                            QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
                            QCheckBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

# Erreur avec les checkbox
# Erreur avec requete pour les réservations
# ==> l'appli se ferme mais aucune erreur dans console

class fenetreAppli(QWidget) :
    def __init__(self) :
        QWidget.__init__(self)

        self.resize(750, 500)
        contenuAppli = QVBoxLayout()
        self.setLayout(contenuAppli)

        self.ongletAppli = onglet()
        contenuAppli.addWidget(self.ongletAppli)

        self.setWindowTitle("Application MOVA")

class onglet(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        self.layout = QVBoxLayout(self) 
  
                    # Mise en place des onglets
        self.onglet = QTabWidget() 
        self.rechercher = QWidget() 
        self.disponible = QWidget() 
        self.reserver = QWidget()
        self.reparation = QWidget()
        self.infoLocation = QWidget()
        self.parametres = QWidget()
  
                    # Ajouter les onglets à la page principale 
        self.onglet.addTab(self.rechercher, "Recherche") 
        self.onglet.addTab(self.disponible, "Disponible") 
        self.onglet.addTab(self.reserver, "Réservation")
        self.onglet.addTab(self.reparation, "Réparation") 
        self.onglet.addTab(self.infoLocation, "Information location") 
        self.onglet.addTab(self.parametres, "Paramètres")
  
                    # Onglet Recherche 
        self.rechercher.layout = QGridLayout()
        self.rechercher.setLayout(self.rechercher.layout)
        self.label = QLabel("Recherche avec critère") 
        self.rechercher.layout.addWidget(self.label, 0, 1) 
                # Choisir une table
        self.labelListTable = QLabel("Sélectionner une section")
        self.rechercher.layout.addWidget(self.labelListTable, 1, 1)
        self.optionClient = QPushButton("Client")
        self.rechercher.layout.addWidget(self.optionClient, 2, 0)
        self.optionClient.clicked.connect(lambda: self.checkClient())
        self.optionVehic = QPushButton("Véhicule")
        self.rechercher.layout.addWidget(self.optionVehic, 2, 1)
        self.optionVehic.clicked.connect(lambda: self.checkVehic())
        self.optionLocat = QPushButton("Location")
        self.rechercher.layout.addWidget(self.optionLocat, 2, 2)
        self.optionLocat.clicked.connect(lambda: self.checkLocat())
                # La suite de la recherche
        self.labelCheck = QLabel()
        self.rechercher.layout.addWidget(self.labelCheck, 3, 1)
        self.labelOptDispo = QLabel()
        self.textRecherche = QLineEdit()
        self.rechercher.layout.addWidget(self.labelOptDispo, 4, 0)
            # Bouton de recherche et de réinitialisation
        self.boutonSoumettreClient = QPushButton("Rechercher")
        self.boutonSoumettreClient.setMaximumWidth(200)
        self.boutonSoumettreClient.clicked.connect(lambda: self.algoRechercheClient(self.textRecherche.text()))
        self.boutonSoumettreVehic = QPushButton("Rechercher")
        self.boutonSoumettreVehic.setMaximumWidth(200)
        self.boutonSoumettreVehic.clicked.connect(lambda: self.algoRechercheVehic(self.textRecherche.text()))
        self.boutonSoumettreLocat = QPushButton("Rechercher")
        self.boutonSoumettreLocat.setMaximumWidth(200)
        self.boutonSoumettreLocat.clicked.connect(lambda: self.boutonSoumettreLocat(self.textRecherche.text()))
        self.boutonEffacer = QPushButton("Nouvelle recherche")
        self.boutonEffacer.clicked.connect(lambda: self.reinitRecherche())
                # Affichage du résultat
        self.labelResRech = QLabel()
        self.rechercher.layout.addWidget(self.labelResRech, 6, 0)
                # Style de la fenêtre
        self.optionClient.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.optionVehic.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.optionLocat.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonSoumettreClient.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonSoumettreVehic.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonSoumettreLocat.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonEffacer.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelCheck.setStyleSheet("QLabel {font-weight: bold}")
        self.label.setStyleSheet("QLabel {font-weight: bold}")

                    # Onglet Disponible
        self.disponible.layout = QGridLayout()
        self.disponible.setLayout(self.disponible.layout)
                # Recherche à partir de la disponibilité
        self.labelDispo = QLabel("Recherche à partir de la disponibilité d'un véhicule")
        self.disponible.layout.addWidget(self.labelDispo, 0, 0)
            # Entrée paramètres
        self.labelRechDispo = QLabel("Le(s) véhicule(s) est(sont)-il(s) disponible(s) ?")
        self.disponible.layout.addWidget(self.labelRechDispo, 1, 0)
        self.rechDispo = QLineEdit()
        self.rechDispo.setMaximumWidth(150)
        self.disponible.layout.addWidget(self.rechDispo, 2, 0)
            # Bouton de recherche
        self.boutonRechDispo = QPushButton("Rechercher")
        self.boutonRechDispo.clicked.connect(lambda: self.validRechDispo(self.rechDispo.text()))
        self.boutonRechDispo.setMaximumWidth(150)
        self.disponible.layout.addWidget(self.boutonRechDispo, 3, 0)
            # Bouton de réinitialisation
        self.boutonNewSearch = QPushButton("Nouvelle recherche")
        self.boutonNewSearch.clicked.connect(lambda: self.reinitDispo())
        self.disponible.layout.addWidget(self.boutonNewSearch, 3, 1)
        self.boutonNewSearch.setMaximumWidth(150)
            # Label de résultat
        self.labelRepRechDispo = QLabel()
        self.disponible.layout.addWidget(self.labelRepRechDispo, 4, 0)
                # Style de la fenêtre
        self.boutonRechDispo.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonNewSearch.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelDispo.setStyleSheet("QLabel {font-weight: bold}")

                    # Onglet Réservation
        self.reserver.layout = QGridLayout()
        self.reserver.setLayout(self.reserver.layout)
                # Recherche des véhicules disponibles
        self.labelReser = QLabel("Réserver un véhicule")
        self.reserver.layout.addWidget(self.labelReser, 0, 0)
        self.labelVehicDispo = QLabel()
        self.reserver.layout.addWidget(self.labelVehicDispo, 1, 0)
        self.labelAffichDispo = QLabel()
        self.reserver.layout.addWidget(self.labelAffichDispo, 2, 0)
            # Bouton de recherche
        self.boutonRechRes = QPushButton("Rechercher les véhicules disponibles")
        self.boutonRechRes.clicked.connect(lambda: self.affichDispo())
        self.reserver.layout.addWidget(self.boutonRechRes, 3, 1)
                # Réserver un véhicule
        self.labelSelecVehic = QLabel("Numéro du véhicule à réserver")
        self.reserver.layout.addWidget(self.labelSelecVehic, 4, 0)
        self.selecVehicRes = QLineEdit()
        self.selecVehicRes.setMaximumWidth(150)
        self.reserver.layout.addWidget(self.selecVehicRes, 4, 1)
                # Réserver pour un client
        self.labelSelecClient = QLabel("Numéro du client")
        self.reserver.layout.addWidget(self.labelSelecClient, 5, 0)
        self.selecClientRes = QLineEdit()
        self.selecClientRes.setMaximumWidth(150)
        self.reserver.layout.addWidget(self.selecClientRes, 5, 1)
                # Date de début
        self.labelSelecDateDeb = QLabel("Date de début (aaaa-mm-jj)")
        self.reserver.layout.addWidget(self.labelSelecDateDeb, 6, 0)
        self.selecDateDeb = QLineEdit()
        self.selecDateDeb.setMaximumWidth(150)
        self.reserver.layout.addWidget(self.selecDateDeb, 6, 1)
                # Date de fin
        self.labelSelecDateFin = QLabel("Date de fin (aaaa-mm-jj)")
        self.reserver.layout.addWidget(self.labelSelecDateFin, 7, 0)
        self.selecDateFin = QLineEdit()
        self.selecDateFin.setMaximumWidth(150)
        self.reserver.layout.addWidget(self.selecDateFin, 7, 1)
            # Bouton de confirmation
        self.boutonConfirm = QPushButton("Confirmer")
        self.boutonConfirm.clicked.connect(lambda: self.confirmRes(self.selecVehicRes.text(), \
                                                                   self.selecClientRes.text(), \
                                                                   self.selecDateDeb.text(), \
                                                                   self.selecDateFin.text()))
        self.reserver.layout.addWidget(self.boutonConfirm, 8, 1)
            # Affichage de la confirmation
        self.labelConfirmRes = QLabel()
        self.reserver.layout.addWidget(self.labelConfirmRes, 9, 0)
            # Bouton nouvelle recherche
        self.boutonRecommencer = QPushButton("Nouvelle réservation")
        self.boutonRecommencer.clicked.connect(lambda: self.reinitReser())
        self.reserver.layout.addWidget(self.boutonRecommencer, 9, 1)

                # Style de la fenêtre
        self.boutonRechRes.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonConfirm.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonRecommencer.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelReser.setStyleSheet("QLabel {font-weight: bold}")

                    # Onglet Réparation
        self.reparation.layout = QGridLayout()
        self.reparation.setLayout(self.reparation.layout)
                # Entrée paramètres
        self.labelRechRepar = QLabel("Véhicule en réparation et/ou maintenance")
        self.reparation.layout.addWidget(self.labelRechRepar, 0, 1)
        self.labelIndic = QLabel("Envoyer ou récupérer un véhicule de maintenance")
        self.reparation.layout.addWidget(self.labelIndic, 1, 0)
        self.numVehic = QLineEdit()
        self.numVehic.setMaximumWidth(150)
        self.reparation.layout.addWidget(self.numVehic, 1, 1)
            # Bouton d'envoie
        self.envoieRepar = QPushButton("Envoyer")
        self.envoieRepar.clicked.connect(lambda: self.validEnvRepar(self.numVehic.text()))
        self.envoieRepar.setMaximumWidth(150)
        self.reparation.layout.addWidget(self.envoieRepar, 2, 0)
            # Bouton de récupération
        self.recupRepar = QPushButton("Récupérer")
        self.recupRepar.clicked.connect(lambda: self.validRecupRepar(self.numVehic.text()))
        self.recupRepar.setMaximumWidth(150)
        self.reparation.layout.addWidget(self.recupRepar, 2, 1)
            # Bouton de nouvelle recherche
        self.nouvRech = QPushButton("Nouvelle recherche")
        self.nouvRech.clicked.connect(lambda: self.reinitRepar())
        self.nouvRech.setMaximumWidth(150)
        self.reparation.layout.addWidget(self.nouvRech, 2, 2)
                # Information réparation
        self.labelInfoEnvoie = QLabel()
        self.reparation.layout.addWidget(self.labelInfoEnvoie, 3, 1)
        self.labelInfoEnvoieRep = QLabel()
        self.reparation.layout.addWidget(self.labelInfoEnvoieRep, 4, 1)
                # Style de la fenêtre
        self.envoieRepar.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.recupRepar.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.nouvRech.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelRechRepar.setStyleSheet("QLabel {font-weight: bold}")
        
                    # Onglet Information location
        self.infoLocation.layout = QGridLayout()
        self.infoLocation.setLayout(self.infoLocation.layout)
                # Recherche à partir d'un véhicule
        self.labelVehic = QLabel("Recherche à partir d'un véhicule")
        self.infoLocation.layout.addWidget(self.labelVehic, 0, 0)
            # Entrée de paramètres
        # Marque
        self.labelRechMarque = QLabel("Marque ?")
        self.infoLocation.layout.addWidget(self.labelRechMarque, 1, 0)
        self.labelRechMarque.setMaximumWidth(100)
        self.rechMarque = QLineEdit()
        self.infoLocation.layout.addWidget(self.rechMarque, 1, 1, alignment=Qt.AlignRight)
        self.rechMarque.setMaximumWidth(150)
        # Modele
        self.labelRechModele = QLabel("Modèle ?")
        self.infoLocation.layout.addWidget(self.labelRechModele, 2, 0)
        self.labelRechModele.setMaximumWidth(100)
        self.rechModele = QLineEdit()
        self.infoLocation.layout.addWidget(self.rechModele, 2, 1, alignment=Qt.AlignRight)
        self.rechModele.setMaximumWidth(150)
        # Type
        self.labelRechType = QLabel("Type ?")
        self.infoLocation.layout.addWidget(self.labelRechType, 3, 0)
        self.labelRechType.setMaximumWidth(100)
        self.rechType = QLineEdit()
        self.infoLocation.layout.addWidget(self.rechType, 3, 1, alignment=Qt.AlignRight)
        self.rechType.setMaximumWidth(150)
            # Bouton de lancement de recherche
        self.boutonRechVehic = QPushButton("Rechercher")
        self.boutonRechVehic.clicked.connect(lambda: self.validRechVehic(self.rechMarque.text(),
                                                                         self.rechModele.text(),
                                                                         self.rechType.text()))
        self.infoLocation.layout.addWidget(self.boutonRechVehic, 4, 0)
        self.boutonRechVehic.setMaximumWidth(150)
            # Bouton de réinitialisation
        self.boutonNouvRech = QPushButton("Nouvelle recherche")
        self.boutonNouvRech.clicked.connect(lambda: self.reinitVehic())
        self.infoLocation.layout.addWidget(self.boutonNouvRech, 4, 1)
        self.boutonNouvRech.setMaximumWidth(150)
            # Label de résultat
        self.labelRepRechVehic = QLabel()
        self.infoLocation.layout.addWidget(self.labelRepRechVehic, 5, 0)
        self.labelRepRechVehic.setMaximumWidth(500)

                # Recherche à partir d'un client
            # Entrée de paramètres
        self.labelClient = QLabel("Recherche à partir d'un client")
        self.infoLocation.layout.addWidget(self.labelClient, 6, 0)
        # Nom
        self.labelNom = QLabel("Nom du client ?")
        self.infoLocation.layout.addWidget(self.labelNom, 7, 0)
        self.labelNom.setMaximumWidth(100)
        self.rechNom = QLineEdit()
        self.infoLocation.layout.addWidget(self.rechNom, 7, 1)
        self.rechNom.setMaximumWidth(150)
        # Prenom
        self.labelPrenom = QLabel("Prenom du client ?")
        self.infoLocation.layout.addWidget(self.labelPrenom, 8, 0)
        self.labelPrenom.setMaximumWidth(120)
        self.rechPrenom = QLineEdit()
        self.infoLocation.layout.addWidget(self.rechPrenom, 8, 1)
        self.rechPrenom.setMaximumWidth(150)
            # Bouton lancement de recherche
        self.boutonRechClient = QPushButton("Rechercher")
        self.boutonRechClient.clicked.connect(lambda: self.validRechClient(self.rechNom.text(),
                                                                           self.rechPrenom.text()))
        self.infoLocation.layout.addWidget(self.boutonRechClient, 9, 0)
        self.boutonRechClient.setMaximumWidth(150)
            # Bouton réinitialisation
        self.boutonNewRech = QPushButton("Nouvelle recherche")
        self.boutonNewRech.clicked.connect(lambda: self.reinitClient())
        self.infoLocation.layout.addWidget(self.boutonNewRech, 9, 1)
        self.boutonNewRech.setMaximumWidth(150)
            # Label de résultat
        self.labelRepRechClient = QLabel()
        self.infoLocation.layout.addWidget(self.labelRepRechClient, 10, 0)
        self.labelRepRechClient.setMaximumWidth(500)
            # Mise en forme et style de la fenêtre Information location
        self.boutonRechVehic.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonNouvRech.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonRechClient.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.boutonNewRech.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelVehic.setStyleSheet("QLabel {font-weight: bold}")
        self.labelClient.setStyleSheet("QLabel {font-weight: bold}")
        
                    # Onglet Paramètres
        self.parametres.layout = QVBoxLayout()
        self.parametres.setLayout(self.parametres.layout)
            # Modification du mot de passe
        self.labelModif = QLabel("Modifier mon mot de passe")
        self.parametres.layout.addWidget(self.labelModif, alignment=Qt.AlignCenter)
            # Rappelle de l'identifiant de l'utilisateur
        self.labelIdentifiant = QLabel("Veuillez renseigner votre identifiant :")
        self.parametres.layout.addWidget(self.labelIdentifiant, alignment=Qt.AlignCenter)
        self.identifiant = QLineEdit()
        self.parametres.layout.addWidget(self.identifiant, alignment=Qt.AlignCenter)
        self.identifiant.setMaximumWidth(200)
            # Rappelle de l'ancien mdp
        self.labelAncienMdp = QLabel("Veuillez renseigner votre ancien mot de passe :")
        self.parametres.layout.addWidget(self.labelAncienMdp, alignment=Qt.AlignCenter)
        self.ancienMdp = QLineEdit()
        self.ancienMdp.setEchoMode(QLineEdit.Password)
        self.parametres.layout.addWidget(self.ancienMdp, alignment=Qt.AlignCenter)
        self.ancienMdp.setMaximumWidth(200)
            # Définition du nouveau mdp
        self.labelNouveauMdp = QLabel("Veuillez définir votre nouveau mot de passe :")
        self.parametres.layout.addWidget(self.labelNouveauMdp, alignment=Qt.AlignCenter)
        self.nouveauMdp = QLineEdit()
        self.nouveauMdp.setEchoMode(QLineEdit.Password)
        self.parametres.layout.addWidget(self.nouveauMdp, alignment=Qt.AlignCenter)
        self.nouveauMdp.setMaximumWidth(200)
            # Bouton de validation de la modification de mdp
        self.boutonModif = QPushButton("Valider")
        self.boutonModif.clicked.connect(lambda: self.validModif(self.identifiant.text(),
                                                                 self.mdpSecurise(self.ancienMdp.text()),
                                                                 self.mdpSecurise(self.nouveauMdp.text())))
        self.parametres.layout.addWidget(self.boutonModif, alignment=Qt.AlignCenter)
            # Confirmation de la modification
        self.labelConfirm = QLabel()
        self.parametres.layout.addWidget(self.labelConfirm, alignment=Qt.AlignCenter)
            # Mise en forme et style de la fenêtre Paramètres
        self.boutonModif.setStyleSheet(
            "QPushButton {background-color: #8cbf8c ; border-color : #c1f0c1}"
            "QPushButton:Hover {background-color: #548d54 ; border-color : #8cbf8c}")
        self.labelModif.setStyleSheet("QLabel {font-weight: bold}")
            

                    # Ajouter les onglets à la page 
        self.layout.addWidget(self.onglet) 
        self.setLayout(self.layout)

    # Eviter que le mot de passe soit en clair dans la BDD
    def mdpSecurise(self, password) :
        hashMdp = hashlib.sha512()
        hashMdp.update(password.encode("utf-8"))
        return hashMdp.hexdigest()

    # Fonction qui vérifie que l'utilisateur est le bon puis change son mot de passe
    def validModif(self, username, password, newPassword) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"SELECT nomUtilisateur, motDePasse FROM employe WHERE nomUtilisateur='{username}' AND motDePasse='{password}' ;"
            cursor.execute(requete)
            resultat = cursor.fetchall()
            if [(username,password)] == resultat :
                requete = f"UPDATE employe SET motDePasse='{newPassword}' WHERE nomUtilisateur='{username}' AND motDePasse='{password}' ;"
                cursor.execute(requete)
                self.labelConfirm.setText("Modification du mot de passe réussie !")
                self.identifiant.clear()
                self.ancienMdp.clear()
                self.nouveauMdp.clear()
            else :
                self.labelConfirm.setText("Identifiant ou ancien mot de passe incorrect !")

    def validRechVehic(self, marque, modele, types) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"SELECT nomClient, prenomClient, dateDebut, dateFin FROM client AS C \
                        JOIN location AS L ON L.idClient=C.id \
                        JOIN vehicule AS V ON L.idVehicule=V.id \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        WHERE libelleMarque='{marque}' AND libelleModele='{modele}' \
                        AND libelleType='{types}' ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelRepRechVehic.setText(str(resultat))
            if resultat == "" :
                self.labelRepRechVehic.setText("Aucun résultat")

    def validRechClient(self, nom, prenom) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"SELECT libelleMarque, libelleModele, libelleType, dateDebut, dateFin FROM location AS L \
                        JOIN client AS C ON L.idClient=C.id \
                        JOIN vehicule AS V ON L.idVehicule=V.id \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        WHERE nomClient='{nom}' AND prenomClient='{prenom}' ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelRepRechClient.setText(str(resultat))
            if resultat == "" :
                self.labelRepRechClient.setText("Aucun résultat")

    def validRechDispo(self, critere) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = ""
            if critere == "oui" :
                requete = f"SELECT libelleMarque, libelleModele, libelleType \
                        FROM location AS L \
                        JOIN vehicule AS V ON L.idVehicule=V.id \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        JOIN client AS C ON L.idClient=C.id \
                        WHERE V.disponibilite=1 ;"
            else :
                requete = f"SELECT nomClient, prenomClient, libelleMarque, libelleModele, libelleType, dateDebut, dateFin \
                        FROM location AS L \
                        JOIN vehicule AS V ON L.idVehicule=V.id \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        JOIN client AS C ON L.idClient=C.id \
                        WHERE V.disponibilite!=1 ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelRepRechDispo.setText(str(resultat))
            if resultat == "" :
                self.labelRepRechDispo.setText("Aucun résultat")

    def validEnvRepar(self, numVehicule) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"UPDATE vehicule SET disponibilite=2 WHERE id={numVehicule} ;"
            cursor.execute(requete)
            self.labelInfoEnvoie.setText("Le véhicule suivant a été envoyé en réparation et/ou maintenance")
            requete = f"SELECT libelleMarque, libelleModele, libelleType FROM location AS L \
                        JOIN vehicule AS V ON L.idVehicule=V.id \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        WHERE V.id={numVehicule} ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelInfoEnvoieRep.setText(str(resultat))
            if resultat == "" :
                self.labelInfoEnvoieRep.setText("Aucun résultat")
        
    def validRecupRepar(self, numVehicule) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"UPDATE vehicule SET disponibilite=1 WHERE id={numVehicule} ;"
            cursor.execute(requete)
            self.labelInfoEnvoie.setText("Le véhicule suivant a été récupéré")
            requete = f"SELECT libelleMarque, libelleModele, libelleType FROM location AS L \
                        JOIN vehicule AS V ON L.idVehicule=V.id \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        WHERE V.id={numVehicule} ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelInfoEnvoieRep.setText(str(resultat))
            if resultat == "" :
                self.labelInfoEnvoieRep.setText("Aucun résultat")

    def affichDispo(self) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            self.labelVehicDispo.setText("Les véhicules disponibles à ce jour :")
            requete = f"SELECT V.id, libelleMarque, libelleModele, libelleType FROM vehicule AS V \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id \
                        WHERE disponibilite=1 \
                        ORDER BY V.id ASC ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelAffichDispo.setText(str(resultat))
            if resultat == "" :
                self.labelAffichDispo.setText("Aucun résultat")

    def confirmRes(self, numVehic, numClient, dateDebut, dateFin) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if numVehic == '' :
            vehic = 0
        else :
            vehic = int(numVehic)
        if numClient == '' :
            client = 0
        else :
            client = int(numClient)
        if connection.is_connected() :
            requete = f"SET FOREIGN_KEY_CHECKS = 0; \
                        INSERT INTO location(idVehicule, idClient, dateDebut, dateFin) \
                        VALUES ({vehic}, {client}, '{dateDebut}', '{dateFin}') ; \
                        UPDATE vehicule SET disponibilite=0 WHERE vehicule.id={numVehic} ;"
            cursor.execute(requete)
            self.labelConfirmRes.setText("Réservation réussie !")

    def checkClient(self) :
        self.labelCheck.setText("Section clientèle")
        self.labelOptDispo.setText(" Les options possibles : \n nomClient, prenomClient, mailClient \n Renseigner les options séparées par des virgules.")
        self.rechercher.layout.addWidget(self.textRecherche, 4, 1)
        self.rechercher.layout.addWidget(self.boutonSoumettreClient, 5, 1)
        self.rechercher.layout.addWidget(self.boutonEffacer, 6, 1)
        self.boutonSoumettreClient.setHidden(False)
        self.boutonSoumettreVehic.setHidden(False)
        self.boutonSoumettreLocat.setHidden(False)
        self.boutonEffacer.setHidden(False)
        self.textRecherche.setHidden(False)

    def checkLocat(self) :
        self.labelCheck.setText("Section location")
        self.labelOptDispo.setText(" Les options possibles : \n idVehicule, idClient, dateDebut, dateFin \n Renseigner les options séparées par des virgules.")
        self.rechercher.layout.addWidget(self.textRecherche, 4, 1)
        self.rechercher.layout.addWidget(self.boutonSoumettreLocat, 5, 1)
        self.rechercher.layout.addWidget(self.boutonEffacer, 6, 1)
        self.boutonSoumettreClient.setHidden(False)
        self.boutonSoumettreVehic.setHidden(False)
        self.boutonSoumettreLocat.setHidden(False)
        self.boutonEffacer.setHidden(False)
        self.textRecherche.setHidden(False)
        
    def checkVehic(self) :
        self.labelCheck.setText("Section véhicule")
        self.labelOptDispo.setText(" Les options possibles : \n libelleMarque, lieblleModele, libelleType, tarifJour, disponibilite \n Renseigner les options séparées par des virgules.")
        self.rechercher.layout.addWidget(self.textRecherche, 4, 1)
        self.rechercher.layout.addWidget(self.boutonSoumettreVehic, 5, 1)
        self.rechercher.layout.addWidget(self.boutonEffacer, 6, 1)
        self.boutonSoumettreClient.setHidden(False)
        self.boutonSoumettreVehic.setHidden(False)
        self.boutonSoumettreLocat.setHidden(False)
        self.boutonEffacer.setHidden(False)
        self.textRecherche.setHidden(False)

    def algoRechercheClient(self, option) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"SELECT id, {option} FROM client ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelResRech.setText(str(resultat))

    def algoRechercheVehic(self, option) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"SELECT V.id, {option} FROM vehicule AS V \
                        JOIN modele AS Md ON V.idModele=Md.id \
                        JOIN marque AS M ON Md.idMarque=M.id \
                        JOIN type AS T ON Md.idType=T.id ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelResRech.setText(str(resultat))

    def algoRechercheLocat(self, option) :
        #Ici la redéfinition de connection et cursor est nécessaire
        connection = mysql.connector.connect(host='localhost',user='root',password='',database='bddmova')
        cursor = connection.cursor()
        if connection.is_connected() :
            requete = f"SELECT id, {option} FROM location ;"
            cursor.execute(requete)
            rows = cursor.fetchall()
            resultat = ""
            for row in rows :
                resultat += str(row) + '\n'
            self.labelResRech.setText(str(resultat))

    # Effacer le contenu de la page Information location
    def reinitVehic(self) :
        self.rechModele.clear()
        self.rechMarque.clear()
        self.rechType.clear()
        self.labelRepRechVehic.clear()
        
    def reinitClient(self) : 
        self.rechNom.clear()
        self.rechPrenom.clear()
        self.labelRepRechClient.clear()

    def reinitDispo(self) : 
        self.rechDispo.clear()
        self.labelRepRechDispo.clear()

    def reinitRepar(self) :
        self.labelInfoEnvoieRep.clear()
        self.labelInfoEnvoie.clear()
        self.numVehic.clear()

    def reinitRecherche(self) :
        self.labelResRech.clear()
        self.textRecherche.clear()
        self.labelOptDispo.clear()
        self.labelCheck.clear()
        self.boutonSoumettreClient.setHidden(True)
        self.boutonSoumettreVehic.setHidden(True)
        self.boutonSoumettreLocat.setHidden(True)
        self.boutonEffacer.setHidden(True)
        self.textRecherche.setHidden(True)

    def reinitReser(self) :
            self.selecVehicRes.clear()
            self.selecClientRes.clear()
            self.selecDateDeb.clear()
            self.selecDateFin.clear()
            self.labelConfirmRes.clear()
            self.labelVehicDispo.clear()
            self.labelAffichDispo.clear()