<?php
session_start();
setcookie("sessionClient", $resultat['mailClient'], time() - 3600);
session_destroy();
header('Location: index.php');
exit;
