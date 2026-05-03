<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informations des Boîtes Mail</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #ffffff;
        }

        h1, h2 {
            text-align: center;
            color: #333;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }

        th {
            background-color: #1c6190;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid lightgray;
        }

        tr:hover {
            background-color: #f9f9f9;
        }

        .attention {
            color: red;
            font-weight: bold;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #000;
            font-size: 12px;
        }

        img {
            display: block;
            margin: 20px auto;
            max-width: 60%;
            height: auto;
            align-content: center;
        }
    </style>
</head>

<body>
    <h1>📊 Utilisateurs ayant une boîte mail (bientôt) pleine</h1>
    <table>
        <tr>
            <th>Nom et Prénom</th>
            <th>Adresse Mail</th>
            <th>Pourcentage Utilisé</th>
        </tr>
        <?php
        $jsonData = file_get_contents('./fichierImportant/MailboxInfo.json');
        $mailboxes = json_decode($jsonData, true);
        foreach ($mailboxes as $mailbox) { 
            if ($mailbox['usedPercentage'] >= 90) {
            ?>
                <tr>
                    <td><?php echo $mailbox['userName']; ?></td>
                    <td><?php echo $mailbox['userMail']; ?></td>
                    <td class="attention"><?php echo $mailbox['usedPercentage']; ?></td>
                </tr>
            <?php } 
            }
        if ($mailboxes == []) { ?>
            <tr><td colspan='3' style='text-align:center;'>Aucun utilisateur n'a une boîte mail (bientôt) pleine.</td></tr>
        <?php } ?>
    </table>
    <br><br><br>
    <h2>📈 Graphique de l'Utilisation des Boîtes Mail</h2>
    <img src="fichierImportant/graphDiffere.png" alt="Graphique des boîtes mail">

    <div class="footer">
        <p>Généré le: <?php echo date('Y-m-d H:i:s'); ?></p>
    </div>
</body>
</html>