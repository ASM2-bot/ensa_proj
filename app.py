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



    
from flask import Flask, render_template, request, redirect,url_for,session,flash
from database import execute_query
from config  import config
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config.from_object(config)
@app.route('/')
def index():
    return redirect (url_for('login'))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email= request.form.get ('email')
        password = request.form.get('password')
        query = "SELECT*FROM etudiants WHERE email =%s AND mot_de_passe = %s"
        result = execute_query(query, (email, password), fetch=True)

        if result:
            session['user_id']=result[0]['id']
            session ['user_name']=result[0]['prenom']
            flash('Connexion réussie !','success')
            return redirect(url_for('profile'))
        else:
            flash('Email ou mot de passe incorrect','error')
            return redirect (url_for('login'))
    return render_template('auth/login.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        password = request.form.get('password')
        filiere = request.form.get('filiere')
        ecole = request.form.get('ecole')
        check_query = "SELECT * FROM etudiants WHERE email = %s"
        existing = execute_query(check_query,(email,),fetch=True)

        if existing:
            flash('Cet email est déja utilisé','error')
            return redirect(url_for('register'))
        insert_query = """
            INSERT INTO etudiants (nom,prenom,email,mot_de_passe, filiere, ecole)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(insert_query,(nom,prenom,email,password,filiere,ecole))
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login')) 
    return render_template('auth/register.html')
 
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash ('Veuillez vous connecter d\'abord', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    query = "SELECT * FROM etudiants WHERE id = %s"
    etudiant = execute_query(query,(user_id,),fetch=True)

    if etudiant:
        return render_template('profile/profile.html',etudiant=etudiant[0])
    else:
        flash('Erreur lors du chargement du profil','error')
        return redirect (url_for('login'))
    
@app.route('/notes')
def notes():
    if 'user_id' not in session :
        flash ('Veuillez vous connecter d\'abord','error')
        return redirect(url_for('login'))
    user_id = session['user_id']
    query = "SELECT * FROM notes WHERE etudiant_id = %s"
    notes_list = execute_query(query,(user_id,),fetch=True)

    total_points = 0
    total_coef = 0

    if notes_list: # type: ignore
        for note in notes_list: # type: ignore
            total_points += float(note['note']) * int(note['coefficient'])
            total_coef += int(note['coefficient'])
        moyenne = round(total_points / total_coef, 2) if total_coef > 0 else 0
    else:
        moyenne = 0

    return render_template('notes/notes.html', notes= notes_list, moyenne=moyenne)

@app.route('/contact')
def contact():
    query = "SELECT * FROM contact "
    contacts = execute_query(query,fetch=True)

    return render_template('contact/contact.html', contacts=contacts)

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie','success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)


