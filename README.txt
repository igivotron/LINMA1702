Repertoire consacré à la partie informatique de la réalisation du projet d'optimisation (cours LINMA1702) :
Localisation optimale des capacités de production éolienne en Europe : Partie I.

Groupe 41 : 
DEJONGE Olivia, GREGOIRE Igor, MARZULLO Luca, BOLAND Claire

Ce repertoire contient un ensemble de modules utiles et un Jupyter Notebook.
Ils interagissent entre eux et avec le dossier Data-partie-1 tel que fourni sur Moodle. Ce dernier n'est pas inclus dans ce répertoire.

************************************************************************
Module 1 : extract_data
************************************************************************
Le module extract_data contient une classe ExtractData. 
Elle permet d'extraire les données des fichiers fournis et est adaptée uniquement a ceux-ci.

***********************************************************************
Module 2 : plotMap
***********************************************************************
Le module plotMap définit la fonction plotMap qui mappe les sites sur une carte, en fonction des résultats obtenus.

***********************************************************************
Module 3 : graphs
***********************************************************************
Le module graphs definit quatre fonctions qui graphent les rendements et les énergies en fonction du temps,
et établissent des comparaisons entre modèles selon les résultats obtenus.
Les fonctions sauvent, au format png et avec un nom spécifié en argument, les figures nécessaires au rapport.

***********************************************************************
Notebook
***********************************************************************
Le notebook emploie les fonctions définies dans extract_data, plotMap et graphs,
définit des matrices utiles dans la résolution des problèmes posés,
définit la fonction mod3ContSup utile à la résolution du troisième modèle, l'objet Solution et la fonction getSolution utiles à l'affichage des graphes,
définit les fonctions modele1, modele2 et modele3 (résolution des modèles linéaires tels que décrits dans les questions 1, 2 et 3 du projet),
les résout et en affiche les résultats.

**********************************************************************
Module 4 : modeles
**********************************************************************
Le module modeles definit quatre fonctions : modele1, modele2, mod3ContSup et modele3, 
qui optimisent les modèles propres à chaque question et renvoient les variables d'intérêt.
Ce sont exactement les mêmes que celles du notebook. 
(pourquoi ? il nous semblait bon pour la correction que le code concernant l'optimisation soit affiché directement dans le notebook plutôt que d'y être importé)

**********************************************************************
Module 5 : optimize
**********************************************************************
Le module optimize definit une classe Solution et une fonction globale optimize.
La fonction optimize prend en argument le numéro du modèle concerné, 
emploie la fonction de modeles en lien avec celui-ci et renvoie les variables d'intérêt, 
ainsi qu'un objet Solution contenant des données utiles pour analyser la solution fournie.
optimize effectue globalement les mêmes tâches que celles du notebook.
Elle est employée dans les deux modules suivants.

Remarque : les deux modules suivants exécutent leurs propres fonctions. 
Ces fonctions sont placées hors du notebook en raison de leur lenteur d'exécution.

**********************************************************************
Module 6 : le_temps_des_cerises
**********************************************************************
Le module le_temps_des_cerises emploie extract_data, optimize, 
et effectue un certain nombre de fois la résolution du premier et du troisième modèle en calculant le temps necessaire, selon la taille des données fournies.
Il effectue, pour chaque taille de données, une moyenne sur 100 résolutions pour effacer les variations de "bruit".

**********************************************************************
Module 7 : compromize
**********************************************************************
compromize emploie extract_data, optimize, et effectue un certain nombre de fois la resolution du second modèle en fonction du parametre S.




plotMap ---------------------------------------------------------->|
                                                                   |
graphs ----------------------------------------------------------->|-----> notebook
                                                                   |
                                               ------------------->|
                                               |
extract_data --------------------------------->        ----> le_temps_des_cerises
                                               |      |
                                                ----> |    
                                               |      |
modeles ----------------> optimize ----------->        ----> compromize