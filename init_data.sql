-- ============================================================
-- Script d'initialisation de la base de données
-- Base de données : gestion_scolaire
-- Encodage : UTF-8
-- ============================================================

USE gestion_scolaire;

-- Suppression des données existantes (optionnel - décommentez si nécessaire)
-- DELETE FROM annonces;
-- DELETE FROM emploi;
-- DELETE FROM absences;
-- DELETE FROM modules;
-- DELETE FROM students;
-- DELETE FROM filieres;

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
    ('laila_gi', 'CP004', 'Laila El Fassi', 3),
    ('youssef_itirc', 'CP005', 'Youssef Alami', 1),
    ('fatima_gtr', 'CP006', 'Fatima Zaki', 2);

-- ------------------------------------------------------
-- INSERT MODULES
-- ------------------------------------------------------
INSERT INTO modules (nom, semestre, filiere_id)
VALUES
    -- Modules ITIRC (filiere_id = 1)
    ('Réseaux Informatiques', 1, 1),
    ('Protocoles & Routage', 2, 1),
    ('Sécurité des Réseaux', 1, 1),
    ('Administration Système', 2, 1),
    
    -- Modules GTR (filiere_id = 2)
    ('Télécoms Fondamentaux', 1, 2),
    ('Traitement du Signal', 2, 2),
    ('Réseaux Sans Fil', 1, 2),
    
    -- Modules GI (filiere_id = 3)
    ('Programmation Orientée Objet', 1, 3),
    ('Bases de Données', 2, 3),
    ('Développement Web', 1, 3),
    ('Intelligence Artificielle', 2, 3);

-- ------------------------------------------------------
-- INSERT ABSENCES
-- ------------------------------------------------------
INSERT INTO absences (etudiant_nom, module, date_absence, filiere_id)
VALUES
    ('Mohamed El Idrissi', 'Réseaux Informatiques', '2025-02-10', 1),
    ('Sara Bennani', 'Protocoles & Routage', '2025-02-11', 1),
    ('Amine Fadil', 'Télécoms Fondamentaux', '2025-02-12', 2),
    ('Laila El Fassi', 'Bases de Données', '2025-02-08', 3),
    ('Mohamed El Idrissi', 'Sécurité des Réseaux', '2025-02-15', 1),
    ('Youssef Alami', 'Réseaux Informatiques', '2025-02-14', 1),
    ('Fatima Zaki', 'Réseaux Sans Fil', '2025-02-13', 2);

-- ------------------------------------------------------
-- INSERT EMPLOI DU TEMPS
-- ------------------------------------------------------
INSERT INTO emploi (jour, heure, module, salle, filiere_id)
VALUES
    -- Emploi ITIRC (filiere_id = 1)
    ('Lundi', '08:00-10:00', 'Réseaux Informatiques', 'S1', 1),
    ('Lundi', '10:00-12:00', 'Sécurité des Réseaux', 'S2', 1),
    ('Mardi', '10:00-12:00', 'Protocoles & Routage', 'S2', 1),
    ('Mercredi', '14:00-16:00', 'Administration Système', 'L1', 1),
    
    -- Emploi GTR (filiere_id = 2)
    ('Lundi', '14:00-16:00', 'Télécoms Fondamentaux', 'T1', 2),
    ('Mardi', '08:00-10:00', 'Réseaux Sans Fil', 'T2', 2),
    ('Jeudi', '14:00-16:00', 'Traitement du Signal', 'T3', 2),
    
    -- Emploi GI (filiere_id = 3)
    ('Lundi', '08:00-10:00', 'Développement Web', 'L3', 3),
    ('Mardi', '14:00-16:00', 'Bases de Données', 'L2', 3),
    ('Mercredi', '08:00-10:00', 'Programmation Orientée Objet', 'L2', 3),
    ('Vendredi', '10:00-12:00', 'Intelligence Artificielle', 'L4', 3);

-- ------------------------------------------------------
-- INSERT ANNONCES
-- ------------------------------------------------------


-- ------------------------------------------------------
-- Vérification des données insérées
-- ------------------------------------------------------
SELECT 'Données insérées avec succès!' AS statut;

SELECT 
    (SELECT COUNT(*) FROM filieres) AS nb_filieres,
    (SELECT COUNT(*) FROM students) AS nb_etudiants,
    (SELECT COUNT(*) FROM modules) AS nb_modules,
    (SELECT COUNT(*) FROM absences) AS nb_absences,
    (SELECT COUNT(*) FROM emploi) AS nb_cours,
    (SELECT COUNT(*) FROM annonces) AS nb_annonces;