import numpy as np
from modeles import modele1, modele2, modele3

class Solution :
    """
    Classe creuse créée pour la question 1B.
    Initialisée dans optimize.py.

    (on considère les n sites d'éoliennes dans l'ordre de Sites.csv,
    et les h périodes d'une heure (taille d'une ligne de Rendements_(off)/(on)shore.csv))

    Paramètres :
    - Rm, numpy array de taille h, le rendement moyen par heure
    - Rmtot, scalaire, le rendement moyen sur un an
    - E, numpy array de taille h, production d'énergie au cours du temps
    - Etot, scalaire, énergie totale produite au cours d'une année
    """
    
    def __init__(self, Rm, Rmtot, E, Etot) :
        self.Rm = Rm
        self.Rmtot = Rmtot
        self.E = E
        self.Etot = Etot  


def optimize (ct, cm, Rt, Rm, P, k, modele = 1, S=0, delta=0, T=0, checkpoints = False) :
    """
    Fonction générique pour la résolution du problème d'optimisation linéaire, en variables continues,
    de la localisation des productions éoliennes en Europe,
    selon 2 modèles.

    Optimize  optimise la production d'energie d'un nombre n de sites d'éoliennes 
    (situés sur terre, onshore, ou en mer, offshore), 
    ces sites sont numérotés de 0 à n-1 (indices correspondant à l'ordre des éléments dans Sites.csv !!!pas à la colonne index!!!),
    et la production est optimisée selon la variabilité estimée des rendements des sites, 
    la puissance totale installable P, 
    la proportion k de la puissance totale devant obligatoirement être attribuée à des sites d'éoliennes se trouvant dans la mer (offshore),
    ainsi que la quantité S maximale d'énergie achetée à l'année (uniquement pour le second modèle).

    Optimize utilise deux fonctions, modele1 et modele2, décrites dans modeles.py.

    Args :
    - ct, numpy array de dimension t, 
    les capacités totales des t sites d'éoliennes se trouvant sur terre (on-shore)
    - cm, numpy array de dimension m, 
    les capacités totales des m sites d'éoliennes se trouvant dans la mer (off-shore)
    - Rt, numpy array de dimensions t x h, 
    la matrice de rendement (pour chaque heure d'une année) des sites d'éoliennes se trouvant sur terre (on-shore)
    - Rm, numpy array de dimensions m x h, 
    la matrice de rendement (pour chaque heure d'une année) des sites d'éoliennes se trouvant en mer (off-shore)
    remarque : ct, cm, Rt, Rm sont supposées extraites des documents Rendements_offshore.csv, Rendements_onshore.csv, Sites.csv, de la partie Data du projet
    ils sont donc supposés non vides
    - P, scalaire, la puissance totale installable,
    - k, scalaire compris entre 0 et 1, la proportion de la puissance totale devant obligatoirement être attribuée à des sites d'éoliennes se trouvant dans la mer (off-shore)

    - modele, entier valant 1 ou 2 (par défaut : 1), décrivant le modèle résolu par optimize 
    (correspondant aux questions 1 et 2 de l'énoncé du projet)
    - S, scalaire (optionnel : par défaut 0), limite sur la quantité d'énergie achetée à l'année (utilisé seulement si modele = 2)

    - checkpoints, optionnel, un booléen (par défaut False)
    if checkpoints == True, la fonction Optimize imprime un ensemble d'indications dans le terminal pour aider au débuggage
    (un peu mochement fait mais utile normalement)

    Returns :
    - res, un tuple comprenant les variables d'intérêt obtenues par la résolution du problème linéaire
    res contient 1 ou 2 arrays en fonction du modele considere :
    pour le modele 1, res = (x)
    pour le modele 2, res = (x,s)
    -- x, vecteur de taille n dont les valeurs sont comprises entre 0 et 1,
    proportion des sites éoliens devant être installés,
    -- s, vecteur de taille h dont les valeurs sont supérieures ou égales à 0,
    quantités d'énergie supplémentaires (de source non éolienne) achetées par heure
    - z, l'objectif
    - sol, un objet de type Solution, contenant des valeurs intéressantes pour l'analyse des résultats
    """

    ## Getting all the sizes
    t = np.size(ct)
    m = np.size(cm)
    h = np.shape(Rt)[1]
    if checkpoints :
        print("Checking sizes, i want all True :", t==np.shape(Rt)[0], m==np.shape(Rm)[0], h==np.shape(Rm)[1])
    n = t + m

    if n==0 :
        print("There are no values to the problem")
        return 0

    ## Constructing the important c, R, A matrices

    # c is the concatenation of ct and cm
    c = np.concatenate((ct, cm))
    # R is the concatenation of Rt and Rm along the "eolien sites" axis
    R = np.concatenate((Rt, Rm))
    if checkpoints :
        print("Checking dimensions : is c ok ? is R ok ?", np.shape(c)==(n,), np.shape(R)==(n,h))
    # A is the line-product of c and R, so that in A, 
    # each "rendement" (as effective capacity/total capacity) is re-multiplied by total capacity
    A = c[:, np.newaxis] * R


    ## Resolution
    if (modele == 1) :
        x,z = modele1(t,m,n,h,ct,cm,c,Rt,Rm,R,A,P,k,checkpoints)
        res = (x)
    
    elif (modele == 2) :
        x,s,z = modele2(t,m,n,h,ct,cm,c,Rt,Rm,R,A,P,k,S,checkpoints)
        res = (x,s)
    
    elif (modele == 3) :
        x,z = modele3(t, m, n, h, ct, cm, c, Rt, Rm, R, A, P, k, delta, T, checkpoints)
        res = (x)

    else :
        print("Argument modele invalide")
    
    ## Computing interesting values
    ## See the Solution class
    E     = np.zeros((h))
    Rm    = np.zeros((h))
    Etot  = 0
    Rmtot = 0

    for j in range (h) :
        E[j]   =  x @ A[:,j]
        Rm[j] = x @ R[:, j]

    if (np.sum(x) != 0) :
        Rm = Rm/np.sum(x)

    Etot = np.sum(E)
    Rmtot = np.sum(Rm)/h

    sol = Solution (Rm, Rmtot, E, Etot)
    
    return res,z,sol
