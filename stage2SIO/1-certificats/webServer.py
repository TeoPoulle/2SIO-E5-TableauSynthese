from flask import Flask, Response
import subprocess
import os
import logging

app = Flask(__name__)
# Chemin du répertoire contenant les scripts
scriptDir = os.path.dirname(os.path.abspath(__file__))

# Création d'un fichier de log pour les erreurs dans le même dossier que le script
scriptDir = os.path.dirname(os.path.abspath(__file__))
logFile = os.path.join(scriptDir, 'docImportant/expiringCertificate.log')

logging.basicConfig(
    filename=logFile,             # Chemin du fichier de log en cas d'erreur
    level=logging.INFO,           # Pour plus de détails
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

@app.route('/')
def display_table():
    """Exécute le fichier dataFormatage.php et retourne son contenu HTML"""
    try:
        # Exécuter PHP et capturer la sortie
        result = subprocess.run(
            ['php', os.path.join(scriptDir, 'dataFormatage.php')],
            cwd=scriptDir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return Response(result.stdout, mimetype='text/html')
        else:
            logging.error(f"{os.path.basename(__file__)} : Erreur lors de l'exécution de PHP: {result.stderr}")
            return f"<h1>Erreur lors de l'exécution de PHP</h1><pre>{result.stderr}</pre>", 500
            
    except subprocess.TimeoutExpired:
        logging.error(f"{os.path.basename(__file__)} : Timeout : l'exécution de PHP a pris trop de temps")
        return "<h1>Erreur : Timeout</h1><p>L'exécution de PHP a pris trop de temps.</p>", 500
    except FileNotFoundError:
        logging.error(f"{os.path.basename(__file__)} : PHP non trouvé : PHP n'est pas installé ou n'est pas dans le PATH.")
        return "<h1>Erreur : PHP non trouvé</h1><p>PHP n'est pas installé ou n'est pas dans le PATH.</p>", 500
    except Exception as e:
        logging.error(f"{os.path.basename(__file__)} : Exception : {str(e)}")
        return f"<h1>Erreur</h1><pre>{str(e)}</pre>", 500

app.run(host='', port=5000, debug=False, ssl_context=('./docImportant/certificat.pem', './docImportant/clePrivee.pem'))
logging.info(f"{os.path.basename(__file__)} : Serveur démarré sur ")