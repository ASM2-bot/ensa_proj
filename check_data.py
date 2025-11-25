"""
Test ultra simple pour vérifier les données
"""

import mysql.connector
from config import mysql_config

print("=" * 60)
print("🔍 TEST SIMPLE DES DONNÉES")
print("=" * 60)

try:
    # Connexion
    conn = mysql.connector.connect(**mysql_config)
    print("✅ Connexion réussie\n")
    
    cursor = conn.cursor()
    
    # Test 1: Filières
    print("1️⃣  FILIÈRES:")
    cursor.execute("SELECT COUNT(*) FROM filieres")
    count = cursor.fetchone()[0]
    print(f"   Nombre: {count}")
    
    if count > 0:
        cursor.execute("SELECT id, code, nom FROM filieres")
        for row in cursor.fetchall():
            print(f"   ✅ ID: {row[0]} - {row[1]} - {row[2]}")
    else:
        print("   ❌ AUCUNE FILIÈRE!")
    
    # Test 2: Absences
    print("\n2️⃣  ABSENCES:")
    cursor.execute("SELECT COUNT(*) FROM absences")
    count = cursor.fetchone()[0]
    print(f"   Nombre: {count}")
    
    if count > 0:
        cursor.execute("SELECT etudiant_nom, module, date_absence FROM absences LIMIT 5")
        for row in cursor.fetchall():
            print(f"   ✅ {row[0]} - {row[1]} - {row[2]}")
        
        # Liste unique des étudiants
        cursor.execute("SELECT DISTINCT etudiant_nom FROM absences")
        print("\n   📋 Étudiants avec absences:")
        for row in cursor.fetchall():
            print(f"      • {row[0]}")
    else:
        print("   ❌ AUCUNE ABSENCE!")
        print("   👉 LES DONNÉES NE SONT PAS INSÉRÉES")
    
    # Test 3: Emploi du temps
    print("\n3️⃣  EMPLOI DU TEMPS:")
    cursor.execute("SELECT COUNT(*) FROM emploi")
    count = cursor.fetchone()[0]
    print(f"   Nombre: {count}")
    
    if count > 0:
        cursor.execute("SELECT jour, heure, module, salle, filiere_id FROM emploi LIMIT 5")
        for row in cursor.fetchall():
            print(f"   ✅ {row[0]} {row[1]} - {row[2]} (Salle {row[3]}) - Filière: {row[4]}")
    else:
        print("   ❌ AUCUN COURS!")
        print("   👉 LES DONNÉES NE SONT PAS INSÉRÉES")
    
    cursor.close()
    conn.close()
    
    # Conclusion
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC:")
    cursor = conn.cursor() if not conn.is_connected() else None
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM filieres")
    nb_filieres = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM absences")
    nb_absences = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emploi")
    nb_emploi = cursor.fetchone()[0]
    
    if nb_filieres > 0 and nb_absences == 0 and nb_emploi == 0:
        print("⚠️  PROBLÈME IDENTIFIÉ:")
        print("   - Tables créées ✅")
        print("   - Filières insérées ✅")
        print("   - Absences manquantes ❌")
        print("   - Emploi du temps manquant ❌")
        print("\n🔧 SOLUTION:")
        print("   Exécutez: mysql -u root -p gestion_scolaire < init_data.sql")
        print("   OU: python init_database.py")
    elif nb_filieres > 0 and nb_absences > 0 and nb_emploi > 0:
        print("✅ TOUT EST BON!")
        print(f"   - {nb_filieres} filières")
        print(f"   - {nb_absences} absences")
        print(f"   - {nb_emploi} cours")
    else:
        print("⚠️  Situation inhabituelle")
        print(f"   - Filières: {nb_filieres}")
        print(f"   - Absences: {nb_absences}")
        print(f"   - Emploi: {nb_emploi}")
    
    cursor.close()
    conn.close()
    print("=" * 60)

except mysql.connector.Error as e:
    print(f"\n❌ ERREUR MySQL: {e}")
    print(f"   Code erreur: {e.errno}")
    print(f"   Message: {e.msg}")
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()