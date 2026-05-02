<?php
session_start();

// Récupération de la bdd
require "phpFunction.php";
$pdo = getBDD();

// Récupération des données
if (isset($_POST['mailClient']) && isset($_POST['mdp'])) {
    $mailClient = $_POST['mailClient'];
    $mdp = md5($_POST['mdp']);
} else {
    $mailClient = "";
    $mdp = "";
}


// Vérifier si l'utilisateur existe
$req = $pdo->prepare("SELECT mailClient, mdp FROM client WHERE mailClient = ? AND mdp = ?");
$req->execute([$mailClient, $mdp]);
$resultat = $req->fetch();

echo False;

if (!empty($resultat) && verifMdp($mdp, $resultat['mdp']) == 1) {
    setcookie("sessionClient", $resultat['mailClient'], time() + 3600);
    header('Location: index.php');
    exit;
} elseif (!empty($resultat) && verifMdp($mdp, $resultat['mdp']) == 1) {
    setcookie("erreur", "erreur", time() + 360);
    header('Location: pageCoInsc.php');
    exit;
}

$req->closeCursor();
