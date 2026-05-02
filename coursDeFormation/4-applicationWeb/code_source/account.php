<?php require "header.php";
// require "phpFunction.php" ;
$bdd = getBDD();

$req = $bdd->prepare("SELECT nomClient, prenomClient FROM client WHERE mailClient=?");
$req->execute([$_COOKIE['sessionClient']]);
$resultat = $req->fetch();
$nomClient = $resultat['nomClient'];
$prenomClient = $resultat['prenomClient'];

if (isset($_COOKIE['sessionClient'])) { ?>

<body class="container">

  <h2 class="row justify-content-center"> Mes informations </h2>
  <div class="row justify-content-center">
    <form class="col-8 offset-1" method="post" action="modifInfo.php">
      <table class="row">
        <tr>
          <td> <!-- Je n'ai pas trouvé d'autres moyens pour séparer les parties (test avec le css non concluant) -->
            <br>
          </td>
        </tr>
        <tr id="test"> <!-- Modifier les informations simples comme le nom, prénom et le mail -->
          <td class="row">
            <h3 class="col-12">Modifier mes informations</h3>
          </td>
        </tr>
        <tr>
          <td class="row">
            <label class="col-4 offset-1">Mon Nom (ou Pseudo)</label>
            <label class="col-3 offset-3">Mon Prénom</label>
          </td>
        </tr>
        <tr>
          <td class="row">
            <input class="col-4 offset-1" type="text" name="nomClient" placeholder=<?php echo $nomClient ?>>
            <input class="col-4 offset-2" type="text" name="prenomClient" placeholder=<?php echo $prenomClient ?>>
          </td>
        </tr>
        <tr>
          <td>
            <br>
          </td>
        </tr>
        <tr>
          <td class="row">
            <label class="col-auto mx-auto">Mon Mail</label>
          </td>
        </tr>
        <tr>
          <td class="row">
            <input class="col-auto mx-auto" type="email" name="mailClient" placeholder=<?php echo $_COOKIE['sessionClient'] ?>>
          </td>
        </tr>
        <tr>
          <td>
            <br> <br> <br>
          </td>
        </tr>
        <tr id="test"> <!-- Modifier le mot de passe de l'utilisateur -->
          <td class="row">
            <h3 class="col-12">Modifier mon mot de passe</h3>
          </td>
        </tr>
        <tr>
          <td class="row">
            <label class="col-3"> Nouveau mot de passe </label>
            <input class="col-3" type="password" name="mdp">
            <label class="col-2 offset-1"> Confirmation</label>
            <input class="col-3" type="password" name="mdpConf">
          </td>
        </tr>
        <tr>
          <td>
            <br> <br>
          </td>
        </tr>
        <tr>
          <td class="row">
            <input class="col-2 offset-3" type="submit" value="Valider">
            <input class="col-2 offset-2" type="reset" value="Annuler">
          </td>
        </tr>
      </table>
    </form>
  </div>
</body>

<?php 
} else {
  header("Location: pageCoInsc.php") ;
}
$req->closeCursor();
require "footer.php" ?>