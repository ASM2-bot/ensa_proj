CREATE DATABASE IF NOT EXISTS gestion_etudiants;
USE gestion_etudiants;
CREATE TABLE IF NOT EXISTS etudiants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    filiere VARCHAR(100) NOT NULL,
    ecole VARCHAR(100) NOT NULL,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    etudiant_id INT NOT NULL,
    module VARCHAR(150) NOT NULL,
    note DECIMAL(5,2) NOT NULL,
    coefficient INT NOT NULL,
    type_evaluation VARCHAR(50) NOT NULL,
    statut VARCHAR(20) NOT NULL,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service VARCHAR(100) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    reseaux_sociaux TEXT
);
INSERT INTO etudiants (nom, prenom, email, mot_de_passe, filiere, ecole) VALUES
('Filali', 'Fatima', 'fatima.f@ensa.ma', 'password123', 'ITIRC', 'ENSA'),
('Alami', 'Mohammed', 'mohammed.a@ensa.ma', 'password123', 'ITIRC', 'ENSA'),
('Bennani', 'Sara', 'sara.b@ensa.ma', 'password123', 'ITIRC', 'ENSA');
INSERT INTO notes (etudiant_id, module, note, coefficient, type_evaluation, statut) VALUES
-- Notes pour Fatima (id=1)
(1, 'Mathématiques', 14.00, 3, 'DS', 'Validé'),
(1, 'Python', 16.00, 2, 'Projet', 'Validé'),
(1, 'Base de données', 9.00, 2, 'Examen', 'Rattrapage'),
(1, 'Réseaux', 13.50, 3, 'TP', 'Validé'),
(1, 'Systèmes', 11.00, 2, 'DS', 'Rattrapage'),
-- Notes pour Mohammed (id=2)
(2, 'Mathématiques', 15.00, 3, 'DS', 'Validé'),
(2, 'Python', 12.50, 2, 'Projet', 'Validé'),
(2, 'Base de données', 13.00, 2, 'Examen', 'Validé'),
(2, 'Réseaux', 10.00, 3, 'TP', 'Rattrapage'),
-- Notes pour Sara (id=3)
(3, 'Mathématiques', 17.00, 3, 'DS', 'Validé'),
(3, 'Python', 18.00, 2, 'Projet', 'Validé'),
(3, 'Base de données', 16.50, 2, 'Examen', 'Validé'),
(3, 'Réseaux', 15.00, 3, 'TP', 'Validé');
INSERT INTO contact (service, telephone, email, reseaux_sociaux) VALUES
('Scolarité', '05-37-68-71-72', 'scolarite@ensa.ma', 'Facebook: ENSA Officiel | Instagram: @ensa_official'),
('Bibliothèque', '05-37-68-71-73', 'bibliotheque@ensa.ma', 'Facebook: Bibliothèque ENSA | Twitter: @ensa_biblio'),
('Support Technique', '05-37-68-71-74', 'support@ensa.ma', 'WhatsApp: +212 6 12 34 56 78');
SELECT 'Base de données créée avec succès!' AS Message;