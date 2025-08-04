import os
import json
import sqlite3
from pathlib import Path

def read_file_content(file_path):
    """Lit le contenu d'un fichier avec plusieurs encodages possibles"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"Erreur de lecture: {str(e)}"
    
    return "Impossible de lire le fichier"

def read_sqlite_db(file_path):
    """Lit une base de données SQLite et retourne sa structure"""
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        
        # Récupérer la liste des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        db_info = {
            "type": "sqlite_database",
            "tables": []
        }
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            db_info["tables"].append({
                "name": table_name,
                "columns": columns,
                "row_count": row_count
            })
        
        conn.close()
        return json.dumps(db_info, indent=2)
        
    except Exception as e:
        return f"Erreur lecture DB: {str(e)}"

def scan_project(root_path, output_file="project_content.json"):
    """Scanne tout le projet et crée un JSON avec le contenu"""
    
    # Extensions à ignorer (fichiers binaires/trop lourds)
    ignored_extensions = {'.exe', '.dll', '.so', '.dylib', '.bin', '.img', '.iso', 
                         '.zip', '.rar', '.tar', '.gz', '.7z', '.pdf', '.doc', '.docx',
                         '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
                         '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flv', '.ttf'}
    
    # Dossiers à ignorer
    ignored_dirs = {'node_modules', '.git', '__pycache__', '.vscode', '.idea', 
                   'dist', 'build', '.next', 'coverage', '.nyc_output'}
    
    project_data = {
        "project_name": os.path.basename(root_path),
        "scan_path": root_path,
        "files": []
    }
    
    total_files = 0
    processed_files = 0
    
    # Compter le nombre total de fichiers
    for root, dirs, files in os.walk(root_path):
        # Supprimer les dossiers ignorés
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        total_files += len(files)
    
    print(f"📁 Scan du projet: {root_path}")
    print(f"📊 Nombre total de fichiers: {total_files}")
    print("🔍 Traitement en cours...")
    
    for root, dirs, files in os.walk(root_path):
        # Supprimer les dossiers ignorés
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_path)
            
            # Obtenir l'extension
            extension = Path(file).suffix.lower()
            
            processed_files += 1
            print(f"📄 [{processed_files}/{total_files}] {relative_path}")
            
            file_info = {
                "name": file,
                "path": relative_path,
                "full_path": file_path,
                "extension": extension,
                "size": os.path.getsize(file_path)
            }
            
            # Ignorer les fichiers binaires
            if extension in ignored_extensions:
                file_info["content"] = f"[Fichier binaire ignoré - {extension}]"
            
            # Traitement spécial pour les bases de données SQLite
            elif extension == '.db' or file.endswith('.sqlite') or file.endswith('.sqlite3'):
                file_info["content"] = read_sqlite_db(file_path)
            
            # Fichiers texte (tout le reste)
            else:
                file_info["content"] = read_file_content(file_path)
            
            project_data["files"].append(file_info)
    
    # Sauvegarder le JSON
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(project_data, json_file, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Scan terminé!")
    print(f"📋 {len(project_data['files'])} fichiers traités")
    print(f"💾 Résultat sauvé dans: {output_file}")
    
    return project_data

# Utilisation
if __name__ == "__main__":
    # Chemin vers ton projet
    project_path = input("📁 Chemin vers ton projet: ").strip()
    
    if not os.path.exists(project_path):
        print("❌ Chemin introuvable!")
        exit()
    
    # Nom du fichier de sortie
    output_name = input("💾 Nom du fichier JSON (par défaut: project_content.json): ").strip()
    if not output_name:
        output_name = "project_content.json"
    
    # Scanner le projet
    scan_project(project_path, output_name)

