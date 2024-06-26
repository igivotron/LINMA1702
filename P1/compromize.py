from matplotlib import pyplot as plt
import numpy as np

from optimize import optimize
from extract_data import ExtractData

sites_file = "Data-partie-1/Sites.csv"
onshore_file = "Data-partie-1/Rendements_onshore.csv"
offshore_file = "Data-partie-1/Rendements_offshore.csv"

data = ExtractData(sites_file, onshore_file, offshore_file)
ct = data.onshore_capacities()
cm = data.offshore_capacities()
Rt = data.onshore_rendements()
Rm = data.offshore_rendements()

P,k = 5e5, 0.17

### Question 2
### Pour un ensemble de sites éoliens, 
### Pour des valeurs P, k déterminées,
### On fait varier S (limite sur l'énergie de source non éolienne achetée sur l'année),
### On resout le probleme d'optimisation,
### et on observe la variation de l'objectif atteint z.

### Ensuite, on choisit un couple de valeurs (S,z) qui semble adapté et on graphe le résultat.

### Deux interpretations sont possibles :
 
### Premiere interpretation : P et S sont indépendants

### Seconde interprétation : comme P et S sont tous les deux liés à une notion de budget,
### augmenter l'un équivaut à diminuer l'autre.
### On écrit, pour B un budget total, P0 la puissance totale installable lorsque S vaut 0, et h le nombre d'heures considérées,
### B = P0*h = P*h + S
### Ce calcul est bien entendu fictif et B n'a aucun sens monétaire. Il sert juste à mettre en regard les deux valeurs.

### La premiere interprétation est gardée (c'est celle qui est décrite dans le rapport)
interpretation = 1


###################################
## Relatif a l'interpretation 1 ###
###################################

def make_comparison1 (P,k,n,min,max,exp=False) :
    """
    Produit et sauve le graphe des valeurs z, énergie produite, énergie achetée, énergie disponible, selon S. 
    Le graphe contient n*4 points.
    Cette fonction effectue, pour n valeurs de S réparties entre min et max,
    la résolution du problème d'optimisation décrit plus bas, prenant en paramètres P, k, et S.
    Elle affiche sur le graphe l'ensemble des points (S,z), (S,Eprod/h) (S,Each/h), (S,Edisp/h) obtenus, 
    où z est l'objectif atteint du problème d'optimisation,
    Eprod est l'énergie produite sur un an,
    Each est l'énergie achetée sur un an,
    Edisp est l'énergie disponible (Eprod + Each) sur un an.
    Les trois sont calibrées (divisées par le nombre de périodes h) dans le but d'être visuellement comparables avec la valeur z.

    Args :
    P : puissance totale installable
    k : portion de P devant etre attribuee a des sites offshore
    n : nombre de résolutions à effectuer 
    exp : booleen indiquant si les valeurs de S sont prises ou non exponentiellement
    par défaut = False
    si exp = True, les valeurs de S sont prises exponentiellement entre 10^min et 10^max
    si exp = False, les valeurs de S sont prises lineairement entre min et max

    Returns :
    None

    RAPPEL :
    Le probleme d'optimisation dont il est question ici est celui correspondant à la question 2A du projet.
    
    Pour un ensemble de sites éoliens onshore et offshore, 
    dont on connaît la capacité et le rendement théorique par heure sur un an,
    Pour une valeur P (puissance totale installable),
    Une portion de cette valeur kP devant etre attribuée à des sites offshore,
    On fait varier S (limite sur l'énergie de source non éolienne achetée sur l'année),
    Et on resout le probleme d'optimisation,
    qui consiste a maximiser la plus petite valeur d'énergie théoriquement disponible (produite + achetée) sur une période d'une heure,
    selon les variables x,s et z (respectivement, 
    portion du site installé [pour chaque site],
    énergie achetée pour l'heure [pour chaque heure],
    plus petite valeur d'énergie théoriquement obtenue sur une heure).
    """

    if exp :
        S_exp = np.linspace(min,max,n)
        S_values = 10**S_exp
    else :
        S_values = np.linspace(min,max,n)

    z_values = np.zeros((n))
    Etot_values = np.zeros((n))
    stot_values = np.zeros((n))

    for i in range (n) :
        print("point : ",i)
        (x,s), z_values[i], sol = optimize(ct,cm,Rt,Rm,P,k,modele=2,S=S_values[i])
        Etot_values[i] = sol.Etot
        stot_values[i] = np.sum(s)

    plt.figure()
    plt.xlabel("S [MWh]")
    plt.ylabel("energie [MWh]")
    if exp :
        plt.semilogx(S_values,z_values,label="minimum de l'energie produite + achetee")
        plt.semilogx(S_values,Etot_values/8760,label="energie totale produite/nb d'heures")
        plt.semilogx(S_values,stot_values/8760,label="energie totale achetee/nb d'heures")
        plt.semilogx(S_values,(Etot_values+stot_values)/8760,label="energie totale disponible/nb d'heures")
    else :
        plt.stem(S_values,z_values,linefmt='C2-',markerfmt='C2x',basefmt='C2',label="minimum de l'energie produite + achetee")
        plt.stem(S_values,Etot_values/8760,linefmt='C1-',markerfmt='C1o',basefmt='C1',label="energie totale produite/nb d'heures")
        plt.stem(S_values,stot_values/8760,linefmt='C0-',markerfmt='C0o',basefmt='C0',label="energie totale achetee/nb d'heures")
        plt.stem(S_values,(Etot_values+stot_values)/8760,linefmt='C3-',markerfmt='C3o',basefmt='C3',label="energie totale disponible/nb d'heures")
    plt.title("Résolutions : résultats selon la contrainte S",y=1.08)
    plt.legend()
    name = "Q2_zselonS_i1_{}values.png".format(n)
    plt.savefig(name,bbox_inches='tight')
    plt.show()


