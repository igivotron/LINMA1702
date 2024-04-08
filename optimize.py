import numpy as np
from scipy.optimize import linprog

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

def optimize (ct, cm, Rt, Rm, P, k, checkpoints = False) :
    """
    Optimize est une fonction qui optimise la production d'energie d'un nombre n de sites d'éoliennes 
    (situés sur terre, on-shore, ou en mer, off-shore), 
    ces sites sont numérotés de 0 à n-1 
    (indices correspondant à l'ordre des éléments dans Sites.csv !!!pas à la colonne index!!!),
    et la production est optimisée selon la variabilité estimée des rendements des sites, 
    la puissance totale installable P, 
    et la proportion k de la puissance totale devant obligatoirement être attribuée à des sites d'éoliennes se trouvant dans la mer (off-shore).
    
    Optimize renvoie x, les proportions de chaque site d'éoliennes qui seront installées,
    et z, la fonction objectif telle que définie plus bas.

    TODO : définir z de manière compréhensible. 

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

    - checkpoints, optionnel, un booléen (par défaut False)
    if checkpoints == True, la fonction Optimize imprime un ensemble d'indications dans le terminal pour aider au débuggage
    (un peu mochement fait mais utile normalement)

    Returns :
    - x, un vecteur de taille n dont les valeurs sont comprises entre 0 et 1,
    proportion des sites d'éoliennes devant être installées,
    - z, l'objectif
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


    ## Constructing all the matrices of use for linprog
    ## v are the variables linprog will give us in return, v = (x|z)
    ## z is the optimized objective linprog will give us in return
    ## A_ub @ v <= b_ub
    ## A_eq @ v == b_eq

    ## max (min (x@aj)) = max z ; z <= x@aj
    ## where aj is a column of A, of size n
    ## there are h values for x@aj and we want to maximize the smaller one (z)

    
    # Contraintes d'inégalité (A_ub, b_ub) :
    # 0 <= x <= 1 pour tout x
    # z <= (aj)Tx pour tout aj colonne de A

    In = np.identity(n)
    A_ub1 = np.concatenate((In,-In))
    if checkpoints :
        print("Checking construction of A_ub : for now, is A_ub1 shape correct ?", np.shape(A_ub1)==(2*n, n))
    A_ub1 = np.concatenate((A_ub1, np.zeros((2*n))[:, np.newaxis]), axis = 1)
    if checkpoints :
        print("Checking construction of A_ub : is A_ub1 shape correct ?", np.shape(A_ub1)==(2*n, n+1))
    A_ub2 = np.concatenate((-np.transpose(A), np.ones((h))[:, np.newaxis]), axis = 1)
    if checkpoints :
        print("Checking construction of A_ub : is A_ub2 shape correct ?", np.shape(A_ub2)==(h, n+1))
    A_ub = np.concatenate((A_ub1, A_ub2))
    if checkpoints :
        print("Checking construction of A_ub : is A_ub shape correct ?", np.shape(A_ub)==(2*n+h, n+1))
    b_ub = np.concatenate((np.ones((n)),np.zeros((n+h))))
    if checkpoints :
        print("Checking construction of b_ub : is b_ub shape correct ?", np.shape(b_ub)==(2*n+h,))

    
    # Contraintes d'égalité (A_eq, b_eq)
    # c @ x = P
    # cm @ xm = kP
    
    b_eq = np.array([P, k*P])
    A_eq1 = np.concatenate((c,np.zeros((1))))
    A_eq2 = np.concatenate((np.zeros((t)), cm))
    A_eq2 = np.concatenate((A_eq2, np.zeros((1))))
    A_eq = np.array([A_eq1, A_eq2])
    if checkpoints :
        print("Checking construction of A_eq : is A_eq shape correct ?", np.shape(A_eq)==(2,n+1))
    
    coeffs = np.concatenate((np.zeros((n)), np.array([-1])))
    if checkpoints :
        print("Checking construction of coeffs : is coeffs shape correct ?", np.shape(coeffs)==(n+1,))

    
    ## Calling linprog
    res = linprog(coeffs, A_ub, b_ub, A_eq, b_eq)

    if (res.success != True) :
        # TODO : gestion du probleme
        print("There was a trouble with the usage of linprog : the problem could not be optimized")
        print(res.message)
    
    v = res.x
    z = -res.fun
    x = v[0:n]
    if checkpoints :
        print("Checking : is x the correct size ?", len(x)==n)
        print("Sanity check : as z is the last variable and the objective for linprog, is z equal to v[-1] ?", z == v[-1])
        print("Sanity check : is the production c @ x equal to the argument P ?", abs(c@x-P)<1e-9)
        print("Sanity check : is the off-shore production cm @ xm equal to k*P ?", abs(cm@x[t:n]-k*P)<1e-9)
        boundcheck = True
        for i in range (n) :
            if (x[i]<0) or (x[i]>1) :
                boundcheck = False
        print("Sanity check : are all x's taking values between 0 and 1 ?", boundcheck)
        mincheck = True
        for i in range (h) :
            if ( z - A[:,i]@x > 1e-9 ) :
                mincheck = False
        print("Sanity check : is z the minimum of production for all hours ?", mincheck)
    
    ## Computing interesting values
    ## See the Solution class
    E     = np.zeros((h))
    Rm    = np.zeros((h))
    Etot  = 0
    Rmtot = 0

    for j in range (h) :
        E[j]   =  x @ A[:,j]
        Rm[j]  =  x @ R[:,j]
        Etot  +=  E[j]
        Rmtot +=  Rm[j]

    sol = Solution (Rm, Rmtot, E, Etot)
    
    return z,x,sol