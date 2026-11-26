# bixi-pulse
![CI](https://github.com/brahimlansari/bixi-pulse/actions/workflows/ci.yml/badge.svg)
Constat (EDA)	Décision pour le modèle
≈ 180 stations retirées les 17 et 18 novembre	Filtre sur les stations actives + séparation train/test dans le temps
Creux à 8 h et 17 h (heure de Montréal)	Features : heure locale, jour de la semaine
Beaucoup de stations presque vides	Prédictions ≥ 0, erreur mesurée à part sur les stations presque vides
Erreur naïve de 1,01 vélo à 60 min	Horizon de 60 min, objectif MAE < 1,01