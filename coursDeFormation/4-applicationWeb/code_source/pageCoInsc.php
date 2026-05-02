<!DOCTYPE html>
<html lang="fr">

<head>
  <title> Connexion </title>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="styles.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link hrel="helping.js" rel="stylesheet">
</head>

<body class="container">
  <?php require "header.php" ?>
  <div class="row">
    <h3 class="col-12 justify-content-center"> Connexion / Inscription </h3>
  </div>

  <!-- 

  if( isset($_COOKIE['sessionUtil']) && is_string($_COOKIE['sessionUtil']) ) {      // Connexion de l'utilisateur
    $delimiter = "//";
    $split = explode($delimiter, $_COOKIE['sessionUtil']);
    $email = isset($split[0]) ? $split[0] : "";
    $password = isset($split[1]) ? decryptPassword($split[1]) : "";
    // ... Tenter de connecter l'utilisateur
    if( /* l'utilisateur est connecté */ ) {
        // Suite de votre script
    }
    else {
        // Suppression du cookie
        setcookie( 'sessionUtil', null, time() - 3600 );
    }
  }

  if (isset($_POST['remember'])) {                          // Cookie de connexion
    $delimiter = "//";
    $cookieString = $_POST['mailClient'] . $delimiter . encryptPassword($_POST['mdp']);
    $cookieDuration = 60 * 60 * 24; 
    setcookie('sessionClient', $cookieString, time() + $cookieDuration);
  } else {

  -->


  <div class="row">
    <article class="col-6" id="connexion">
      <form class="row" action="login.php" method="post">
        <fieldset>
          <legend> Connexion </legend>
          <table>
            <tr>
              <td class="row mx-auto">
                <p class="col-12"> Vous avez déjà un compte ? Connectez-vous !</p>
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Mail * </label>
                <input class="col-7" type="email" name="mailClient" placeholder="email@example.com" size="50" required>
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Mot de passe * </label>
                <input class="col-7" type="password" name="mdp" required>
              </td>
            </tr>
            <tr>
              <td class="row">
                <input class="col-4 offset-4" type="submit" value="Se connecter">
              </td>
            </tr>
          </table>
        </fieldset>
      </form>
    </article>

    <article class="col-6" id="inscription">
      <form class="row" action="inscription.php" method="post">
        <fieldset>
          <legend> Inscription </legend>
          <table>
            <tr>
              <td class="row mx-auto">
                <p class="col-12"> Les champs marqués d'un * sont obligatoires. </p>
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Nom </label>
                <input class="col-7" type="text" name="nomClient">
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Prénom </label>
                <input class="col-7" type="text" name="prenomClient">
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Mail * </label>
                <input class="col-7" type="email" name="mailClient" placeholder="email@example.com" size="50" required>
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Mot de passe * </label>
                <input class="col-7" type="password" name="mdp" required>
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-5"> Confirmation * </label>
                <input class="col-7" type="password" name="mdpConf" required>
              </td>
            </tr>
            <tr>
              <td class="row">
                <label class="col-4 offset-3"> J'accepte les <a id="cguLink" onclick="window.open('cgu.html','wclose','width=1000, height=500, toolbar=si, scroolbar=si, status=si'); return false;">CGU</a> * </label>
                <input class="col-1" type="checkbox" name="cgu" required>
              </td>
            </tr> <br>
            <tr>
              <td class="row">
                <input class="col-3 offset-2" type="submit" value="S'inscrire">
                <input class="col-3 offset-2" type="reset" value="Annuler">
              </td>
            </tr>
          </table>
        </fieldset>
      </form>
    </article>
  </div>

  <?php require "footer.php" ?>

</body>