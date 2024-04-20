Repertoire consacré à la partie informatique de la réalisation du projet d'optimisation (cours LINMA1702) :
Localisation optimale des capacités de production éolienne en Europe : Partie I.

Ce repertoire contient un ensemble de modules utiles et un Jupyter Notebook.
Ils interagissent entre eux et avec le dossier Data-partie-1 tel que fourni sur Moodle.

Le module extract_data contient une classe ExtractData. 
Elle permet d'extraire les données des fichiers fournis et est adaptée uniquement a ceux-ci.

Le module "modeles" definit trois fonctions, modele1, modele2 et modele3, 
qui optimisent les modèles propres à chaque question et renvoient les variables d'intérêt.

Le module "optimize" definit une classe "Solution" et une fonction globale "optimize".
La fonction "optimize" prend en argument le numéro du modèle concerné, 
emploie la fonction de "modeles" en lien avec celui-ci et renvoie les variables d'interet, 
ainsi qu'un objet "Solution" contenant des données utiles pour analyser la solution fournie.

Le module "graphs" definit quatre fonctions, graph_rendements, graph_Q1energy, graph_Q2energy, graph_comparison,
qui graphent les rendements, les énergies, en fonction du temps et des comparaisons entre modeles selon les résultats obtenus.

Le module "plotMap" définit la fonction plotMap qui mappe les sites sur une carte, en fonction des resultats obtenus.

le_temps_des_cerises emploie extract_data, optimize, modeles, et effectue un certain nombre de fois la resolution en calculant le temps necessaire.
compromize emploie extract_data, optimize, modeles, et effectue un certain nombre de fois la resolution de la Q2 en fonction du parametre Solution.

le jupyter notebook emploie extract_data, graphs, plotMap, redéfinit modeles et reformule completement optimize sans en garder le nom,
et effectue les resolutions des 3 questions selon les differents parametres choisis

pourquoi reformuler modeles et optimize dans le notebook ?
question de lisibilite pour la remise : il nous semblait bon que le code concernant l'optimisation soit affiché dans le notebook

Nous devons conserver neanmoins les modules optimize et modeles pour pouvoir employer le_temps_des_cerises et compromize, 
et devons etre attentifs à la synchronisation entre les fonctions optimize, modele1, modele2 modele3 des modules
et les fonctions getSolution, modele1, modele2, modele3 + code hors fonction du jupyter notebook.