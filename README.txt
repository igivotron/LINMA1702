Repertoire consacré à la partie informatique de la réalisation du projet d'optimisation (cours LINMA1702)
Localisation optimale des capacités de production éolienne en Europe : Partie I

Ce repertoire contient un ensemble de modules et 3 "main".
Ils interagissent entre eux et avec le dossier Data-partie-1 tel que fourni sur Moodle.

Le module extract_data contient une classe ExtractData. 
Elle permet d'extraire les données des fichiers fournis et est adaptée uniquement a ceux-ci.

Le module "modeles" definit trois fonctions, modele1, modele2 et modele3, 
qui optimisent les modèles propres à chaque question et renvoient les variables d'intérêt.

Le module "optimize" definit une classe "Solution" et une fonction globale "optimize".
La fonction "optimize" prend en argument le numéro du modèle concerné, 
emploie la fonction de "modeles" en lien avec celui-ci et renvoie les variables d'interet, 
ainsi qu'un objet "Solution" contenant des données utiles pour analyser la solution fournie.

Le module "graphs" definit trois fonctions, graph_rendements, graph_Q1energy, graph_Q2energy,
qui graphent les rendements, les énergies, en fonction du temps et selon les résultats obtenus.

le_temps_des_cerises

etcetcetc