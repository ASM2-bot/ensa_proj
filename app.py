from flask import Flask, render_template, request
from database import (
    get_all_filieres,
    get_all_absences,
    get_absence_by_student,
    get_emploi_by_filiere
)

app = Flask(__name__)


@app.route('/')
def index():
    try:
        filieres = get_all_filieres()
        return render_template('filieres.html', filieres=filieres)
    except Exception as e:
        return f"<h1>Erreur</h1><p>{e}</p>"


@app.route('/filieres')
def filieres():
    try:
        filieres_list = get_all_filieres()
        print(f"DEBUG: {len(filieres_list)} filières récupérées")
        return render_template('filieres.html', filieres=filieres_list)
    except Exception as e:
        return f"<h1>Erreur</h1><p>{e}</p>"


@app.route('/absence')
def absences():
    try:
        etudiant_nom = request.args.get('etudiant', None)
        
        if etudiant_nom:
            absences_list = get_absence_by_student(etudiant_nom)
            etudiant_selectionne = etudiant_nom
        else:
            absences_list = get_all_absences()
            etudiant_selectionne = None
        
        # Récupérer la liste unique des étudiants
        all_absences = get_all_absences()
        etudiants = list(set([abs['etudiant_nom'] for abs in all_absences]))
        etudiants.sort()

        return render_template(
            'absence.html',
            absences=absences_list,
            etudiants=etudiants,
            etudiant_selectionne=etudiant_selectionne
        )
    except Exception as e:
        return f"<h1>Erreur</h1><p>{e}</p>"


@app.route('/emploi')  # Suppression de l'espace dans l'URL
def emploi_du_temps():
    try:
        filiere_id = request.args.get('filiere', None)
        print(">>> FILIERE REÇUE PAR FLASK =", repr(filiere_id))
        filieres = get_all_filieres()
        
        if filiere_id:
            emploi = get_emploi_by_filiere(filiere_id)
            filiere_selectionnee = int(filiere_id)
        else:
            emploi = []
            filiere_selectionnee = None
        
        return render_template(
            'emploi.html',
            filieres=filieres,
            emploi=emploi,
            filiere_selectionnee=filiere_selectionnee
        )
    except Exception as e:
        return f"<h1>Erreur</h1><p>{e}</p>"


@app.route('/calendrier')
def calendrier_academique():
    try:
        return render_template('calendrier.html')
    except Exception as e:
        return f"<h1>Erreur</h1><p>{e}</p>"


if __name__ == '__main__':
    app.run(debug=True, port=5000)



    