<?php
require "phpFunction.php";
$bdd = getBDD();

$req = $bdd->prepare("SELECT id FROM client WHERE mailClient=?");
$req->execute([$_COOKIE['sessionClient']]);
$resultat = $req->fetch();
$id = $resultat['id'];


if (isset($_POST['nomClient']) && !empty($_POST['nomClient'])) {
  $req = $bdd->prepare("UPDATE client SET nomClient=? WHERE id=?");
  $req->execute([$_POST['nomClient'], $id]);
}

if (isset($_POST['prenomClient']) && !empty($_POST['prenomClient'])) {
  $req = $bdd->prepare("UPDATE client SET prenomClient=? WHERE id=?");
  $req->execute([$_POST['prenomClient'], $id]);
}

if (isset($_POST['mailClient']) && !empty($_POST['mailClient'])) {
  $req = $bdd->prepare("UPDATE client SET mailClient=? WHERE id=?");
  $req->execute([$_POST['mailClient'], $id]);

  $req = $bdd->prepare("SELECT mailClient FROM client WHERE id=?");
  $req->execute([$id]);
  $resultat = $req->fetch();
  setcookie("sessionClient", $resultat['mailClient'], time() + 3600);
}

if (verifMdp($_POST['mdp'], $_POST['mdpConf']) == 1) {
  $nouvMdp = md5($_POST['mdp']);
  $req = $bdd->prepare("UPDATE client SET mdp=? WHERE id=?");
  $req->execute([$nouvMdp, $id]);
}

$req->closeCursor();
header('Location: account.php');
