<?php

require "phpFunction.php";
$bdd = getBDD();

if (isset($_POST['mdp']) && isset($_POST['mdpConf'])) {
  if ($_POST['mdp'] == $_POST['mdpConf']) {
    if (isset($_POST['mailClient'], $_POST['mdp'])) {
      if (empty($_POST['mailClient'])) {
        echo "Le champ e-mail est vide.";
      } elseif ($req = $bdd->query("SELECT * FROM client WHERE mailClient='" . $_POST['mailClient'] . "'") == 1) {
        echo "Cette adresse e-mail est déjà Clientisée.";
      } else {
        if (isset($_POST['nomClient']) && isset($_POST['prenomClient'])) {
          $req = $bdd->prepare("INSERT INTO client(nomClient, prenomClient, mailClient, mdp) VALUES(?, ?, ?, ?) ;");
          $req->execute(array($_POST['nomClient'], $_POST['prenomClient'], $_POST['mailClient'], md5($_POST['mdp'])));
        } elseif (isset($_POST['nomClient'])) {
          $req = $bdd->prepare("INSERT INTO client(nomClient, mailClient, mdp) VALUES(?, ?, ?) ;");
          $req->execute(array($_POST['nomClient'], $_POST['mailClient'], md5($_POST['mdp'])));
        } elseif (isset($_POST['prenomClient'])) {
          $req = $bdd->prepare("INSERT INTO client(prenomClient, mailClient, mdp) VALUES(?, ?, ?) ;");
          $req->execute(array($_POST['prenomClient'], $_POST['mailClient'], md5($_POST['mdp'])));
        } else {
          $req = $bdd->prepare("INSERT INTO client(mailClient, mdp) VALUES(?, ?) ;");
          $req->execute(array($_POST['mailClient'], md5($_POST['mdp'])));
        }
      }
    }
    header('Location: index.php');
    $req->closeCursor();
  } else {
    echo "Les deux champs sont différents !";
    header('Location: pageCoInsc.php');
  }
}
