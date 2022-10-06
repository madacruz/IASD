/* a. Quelles sont les dates du concert de Mireille à la Cigale ? */

CREATE TABLE Concert_par_Artiste(
    Artiste TEXT,
    Nom_Salle TEXT,
    Concert_ID INT,
    Date_Concert DATE, /* Format yyyy-mm-dd */
    PRIMARY KEY((Artiste, Nom_Salle), Date_Concert)
);

INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Mireille', 'Cigale', 1, '2021-01-05');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Mireille', 'Cigale', 2, '2021-02-05');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Yves', 'Animatis', 3, '2022-01-27');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Jeanine', 'ZenithAuvergne', 4, '2021-12-15');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Jeanine', 'ZenithAuvergne', 5, '2021-12-16');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Jeanine', 'ZenithAuvergne', 6, '2021-12-17');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Paulette', 'Bikini', 7, '2022-02-06');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Yves', 'Astrada', 8, '2021-01-05');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Yves', 'Cigale', 9, '2021-03-25');
INSERT INTO Concert_par_Artiste(Artiste, Nom_Salle, Concert_ID, Date_Concert) VALUES('Jeanine', 'AccorHotelArena', 10, '2021-03-10');

SELECT Date_Concert FROM Concert_par_Artiste 
WHERE Artiste = 'Mireille'
AND Nom_Salle = 'Cigale';


/* b. Quels sont les noms des salles ayant la plus grande capacité ? */

CREATE TABLE Salle(
    Salle_ID INT,
    Nom TEXT, 
    Adresse TEXT, 
    Capacite INT,
    PRIMARY KEY (Salle_ID, Capacite)
) WITH CLUSTERING ORDER BY (Capacite DESC);

INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(1, 'AccorHotalArena', 'Paris', 20000);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(2, 'ZenithAuvergne', 'Cournon', 10000);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(3, 'Cigale', 'Paris', 2000);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(4, 'Bataclan', 'Paris', 3000);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(5, 'Bikini', 'Toulouse', 1000);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(6, 'Astrada', 'Marsiac', 50000); 
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(7, 'LePlan', 'Ris', 2000);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(8, 'Ninkasi', 'Lyon', 500);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(9, 'Animatis', 'Issoire', 3);
INSERT INTO Salle(Salle_ID, Nom, Adresse, Capacite) VALUES(10, 'ZenithToulouse', 'Toulouse', 25000);

SELECT Nom FROM Salle LIMIT 1;

/* f. Combien de billets de catégorie 1 ont été vendus par spectacles le '2020-30-11' ? */

CREATE TABLE Billet_Vendu_par_Date(
	Vente_ID INT,
	Date_Vente DATE,
	Categorie_Billet INT,
	Spectacle_ID INT,
	PRIMARY KEY ((Date_Vente, Spectacle_ID, Categorie_Billet), Vente_IDs)
);

INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (1, '2020-12-12', 1, 8);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (2, '2020-10-07', 1, 8);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (3, '2020-11-30', 1, 8);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (4, '2020-11-30', 1, 4);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (5, '2020-08-07', 2, 4);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (6, '2020-06-17', 1, 9);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (7, '2020-11-09', 3, 4);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (8, '2020-12-09', 2, 7);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (9, '2020-12-25', 4, 2);
INSERT INTO Billet_Vendu_par_Date(Vente_ID, Date_Vente, Categorie_Billet, Spectacle_ID) VALUES (10, '2020-12-12', 1, 2);

SELECT Spectacle_ID, Count(*) FROM Billet_Vendu_par_Date WHERE Spectacle_ID = 8 AND Date_Vente = '2020-11-30' AND Categorie_Billet = 1;
