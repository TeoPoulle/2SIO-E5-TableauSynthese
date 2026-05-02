<footer class="row">
  <div class="col-2">
    <nav class="navbar navbar-expand-sm" id="logo">
      <div class="collapse navbar-collapse">
        <a class="nav-item nav-link" href="index.php">
          <img id="logo" src="images/LogoMOVA.png">
        </a>
      </div>
    </nav>
  </div>

  <div class="col-3 offset-1">
    <h5 class="row"> COORDONNEES </h5>
    <p class="row"> contact@mova.com </p>
    <p class="row"> 05 00 00 00 00 </p>
    <p class="row"> 123 Rue des Innovateurs, <br> 76300 Sotteville lès Rouen </p>
  </div>

  <div class="col-3">
    <h5 class="row"> RESEAUX </h5>
    <div class="row">
      <img src="images/facebook.png" class="col-6" id="reseau">
      <img src="images/instagram.png" class="col-6" id="reseau">
    </div>
    <div class="row">
      <img src="images/twitter.png" class="col-6" id="reseau">
      <img src="images/linkedin.png" class="col-6" id="reseau">
    </div>
  </div>

  <div class="col-2 offset-1" id="nav">
    <h5 class="row"> NAVIGATION </h5>
    <p class="row"> <a class="col-auto" href="index.php"> Accueil </a> </p>
    <?php if (isset($_COOKIE['sessionClient']) && !empty($_COOKIE['sessionClient'])) { ?>
      <p class="row"> <a class="col-auto" href="account.php"> Mon compte </a> </p>
      <p class="row"> <a class="col-auto" href="reservation.php"> Réservation </a> </p>
    <?php } ?>
    <p class="row"> <a class="col-auto" href="contact.php"> Contact </a> </p>
    <p class="row"> <a class="col-auto" href="logout.php"> Déconnexion </a> </p>
  </div>
</footer>