<?php require "header.php"; ?>

<body class="container">
    <h1 class="row justify-content-center"> Pour nous contacter </h1>

    <div class="row">
        <h2 class="col-12"> Formulaire de contact </h2>
    </div>

    <div class="row justify-content-center">
        <form method="post" action="mailto:" class="col-7 offset-1"> <!-- contact@mova.com -->
            <fieldset class="row">
                <legend class="col-auto"> Nous vous répondrons dans les meilleurs délais ! </legend>
                <table>
                    <tr class="row">
                        <td class="col-3"> Votre adresse mail * </td>
                        <td class="col-9"> <input type="email" name="adressemail" maxlength="50" size="72" require> </td>
                    </tr>
                    <tr class="row">
                        <td class="col-3"> Votre demande * </td>
                        <td class="col-9">
                            <select name="sujetdemande" require>
                                <option value="defaut"> --Défaut--</option>
                                <option value="location"> Locations </option>
                                <option value="reservation"> Réservation en cours </option>
                                <option value="info"> Informations complémentaires </option>
                                <option value="autre"> Autres </option>
                            </select>
                        </td>
                    </tr>
                    <tr class="row">
                        <td class="col-3"> A vous * </td>
                        <td class="col-9"> <textarea cols="75" rows="7" require> </textarea> </td>
                    </tr>
                    <tr class="row">
                        <td class="col-2 offset-4"> <input type="reset" value="Annuler"> </td>
                        <td class="col-2 offset-2"> <input type="submit" value="Envoyer"> </td>
                    </tr>
                </table>
            </fieldset>
        </form>
    </div>
</body>

<?php require "footer.php" ?>