from flask import Flask, render_template, request,redirect
from datetime import datetime

from database import (
    get_all_filieres,
    get_all_absences,
    get_absence_by_student,
    get_emploi_by_filiere
)

app = Flask(__name__)


@app.route('/')
def index():
    
        filieres = get_all_filieres()
        return render_template('filieres.html', filieres=filieres)
   
@app.route('/retour')
def retour():
      print("REFERRER =", request.referrer)
      return redirect(request.referrer or '/')




@app.route('/filieres')
def filieres():
    
        filieres_list = get_all_filieres()
        return render_template('filieres.html', filieres=filieres_list)




@app.route('/emploi')
def emploi_du_temps():
    
        filiere_id = request.args.get('filiere')
        filieres = get_all_filieres()

        jours = [ 
            "Lundi", "Mardi", "Mercredi", 
            "Jeudi", "Vendredi", "Samedi","Dimanche"
            ]
        emploi_grille = {}

        if filiere_id:
            cours = get_emploi_by_filiere(filiere_id)
            filiere_selectionnee = int(filiere_id)

            for c in cours:
                heure = c["heure"]
                jour = c["jour"]

                if heure not in emploi_grille:
                    emploi_grille[heure] = {}

                emploi_grille[heure][jour] = {
                    "module": c["module"],
                    "salle": c["salle"]
                }

            emploi_grille = dict(sorted(
              emploi_grille.items(),
              key=lambda x: datetime.strptime(x[0].split('-')[0], '%H:%M')
            ))



        else:
            filiere_selectionnee = None

        return render_template(
            "emploi.html",
            filieres=filieres,
            emploi=emploi_grille,
            jours=jours,
            filiere_selectionnee=filiere_selectionnee
        )



@app.route('/absence')
def absences():
    
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


@app.route('/calendrier')
def calendrier_academique():
    
        return render_template('calendrier.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)



    