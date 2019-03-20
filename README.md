# Objectif

Cartographie d'un système de Lotka-Volterra compétitif avec contrôle multiplicatif scalaire
défavorable via Hamilton-Jacobi.

# Design

- une classe pour la modélisation du système différentiel avec contrôle.
- une classe pour la cartographie stockant la valeur
- un dossier pour les maths
- un dossier pour des exemples. 

# Reste à faire

- Régler l'import depuis exemple.
- Visualiser valeur/contrôle via des animations?
- Pour une grille de temps régulière on n'a pas à recalculer les points déplacés par les flux.
- Donner l'option de ne pas utiliser le bang-bang.
- Rajouter une grille pour le contrôle.
- Ne garder que les temps intéressants dans la grille des valeurs.
- Reconstruire les arcs singuliers.
- Création Classe abstraite pour les systèmes?
