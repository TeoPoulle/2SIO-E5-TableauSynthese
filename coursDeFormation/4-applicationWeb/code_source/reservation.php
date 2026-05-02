<?php
require "header.php";
$esp = "  ";

$req = $pdo->prepare("SELECT nomClient FROM client WHERE mailClient=?");
$req->execute([$_COOKIE['sessionClient']]);
$resultat = $req->fetch();
$nomClient = $resultat['nomClient'];

if (isset($_COOKIE['sessionClient'])) { ?>
  <body class="container">
    <h2 class="row justify-content-center">Vos réservations</h2>
    <div class="col-8 offset-2">
      <br>
      <table class="row">

        <tr class="row justify-content-center" id="thead">
          <th class="col-4" colspan="3"> Numéros important </th>
          <th class="col-4" colspan="3">Caractéristique véhicule </th>
          <th class="col-4" colspan="3"> Dates importantes </th>
        </tr>
        <tr class="row justify-content-center">
          <td class="col-1">Location</td>
          <td class="col-1">Véhicule</td>
          <td class="col-1">Client</td>
          <td class="col-1">Marque</td>
          <td class="col-1">Modèle</td>
          <td class="col-1">Type</td>
          <td class="col-2">Début</td>
          <td class="col-2">Fin</td>
        </tr>
        <?php
        $req = $pdo->prepare("SELECT C.mailClient, L.id, L.idVehicule, L.idClient, L.dateDebut, L.dateFin, Mo.libelleModele, T.libelleType, Ma.libelleMarque, V.tarifJour FROM client AS C 
                                JOIN location AS L ON C.id = L.idClient
                                JOIN vehicule AS V ON V.id = L.idVehicule
                                JOIN modele AS Mo ON Mo.id = V.idModele
                                JOIN marque AS Ma ON Ma.id = Mo.idMarque
                                JOIN type AS T ON T.id = Mo.idType
                                WHERE C.mailClient = ?");
        $req->execute([$_COOKIE['sessionClient']]);
        $resultat = $req->fetchAll();
        if (!empty($resultat)) {
          foreach ($resultat as $ligne) {
            $location = $ligne['id'];
            $vehicule = $ligne['idVehicule'];
            $client = $ligne['idClient'];
            $marque = $ligne['libelleMarque'];
            $modele = $ligne['libelleModele'];
            $type = $ligne['libelleType'];
            $debut = $ligne['dateDebut'];
            $fin = $ligne['dateFin']; ?>
            <tr class="row justify-content-center">
              <td class="col-1"> <?php echo $location ?> </td>
              <td class="col-1"> <?php echo $vehicule ?> </td>
              <td class="col-1"> <?php echo $client ?> </td>
              <td class="col-1"> <?php echo $marque ?> </td>
              <td class="col-1"> <?php echo $modele ?> </td>
              <td class="col-1"> <?php echo $type ?> </td>
              <td class="col-2"> <?php echo $debut ?> </td>
              <td class="col-2"> <?php echo $fin ?> </td>
            </tr>
          <?php }
        } else { ?>
          <tr class="row justify-content-center">
            <td class="col-12" colspan="9"> Vous n'avez pas de réservations pour le moment ! </td>
          </tr>
        <?php } ?>
      </table>
    </div>

    <br> <br>
    <h2 class="row justify-content-center">Nouvelle demande</h2>

    <form class="row" method="post" action="location.php">
      <table class="col-8 mx-auto">
        <tr class="row">
          <td class="col-4 offset-2"> A quel nom sera la réservation ? </td>
          <td class="col-6"> <input type="text" name="nomClient" value=<?php echo $nomClient ?> size="35" require> </td>
        </tr>
        <tr class="row">
          <td class="col-4 offset-2"> Mail de réservation </td>
          <td class="col-6"> <input type="email" name="mailClient" value=<?php echo $_COOKIE['sessionClient'] ?> size="35" require> </td>
        </tr>
        <tr class="row">
          <td class="col-4 offset-2"> Véhicule souhaité </td>
          <td class="col-6">
            <select name="carac" require>
              <?php $req = $pdo->prepare("SELECT V.id, Ma.libelleMarque, Mo.libelleModele, T.libelleType, V.tarifJour FROM vehicule AS V
                                        JOIN modele AS Mo ON Mo.id=V.idModele
                                        JOIN marque AS Ma ON Ma.id=Mo.idMarque
                                        JOIN type AS T ON T.id=Mo.idType
                                        WHERE V.disponibilite=1");
              $req->execute();
              $resultat = $req->fetchAll();
              if (!empty($resultat)) {
                foreach ($resultat as $ligne) {
                  $id = $ligne['id'];
                  $mar = $ligne['libelleMarque'];
                  $mod = $ligne['libelleModele'];
                  $type = $ligne['libelleType'];
                  $tarif = $ligne['tarifJour'] . "€/jour"; ?>
                  <option> <?php echo $id . $esp . $mar . $esp . $mod . $esp . $type . $esp . $tarif ?> </option>
              <?php }
              }
              ?>
            </select>
          </td>
        </tr>
        <tr class="row">
          <td class="col-4 offset-2"> Date de début </td>
          <td class="col-6"> <input type="date" name="debut"> </td>
        </tr>
        <tr class="row">
          <td class="col-4 offset-2"> Date de fin </td>
          <td class="col-6"> <input type="date" name="fin"> </td>
        </tr>
        <tr class="row">
          <td class="col-1 offset-3"> <input type="submit" value="Valider"> </td>
          <td class="col-1 offset-4"> <input type="reset" value="Annuler"> </td>
        </tr>
      </table>
    </form>
  </body>
<?php
} else {
  header("Location: pageCoInsc.php");
}
$req->closeCursor();
require "footer.php";
?>