if (interpretation == 1) :
    make_comparison1(P,k,20,0,1e8,exp=False)

# Valeurs de max pour S utilisées : 1e15, 1e10, 5e9, 1e9, 1e8, 1e7



###################################
## Relatif a l'interpretation 2 ###
###################################

## Remarque : l'interprétation 2 a été vite mise de côté, pour cette raison, la fonction make_comparison2 est moins développée que make_comparison1.

def make_comparison2 (P0,k,n) :
    """
    Produit et sauve le graphe des valeurs z selon S. Le graphe contient n points.
    Cette fonction effectue, pour n valeurs de S réparties entre 0 et P0*8760,
    la résolution du problème d'optimisation décrit plus bas, prenant en paramètres P=P0-S/h, k, et S.
    Elle affiche sur le graphe l'ensemble des points (S,z) obtenus, où z est l'objectif atteint du problème d'optimisation.

    Cette fonction procède comme make_comparison1 mais en diminuant P lorsque S augmente (notion de "budget total").

    Args :
    P0 : puissance totale installable pour S = 0
    k : portion de P devant etre attribuee a des sites offshore
    n : nombre de résolutions à effectuer 

    Returns :
    None

    RAPPEL : 
    Le probleme d'optimisation dont il est question ici est celui correspondant à la question 2A du projet.
    
    Pour un ensemble de sites éoliens onshore et offshore, 
    dont on connaît la capacité nominale et le rendement théorique par heure sur un an,
    Pour une valeur P (puissance nominale totale installable),
    Une portion de cette valeur kP devant etre attribuée à des sites offshore,
    On fait varier S (limite sur l'énergie de source non éolienne achetée sur l'année),
    Et on resout le probleme d'optimisation,
    qui consiste a maximiser la plus petite valeur d'énergie théoriquement disponible (produite + achetée) sur une période d'une heure,
    selon les variables x,s et z (respectivement, 
    portion du site installé [pour chaque site],
    énergie achetée pour l'heure [pour chaque heure],
    plus petite valeur d'énergie théoriquement obtenue sur une heure).
    """

    h = 8760
    min = 0
    max = P0*h
    
    S_values = np.linspace(min,max,n)
    z_values = np.zeros((n))

    P_values = ( P0*h - S_values ) / h

    for i in range (n) :
        print("point : ",i)
        (x,s), z_values[i], sol = optimize(ct,cm,Rt,Rm,P_values[i],k,modele=2,S=S_values[i])

    plt.figure()
    plt.xlabel("S [MWh]")
    plt.ylabel("z [MWh]")
    plt.stem(S_values,z_values,label="minimum de l'energie produite + achetee")
    plt.title("Graphe de l'objectif selon la qté max d'énergie pouvant être achetée sur l'année, P0 = {}, k = {}".format(P0,k),y=1.08)
    plt.title()
    name = "Q2_zselonS_i2_{}values.png".format(n)
    plt.savefig(name,bbox_inches='tight')

if (interpretation == 2) :
    make_comparison2(P,k,10)