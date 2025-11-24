USE gestion_scolaire;

-- ------------------------------------------------------
-- INSERT FILIERES
-- ------------------------------------------------------
INSERT INTO filieres (code, nom, duree, nombre_etudiants)
VALUES
('ITIRC', 'Informatique et Technologies des Réseaux et Communications', '3 ans', 120),
('GTR', 'Génie des Télécommunications et Réseaux', '3 ans', 90),
('GI', 'Génie Informatique', '3 ans', 150);

-- ------------------------------------------------------
-- INSERT STUDENTS
-- ------------------------------------------------------
INSERT INTO students (username, code_personnel, nom, filiere_id)
VALUES
('mohamed123', 'CP001', 'Mohamed El Idrissi', 1),
('sara01', 'CP002', 'Sara Bennani', 1),
('amine_gtr', 'CP003', 'Amine Fadil', 2),
('laila_gi', 'CP004', 'Laila El Fassi', 3);

-- ------------------------------------------------------
-- INSERT MODULES
-- ------------------------------------------------------
INSERT INTO modules (nom, semestre, filiere_id)
VALUES
('Réseaux Informatiques', 1, 1),
('Protocoles & Routage', 2, 1),
('Télécoms Fondamentaux', 1, 2),
('Programmation Orientée Objet', 1, 3),
('Bases de Données', 2, 3);

-- ------------------------------------------------------
-- INSERT ABSENCES
-- ------------------------------------------------------
INSERT INTO absences (etudiant_nom, module, date_absence, filiere_id)
VALUES
('Mohamed El Idrissi', 'Réseaux Informatiques', '2025-02-10', 1),
('Sara Bennani', 'Protocoles & Routage', '2025-02-11', 1),
('Amine Fadil', 'Télécoms Fondamentaux', '2025-02-12', 2),
('Laila El Fassi', 'Bases de Données', '2025-02-08', 3);

-- ------------------------------------------------------
-- INSERT EMPLOI DU TEMPS
-- ------------------------------------------------------
INSERT INTO emploi (jour, heure, module, salle, filiere_id)
VALUES
('Lundi', '08:00-10:00', 'Réseaux Informatiques', 'S1', 1),
('Mardi', '10:00-12:00', 'Protocoles & Routage', 'S2', 1),
('Jeudi', '14:00-16:00', 'Télécoms Fondamentaux', 'T3', 2),
('Vendredi', '08:00-10:00', 'Programmation Orientée Objet', 'L2', 3);

-- ------------------------------------------------------
-- INSERT ANNONCES
-- ------------------------------------------------------
INSERT INTO annonces (titre, contenu, date_publication, filiere_id)
VALUES
('Examen S1', 'L’examen du semestre 1 aura lieu le 20 février.', '2025-02-01', 1),
('Réunion GTR', 'Réunion obligatoire pour les étudiants GTR.', '2025-02-03', 2),
('Projet GI', 'Début du projet POO pour les étudiants GI.', '2025-02-02', 3);
