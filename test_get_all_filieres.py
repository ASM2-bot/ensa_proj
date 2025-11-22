# test_get_filieres.py
from database import get_all_filieres

print("=" * 60)
print("TEST DE get_all_filieres()")
print("=" * 60)

filieres = get_all_filieres()

print(f"\n📊 Résultat : {len(filieres)} filières trouvées\n")

if filieres:
    print("Détails des filières :")
    print("-" * 60)
    for f in filieres:
        print(f"  {f['code']:10s} | {f['nom']}")
    print("=" * 60)
    print("✅ La fonction fonctionne !")
else:
    print("❌ Aucune filière trouvée !")
    print("\n💡 Lancez : python init_all_tables.py")