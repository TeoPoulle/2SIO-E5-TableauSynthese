<!DOCTYPE html>
<html lang="fr">

<head>
  <title> MOVA </title>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="styles.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<?php require "login.php"; ?>

<header class="row">
  <div class="col-1 offset-1">
    <nav class="navbar navbar-expand-sm" id="logo">
      <div class="collapse navbar-collapse">
        <a class="nav-item nav-link" href="index.php">
          <img id="logo" src="images/LogoMOVA.png">
        </a>
      </div>
    </nav>
  </div>

  <h1 class="col-5 offset-1"> MOVA </h1>

  <div class="col-auto" id="navH">
    <nav class="navbar navbar-expand-sm">
      <div class="collapse navbar-collapse">
        <?php if (isset($_COOKIE['sessionClient']) && !empty($_COOKIE['sessionClient'])) { ?>
          <a class="nav-item nav-link" href="account.php"> <?php echo $_COOKIE['sessionClient']; ?> </a>
          <a class="nav-item nav-link" href="reservation.php"> Réservation </a>
        <?php } else { ?>
          <a class="nav-item nav-link" href="pageCoInsc.php"> Connexion </a>
        <?php } ?>
        <a class="nav-item nav-link" href="logout.php">Déconnexion</a>

      </div>
    </nav>
  </div>
</header>