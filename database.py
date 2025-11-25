import mysql.connector
from config import mysql_config


def get_db_connection():
    """Établit une connexion à la base de données MySQL"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        print("Connexion MySQL réussie")
        return conn
    except Exception as e:
        print(f"Erreur de connexion MySQL: {e}")
        return None


def init_filieres_tables():
    """Crée toutes les tables nécessaires pour l'application"""
    conn = get_db_connection()
    if not conn:
        print("Impossible de créer les tables: pas de connexion")
        return
    
    cursor = conn.cursor()

    # Table filières
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filieres(
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(10) NOT NULL UNIQUE,
            nom VARCHAR(100) NOT NULL,
            duree VARCHAR(50),
            nombre_etudiants INT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    # Table étudiants
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

    # Table modules
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            semestre INT,
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    # Table absences
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

    # Table emploi du temps
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

    # Table annonces


    conn.commit()
    cursor.close()
    conn.close()
    print("Toutes les tables ont été créées avec succès.")


# ============================================
# FONCTIONS DE RÉCUPÉRATION DES DONNÉES
# ============================================

def get_all_filieres():
    """Récupère toutes les filières"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM filieres ORDER BY nom')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"DEBUG get_all_filieres: {len(data)} filières récupérées")
        return data
    except Exception as e:
        print(f"Erreur lors de la récupération des filières: {e}")
        return []


def get_all_absences():
    """Récupère toutes les absences avec les informations de filière"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                a.id,
                a.etudiant_nom,
                a.module,
                a.date_absence,
                a.filiere_id,
                f.nom AS filiere_nom
            FROM absences a
            LEFT JOIN filieres f ON a.filiere_id = f.id
            ORDER BY a.date_absence DESC
        ''')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"DEBUG get_all_absences: {len(data)} absences récupérées")
        if len(data) > 0:
            print(f"DEBUG Exemple: {data[0]}")
        
        return data
    except Exception as e:
        print(f"ERREUR get_all_absences: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_absence_by_student(etudiant_nom):
    """Récupère les absences d'un étudiant spécifique"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                a.id,
                a.etudiant_nom,
                a.module,
                a.date_absence,
                a.filiere_id,
                f.nom AS filiere_nom
            FROM absences a
            LEFT JOIN filieres f ON a.filiere_id = f.id
            WHERE a.etudiant_nom = %s
            ORDER BY a.date_absence DESC
        ''', (etudiant_nom,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"DEBUG get_absence_by_student({etudiant_nom}): {len(data)} absences")
        return data
    except Exception as e:
        print(f"ERREUR get_absence_by_student: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_emploi_by_filiere(filiere_id):
    """Récupère l'emploi du temps d'une filière"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT id,
            jour,
            heure,
            module,
            salle,
            filiere_id   
        FROM emploi
            WHERE filiere_id = %s
            ORDER BY 
                FIELD(jour, 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'),
                heure
        ''', (filiere_id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"DEBUG get_emploi_by_filiere({filiere_id}): {len(data)} cours")
        if len(data) > 0:
            print(f"DEBUG Exemple: {data[0]}")
        
        return data
    except Exception as e:
        print(f"ERREUR get_emploi_by_filiere: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_modules_by_filiere(filiere_id):
    """Récupère les modules d'une filière"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM modules
            WHERE filiere_id = %s
            ORDER BY semestre, nom
        ''', (filiere_id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"ERREUR get_modules_by_filiere: {e}")
        return []


def get_annonces_by_filiere(filiere_id):
    """Récupère les annonces d'une filière"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM annonces
            WHERE filiere_id = %s
            ORDER BY date_publication DESC
        ''', (filiere_id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"ERREUR get_annonces_by_filiere: {e}")
        return []


def get_student_by_login(username, code_personnel):
    """Récupère un étudiant par son login et code personnel"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM students
            WHERE username = %s AND code_personnel = %s
        ''', (username, code_personnel))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        return student
    except Exception as e:
        print(f"ERREUR get_student_by_login: {e}")
        return None


# Fonction de test pour vérifier les données
def test_database():
    """Fonction de test pour vérifier que tout fonctionne"""
    print("\n=== TEST DE LA BASE DE DONNÉES ===\n")
    
    print("1. Test get_all_filieres():")
    filieres = get_all_filieres()
    print(f"   Résultat: {len(filieres)} filières\n")
    
    print("2. Test get_all_absences():")
    absences = get_all_absences()
    print(f"   Résultat: {len(absences)} absences")
    if absences:
        print(f"   Premier étudiant: {absences[0].get('etudiant_nom', 'N/A')}\n")
    
    if filieres:
        filiere_id = filieres[0]['id']
        print(f"3. Test get_emploi_by_filiere({filiere_id}):")
        emploi = get_emploi_by_filiere(filiere_id)
        print(f"   Résultat: {len(emploi)} cours")
        if emploi:
            print(f"   Premier cours: {emploi[0].get('module', 'N/A')}\n")


if __name__ == '__main__':
    test_database()