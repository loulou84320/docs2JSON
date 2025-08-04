# docs2JSON
Un outil Python pour scanner et convertir l'intégralité d'un projet en un fichier JSON structuré, incluant le contenu de tous les fichiers.
docs2JSON est un scanner de projet qui parcourt récursivement tous les fichiers d'un dossier et génère un fichier JSON contenant :

La structure complète du projet
Le contenu de tous les fichiers texte
Les métadonnées (taille, chemin, extension)
La structure des bases de données SQLite
Une gestion intelligente des fichiers binaires

🚀 Installation et Dépendances
Prérequis

Python 3.6+
Modules standard Python (aucune installation externe requise)

Dépendances
# Modules standard inclus avec Python
import os
import json
import sqlite3
from pathlib import Path
Installation
# Cloner ou télécharger le fichier
curl -O https://raw.githubusercontent.com/[votre-repo]/docs2JSON/main/docs2json.py

# Ou créer le fichier directement
touch docs2json.py
# Copier le code dans le fichier
📖 Mode d'emploi
Utilisation basique
python docs2json.py
Le programme vous demandera :

Chemin vers votre projet : /chemin/vers/votre/projet
Nom du fichier de sortie : mon_projet.json (optionnel)

Utilisation programmatique
from docs2json import scan_project

# Scanner un projet
data = scan_project("/chemin/vers/projet", "output.json")

# Accéder aux données
print(f"Projet: {data['project_name']}")
print(f"Nombre de fichiers: {len(data['files'])}")
Exemples d'usage
# Exemple 1: Projet web
python docs2json.py
📁 Chemin vers ton projet: /home/user/mon-site-web
💾 Nom du fichier JSON: site_backup.json

# Exemple 2: Application Python
python docs2json.py
📁 Chemin vers ton projet: ./mon-app-python
💾 Nom du fichier JSON: [Entrée vide = nom par défaut]
🔧 Fonctionnalités
✅ Fichiers supportés

Fichiers texte : .txt, .md, .py, .js, .html, .css, .json, etc.
Code source : Tous les langages de programmation
Bases de données : .db, .sqlite, .sqlite3 (structure + métadonnées)
Configuration : .env, .config, .ini, .yaml, etc.

❌ Fichiers ignorés/traités différemment

Fichiers binaires : .exe, .dll, .so, images, vidéos, archives
Dossiers système : node_modules, .git, __pycache__, .vscode

🎯 Gestion des encodages
Le programme tente plusieurs encodages automatiquement :

UTF-8 (priorité)
Latin-1
CP1252
ISO-8859-1

📊 Structure de sortie JSON
{
  "project_name": "mon-projet",
  "scan_path": "/chemin/vers/projet",
  "files": [
    {
      "name": "app.py",
      "path": "src/app.py",
      "full_path": "/chemin/vers/projet/src/app.py",
      "extension": ".py",
      "size": 1024,
      "content": "# Contenu du fichier..."
    },
    {
      "name": "database.db",
      "path": "data/database.db", 
      "extension": ".db",
      "size": 8192,
      "content": "{\"type\": \"sqlite_database\", \"tables\": [...]}"
    }
  ]
}
🛠️ Options avancées
Personnalisation des filtres
# Modifier les extensions ignorées
ignored_extensions = {'.exe', '.dll', '.pdf'}  # Ajouter/retirer des types

# Modifier les dossiers ignorés  
ignored_dirs = {'node_modules', '.git', 'build'}  # Personnaliser
Traitement des erreurs

Fichiers non lisibles : Message d'erreur dans le contenu
Bases de données corrompues : Erreur capturée et loggée
Permissions insuffisantes : Gestion gracieuse

📝 Cas d'usage

Backup de projet : Sauvegarde complète en un fichier
Documentation automatique : Générer une vue d'ensemble
Migration de code : Transférer facilement un projet
Analyse de projet : Comprendre une base de code inconnue
Formation IA : Préparer des données d'entraînement
