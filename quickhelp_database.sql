-- ============================================================
--  QUICKHELP - Structure de la base de données
--  Les données de test sont insérées automatiquement par Python
--  au démarrage du serveur (main.py)
-- ============================================================

DROP DATABASE IF EXISTS quickhelp;
CREATE DATABASE quickhelp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE quickhelp;

CREATE TABLE utilisateur (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    nom               VARCHAR(100)  NOT NULL,
    prenom            VARCHAR(100)  NOT NULL,
    email             VARCHAR(255)  NOT NULL UNIQUE,
    mot_de_passe_hash VARCHAR(255)  NOT NULL,
    telephone         VARCHAR(20),
    latitude          DECIMAL(9,6)  DEFAULT 48.8566,
    longitude         DECIMAL(9,6)  DEFAULT 2.3522,
    note_moyenne      DECIMAL(3,2)  DEFAULT 0.00,
    nb_avis           INT           DEFAULT 0,
    date_inscription  DATETIME      DEFAULT CURRENT_TIMESTAMP,
    est_verifie       BOOLEAN       DEFAULT FALSE
);

CREATE TABLE categorie_tache (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    nom               VARCHAR(100)  NOT NULL,
    description       TEXT,
    prix_suggere      DECIMAL(5,2)  NOT NULL,
    duree_estimee_min INT           NOT NULL
);

CREATE TABLE tache (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    demandeur_id     INT           NOT NULL,
    executant_id     INT,
    categorie_id     INT,
    titre            VARCHAR(255)  NOT NULL,
    description      TEXT,
    latitude         DECIMAL(9,6)  NOT NULL,
    longitude        DECIMAL(9,6)  NOT NULL,
    prix             DECIMAL(6,2)  NOT NULL,
    statut           ENUM('publiee','acceptee','en_cours','terminee','annulee') DEFAULT 'publiee',
    statut_paiement  ENUM('en_attente','valide','verse') DEFAULT 'en_attente',
    date_creation    DATETIME      DEFAULT CURRENT_TIMESTAMP,
    date_acceptation DATETIME,
    date_fin         DATETIME,
    CONSTRAINT fk_dem FOREIGN KEY (demandeur_id) REFERENCES utilisateur(id),
    CONSTRAINT fk_exe FOREIGN KEY (executant_id) REFERENCES utilisateur(id),
    CONSTRAINT fk_cat FOREIGN KEY (categorie_id) REFERENCES categorie_tache(id)
);

CREATE TABLE avis (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    tache_id      INT     NOT NULL,
    auteur_id     INT     NOT NULL,
    cible_id      INT     NOT NULL,
    note          TINYINT NOT NULL CHECK (note BETWEEN 1 AND 5),
    commentaire   TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_avis_t FOREIGN KEY (tache_id)  REFERENCES tache(id),
    CONSTRAINT fk_avis_a FOREIGN KEY (auteur_id) REFERENCES utilisateur(id),
    CONSTRAINT fk_avis_c FOREIGN KEY (cible_id)  REFERENCES utilisateur(id),
    UNIQUE KEY uq_avis (tache_id, auteur_id)
);

CREATE TABLE transaction (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    tache_id              INT          NOT NULL UNIQUE,
    montant_total         DECIMAL(6,2) NOT NULL,
    montant_executant     DECIMAL(6,2) NOT NULL,
    commission_plateforme DECIMAL(6,2) NOT NULL,
    statut                ENUM('en_attente','validee','versee') DEFAULT 'en_attente',
    date_transaction      DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tr FOREIGN KEY (tache_id) REFERENCES tache(id)
);

CREATE INDEX idx_tache_statut   ON tache(statut);
CREATE INDEX idx_tache_pos      ON tache(latitude, longitude);
CREATE INDEX idx_user_pos       ON utilisateur(latitude, longitude);
