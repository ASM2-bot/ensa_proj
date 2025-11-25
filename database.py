import mysql.connector
from mysql.connector import Error
from config import config 

def get_db_connection():
    try:
        connection=mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port = config.MYSQL_PORT
        )
        if connection.is_connected():
            print("connexion reussie à MYSQL")
            return connection
         
    except Error as e:
        print (f" erreur de connexion à MYSQL:{e}")
        return None

def execute_query(query, params=None, fetch=False):
    connection = get_db_connection()
    if  not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f" Erreur d'exécution de requête: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(" Connexion MySQL fermée")

def test_connection():
    connection = get_db_connection()
    if connection:
        print(" Testdeconnexion réussi")
        connection.close()
        return True
    else:
        print(" Testdeconnexion échoue")
        return False