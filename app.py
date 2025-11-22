

from flask import Flask, render_template
from database import get_all_filieres , get_all_absences,get_absence_by_student


app=Flask(__name__)


@app.route('/')
def index():
    try:
        filieres=get_all_filieres()
        return render_template('filieres.html',filieres=filieres)
    except Exception as e:
        return f"<h1>erreur</h1><p>{e}</p>"
    



@app.route('/filieres')
def filieres():
    try:
        filieres_list=get_all_filieres()
        print(f"DEBUG:{len(filieres_list)}filieres recuperee")
        return render_template('filieres.html',filieres=filieres_list)
    except Exception as e:
        return f"<h1>erreur</h1><p>{e}</p>"
    




@app.route('/abscence')
def abscences():
    from flask import request 
    try:
        etudiant_nom=request.args.get('etudiant',None)
        if etudiant_nom:
          abscences_list=get_absence_by_student(etudiant_nom)
          etudiant_selectionne=etudiant_nom
        else:
          abscences_list= get_all_absences()
          etudiant_selectionne=None 
        all_absences=get_all_absences() 
        etudiants=list(set([abs['etudiant_nom'] for abs in get_all_absences()]))   
        etudiants.sort()


        return render_template('abscence.html',
                         absences=abscences_list,
                         etudiants=etudiants,
                         etudiant_selectionne=etudiant_selectionne)  
    except Exception as e:
        return f"<h1>erreur</h1><p>{e}</p>"


@app.route('/Emploi du temps')
def Emploidutemps():
    from flask import request
    from database import get_all_filieres,get_emploi_by_filiere

    filiere_id=request.args.get('filiere',None)
    filieres=get_all_filieres()
    if filiere_id:
        emploi=get_emploi_by_filiere(filiere_id)
        filiere_selectionnee=int(filiere_id)
    else:
        emploi=[]
        filiere_selectionnee=None
    return render_template('emploi.html',filieres=filieres,emploi=emploi,filiere_selectionnee=filiere_selectionnee)





    

@app.route('/Calendrier académique')
def Calendrieracadémique():

    return render_template('Calendrier.html') 
if __name__ =='__main__':
    app.run(debug=True,port=5000)  



    