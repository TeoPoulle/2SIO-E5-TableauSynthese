<?php

// Fonction pour se connecter à la base de données
function getBDD() {
  try {
    $bdd = new PDO("mysql:host=localhost;dbname=3-logicielInterne;charset=utf8", "teo", "16122004");
    $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $bdd;
  } catch (Exception $e) {
    $msg = "ERREUR PDO dans " . $e->getFile() . "L." . $e->getLine() . " : " . $e->getMessage();
    die($msg);
  }
}

// Vérifier que les mots de passe sont identiques
function verifMdp($mdp, $aComparer) {
  if ($mdp != $aComparer) { ?>
    <p> Erreur de connexion. Mauvais identifiant / mot de passe. </p>
  <?php return False ;
  } else {
    return True ;
  }
}




?>