"""
Script d'initialisation de la base de données
Exécutez ce script pour créer les tables et insérer les données initiales
"""

import mysql.connector
from config import mysql_config
from database import init_filieres_tables


def create_database():
    """Crée la base de données si elle n'existe pas"""
    try:
        # Connexion sans spécifier la base de données
        conn = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password']
        )
        cursor = conn.cursor()
        
        # Création de la base de données
        cursor.execute("CREATE DATABASE IF NOT EXISTS gestion_scolaire CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Base de données 'gestion_scolaire' créée ou déjà existante")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base de données: {e}")
        return False


def execute_sql_file(filepath='init_data.sql'):
    """Exécute le fichier SQL pour insérer les données initiales"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        # Lecture du fichier SQL
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Séparation et exécution des commandes SQL
        sql_commands = sql_script.split(';')
        
        for command in sql_commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                except mysql.connector.Error as e:
                    # Ignorer les erreurs de duplication (données déjà existantes)
                    if e.errno != 1062:  # 1062 = Duplicate entry
                        print(f"⚠️  Avertissement: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Données initiales insérées avec succès")
        return True
        
    except FileNotFoundError:
        print(f"❌ Fichier '{filepath}' introuvable")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        return False


def check_tables():
    """Vérifie que toutes les tables existent"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        required_tables = ['filieres', 'students', 'modules', 'absences', 'emploi', 'annonces']
        
        print("\n📊 Tables dans la base de données:")
        for table in tables:
            status = "✅" if table in required_tables else "ℹ️ "
            print(f"  {status} {table}")
        
        missing_tables = set(required_tables) - set(tables)
        if missing_tables:
            print(f"\n⚠️  Tables manquantes: {', '.join(missing_tables)}")
        else:
            print("\n✅ Toutes les tables nécessaires sont présentes")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des tables: {e}")


def check_data():
    """Vérifie le nombre d'enregistrements dans chaque table"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        tables = ['filieres', 'students', 'modules', 'absences', 'emploi', 'annonces']
        
        print("\n📈 Nombre d'enregistrements par table:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  • {table}: {count} enregistrement(s)")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des données: {e}")


def main():
    """Fonction principale d'initialisation"""
    print("=" * 60)
    print("🚀 INITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    
    # Étape 1: Créer la base de données
    print("📌 Étape 1: Création de la base de données...")
    if not create_database():
        return
    print()
    
    # Étape 2: Créer les tables
    print("📌 Étape 2: Création des tables...")
    try:
        init_filieres_tables()
        print("✅ Tables créées avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return
    print()
    
    # Étape 3: Vérifier les tables
    print("📌 Étape 3: Vérification des tables...")
    check_tables()
    print()
    
    # Étape 4: Insérer les données initiales
    print("📌 Étape 4: Insertion des données initiales...")
    execute_sql_file('init_data.sql')
    print()
    
    # Étape 5: Vérifier les données
    print("📌 Étape 5: Vérification des données...")
    check_data()
    print()
    
    print("=" * 60)
    print("✨ INITIALISATION TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print()
    print("🎯 Vous pouvez maintenant lancer l'application avec:")
    print("   python app.py")
    print()


if __name__ == '__main__':
    main()