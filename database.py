
import mysql.connector
from config import mysql_config
def get_db_connection():
    try:
        conn = mysql.connector.connect(**mysql_config)
        print("connexion mysql reussie ")
        return conn 
    except Exception as e:
        print(f"erreur de connexion mysql:{e}")
        return None
    
    #creation ddees tables :
def init_fillieres_tables():
    conn=get_db_connection()
    cursor=conn.cursor()

#tables fillieres
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS filieres(
        id INT AUTO_INCREMENT PRIMARY KEY,
        code VARCHAR(10) NOT NULL UNIQUE,
        nom VARCHAR(100) NOT NULL,

        duree VARCHAR(50),
        nombre_etudiants INT
       
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4           
    ''' )

# table etudiant
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            code_personnel VARVHAR(50) NOT NULL ,
            nom VARCHAR(100) NOT NULL,
            filiere_id INT ,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET =utfmb4
    ''')      
    
    #table modules
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            semestre int ,
            filiere_id INT ,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET =utfmb4
    ''')   

    # table absences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS absences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            etudiant_nom VARCHAR(100) ,
            module VARVHAR(100)  ,
            date_absence DATE,
            filiere_id INT ,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET =utfmb4
    ''')   

    # emploi du temps 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emploi (
            id INT AUTO_INCREMENT PRIMARY KEY,
            jour VARCHAR(20) ,
            heure VARVHAR(20) ,
            module VARCHAR(100) ,
            salle VARCHAR(50) ,
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET =utfmb4
    ''')   

    # table annonce
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS annonces (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titre VARCHAR(20) ,
            contenu text ,
            date_publication  DATE,
            filiere_id INT,
            FOREIGN KEY (filiere_id) REFERENCES filieres(id)
        ) ENGINE=InnoDB DEFAULT CHARSET =utfmb4
    ''')   
    conn.commit()
    cursor.close()
    conn.close()
    print("toute les tables ont ete crees avec succes.")



    
    
    
    



# 3. fillieres 

def get_all_filieres():
    try:
        conn=get_db_connection()
       
        cursor=conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM filieres ORDER BY nom')
        data=cursor.fetchall()
        cursor.close()
        conn.close()
        return data 
        
    except Exception as e:
         print(f"erreur lors de la recuperation des filieres:{e}")
         return[]
    
   


#4.absences

def get_all_absences():
         try:
          conn=get_db_connection()
         
          cursor =conn.cursor(dictionary=True)
          cursor.execute('''
              SELECT a.*,f.nom as filiere_nom
              FROM absences a
                
              LEFT JOIN filieres f ON a.filiere_id=f.id
             
              ORDER BY a.date_absence DESC
          ''')
          data=cursor.fetchall()
          cursor.close()
          conn.close()
          return data
         except Exception as e:
          print(f"ERREUR get_all_absences:{e}")
          return[]



def get_absence_by_student(etudiant_nom):
    try:
          conn=get_db_connection()
          
          cursor =conn.cursor(dictionary=True)
          cursor.execute('''
              SELECT a.*,f.nom as filiere_nom
              FROM absences a           
              LEFT JOIN filieres f ON a.filiere_id=f.id
              WHERE a.etudiant_nom=%s
              ORDER BY a.date_absence DESC
          ''',(etudiant_nom,))
          data=cursor.fetchall()
          cursor.close()
          conn.close()
          return data
    except Exception as e:
          print(f"ERREUR:{e}")
          return[]






def get_emploi_by_filiere(filiere_id):
    try:
          conn=get_db_connection()
          
          cursor =conn.cursor(dictionary=True)
          cursor.execute('''
              SELECT  *FROM emploi
              
              WHERE filiere_id=%s
              ORDER BY jour,heure
          ''',(filiere_id,))
          data=cursor.fetchall()
          cursor.close()
          conn.close()
          return data
    except Exception as e:
          print(f"ERREUR:{e}")
          return[]


def get_modules_by_filiere(filiere_id):
    try:
          conn=get_db_connection()
          
          cursor =conn.cursor(dictionary=True)
          cursor.execute('''
              SELECT * from modules
            
              WHERE filiere_id=%s
              ORDER BY semestre,nom
          ''',(filiere_id,))
          data=cursor.fetchall()
          cursor.close()
          conn.close()
          return data
    except Exception as e:
          print(f"ERREUR:{e}")
          return[]




def get_annonces_by_filiere(filiere_id):
    try:
          conn=get_db_connection()
          
          cursor =conn.cursor(dictionary=True)
          cursor.execute('''
              SELECT * from annonces
            
              WHERE filiere_id=%s
              ORDER BY date_publication DESC
          ''',(filiere_id,))
          data=cursor.fetchall()
          cursor.close()
          conn.close()
          return data
    except Exception as e:
          print(f"ERREUR:{e}")
          return[]




def get_student_by_login(username,code_personnel):
    try:
          conn=get_db_connection()
          
          cursor =conn.cursor(dictionary=True)
          cursor.execute('''
              SELECT * from students
            
              WHERE username=%s AND code_personnel =%s
              
          ''',(username,code_personnel))
          student=cursor.fetchall()
          cursor.close()
          conn.close()
          return student
    except Exception as e:
          print(f"ERREUR:{e}")
          return None
