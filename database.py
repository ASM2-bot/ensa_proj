import mysql.connector
from mysql.connector import Error
from config import config

def get_db_connection():
    """Établit une connexion à la base de données MySQL"""
    try:
        conn = mysql.connector.connect(**config.get_db_config())
        if conn.is_connected():
            print("Connexion MySQL réussie")
            return conn
    except Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Exécute une requête SQL (SELECT ou INSERT/UPDATE/DELETE)"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Erreur d'exécution de requête: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connexion MySQL fermée")

# ========================
# Fonctions spécifiques à ton application
# ========================

def init_filieres_tables():
    """Crée toutes les tables nécessaires"""
    conn = get_db_connection()
    if not conn:
        print("Impossible de créer les tables: pas de connexion")
        return
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filieres(
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(10) NOT NULL UNIQUE,
            nom VARCHAR(100) NOT NULL,
            duree VARCHAR(50),
            nombre_etudiants INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            code_personnel VARCHAR(50) NOT NULL,
            nom VARCHAR(100) NOT NULL,
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            semestre INT,
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS absences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            etudiant_nom VARCHAR(100),
            module VARCHAR(100),
            date_absence DATE,
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emploi (
            id INT AUTO_INCREMENT PRIMARY KEY,
            jour VARCHAR(20),
            heure VARCHAR(20),
            module VARCHAR(100),
            salle VARCHAR(50),
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Toutes les tables ont été créées avec succès.")


# Fonctions de récupération de données

def get_all_filieres():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM filieres ORDER BY nom')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_all_absences():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.id, a.etudiant_nom, a.module, a.date_absence, a.filiere_id,
               f.nom AS filiere_nom
        FROM absences a
        LEFT JOIN filieres f ON a.filiere_id = f.id
        ORDER BY a.date_absence DESC
    ''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_absence_by_student(etudiant_nom):
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.id, a.etudiant_nom, a.module, a.date_absence, a.filiere_id,
               f.nom AS filiere_nom
        FROM absences a
        LEFT JOIN filieres f ON a.filiere_id = f.id
        WHERE a.etudiant_nom = %s
        ORDER BY a.date_absence DESC
    ''', (etudiant_nom,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_emploi_by_filiere(filiere_id):
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT id, jour, heure, module, salle, filiere_id
        FROM emploi
        WHERE filiere_id = %s
        ORDER BY FIELD(jour, 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'), heure
    ''', (filiere_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data
