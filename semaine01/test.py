# Cliquez sur le bouton Play en haut à droite pour exécuter ceci.

import sys

version = sys.version_info
msg: str = f"Welcome to Python {version.major}.{version.minor}.{version.micro}!"
print(msg)

# Ceci devrait être souligné en rouge car il y a une erreur de type,
# sans toutefois empêcher l'exécution du code. Rajoutez des guillemets
# autour de 3 pour corriger l'erreur. Normalement, le formatage automatique
# du code lors de la sauvegarde du fichier devrait ensuite automatiquement
# insérer des espaces autour du symbole =.
msg=3
