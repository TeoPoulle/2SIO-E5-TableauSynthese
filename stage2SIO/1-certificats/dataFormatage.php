<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Applications Expirantes et/ou Expirées</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #ffffff;
        }

        h1 {
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

        .expire {
            background-color: #ffcccc;
            font-weight: bold;
            color: #c00;
            border-top: 1px solid #a9a9a9;
        }

        .urgent {
            background-color: #ffe6cc;
            font-weight: bold;
            color: #ff6600;
            border-top: 1px solid #a9a9a9;
        }

        .alert {
            background-color: #ffffcc;
            font-weight: bold;
            color: #ff9900;
            border-top: 1px solid #a9a9a9;
        }

        .ok {
            background-color: #ccffcc;
            font-weight: bold;
            color: #009900;
            border-top: 1px solid #a9a9a9;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #000;
            font-size: 12px;
        }
    </style>
</head>

<body>
    <h1>📊 Applications Expirantes et/ou Expirées</h1>
    <table>
        <tr>
            <th>Application</th>
            <th>Type</th>
            <th>Date Fin</th>
            <th>Status</th>
        </tr>

        <?php
        $jsonData = file_get_contents('./docImportant/ExpiringApps.json');
        $apps = json_decode($jsonData, true);
        foreach ($apps as $app) {
            $statusClass = '';
            switch ($app['Status']) {
                case 'Expiré':
                    $statusClass = 'expire';
                    break;
                case "Expire bientôt (moins d'un mois)":
                    $statusClass = 'urgent';
                    break;
                case 'Expire dans moins de 6 mois':
                    $statusClass = 'alert';
                    break;
                case 'Valide':
                    $statusClass = 'ok';
                    break;
            } ?>
            <tr>
                <td><?php echo $app['Application']; ?></td>
                <td><?php echo $app['Type']; ?></td>
                <td><?php echo $app['EndDate']; ?></td>
                <td class="<?php echo $statusClass; ?>"><?php echo $app['Status']; ?></td>
            </tr>
        <?php } ?>
    </table>
    <div class="footer">
        <p>Total: <?php echo count($apps); ?> application(s) | Généré le: <?php echo date('Y-m-d H:i:s'); ?></p>
    </div>
</body>
</html>