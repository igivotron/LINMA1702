import numpy as np
from scipy.optimize import linprog

def modele1 (t, m, n, h, ct, cm, c, Rt, Rm, R, A, P, k, checkpoints) :
    """
    modele1 est un enfant d'optimize

    Args :
    valeurs propres au problème telles que décrites / construites dans optimize
    
    Returns :
    - x, numpy array de taille n, les proportions de chaque site d'éoliennes qui seront installées,
    - z, scalaire, la fonction objectif, minimum des productions d'énergie sur toutes les periodes d'une heure
    
    """
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

    return x,z
def mod3ContSup(R, c, T):
    A = np.zeros(R.shape)
    for i in range(len(c)):
        A[i] = c[i] * R[i]
    # p : nombre de période et reste
    p = A.shape[1] // T
    r = A.shape[1] % T
    # On coupe la matrice car sinon il n'y a pas assez de données de remplir la dernière période
    if r != 0:
        A = A[:, :-r]
    # C :matrice pour additionner les productions d'une période
    C = np.zeros((A.shape[1], p))
    for i in range(p):
        C[i * T:(i + 1) * T, i] = 1
    # P : matrice de production par période
    P = np.dot(A, C)
    # B : matrice pour calculer les différences de productions entre période successive
    B = np.eye(p, p - 1, k=-1) - np.eye(p, p - 1)
    # D : matrice des deltaP
    D = np.dot(P, B)
    # E : matrice pour faire la différence entre colonnes successives
    E = np.eye(D.shape[1], D.shape[0]+1, k=-1) - np.eye(D.shape[1], D.shape[0]+1)
    # F : matrice Ak+1 - Ak
    F = np.dot(D, E)
    # G : matrice Ak - Ak+1
    G = np.dot(D, -E)
    # U: matrice addition toutes les heures
    U = np.ones((P.shape[1], 1))
    # V : matrice production éolienne totale
    V = np.dot(P, U)

    return V[:,0], F.T, G.T

def modele3(t, m, n, h, ct, cm, c, Rt, Rm, R, A, P, k, delta, T, checkpoints):
    """
    modele2 est un gros copié collé de modèle1

    Args :
    valeurs propres au problème telles que décrites / construites dans optimize

    Returns :
    - x, numpy array de taille n, les proportions de chaque site d'éoliennes qui seront installées,
    - z, scalaire, la fonction objectif, minimum des productions d'énergie sur toutes les periodes d'une heure

    """
    ## Constructing all the matrices of use for linprog
    ## v are the variables linprog will give us in return, v = (x|d|z)
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
    A_ub1 = np.concatenate((In, -In))
    V, F, G = mod3ContSup(R, c, T)
    m = F.shape[0] #p-1



    A_ub1 = np.concatenate((A_ub1, np.zeros((A_ub1.shape[0], m))), axis=1)
    A_ub2 = np.concatenate((F,-np.identity(F.shape[0])), axis=1)
    A_ub3 = np.concatenate((G,-np.identity(G.shape[0])), axis=1)
    A_ub4 = np.concatenate((np.zeros((1,n)), np.ones((1,m))), axis=1)
    A_ub = np.concatenate((A_ub1, A_ub2, A_ub3, A_ub4))

    b_ub1 = np.ones((n))
    b_ub2 = np.zeros((n))
    b_ub3 = np.zeros((2*m))
    b_ub4 = np.array([delta*T*P*m])
    b_ub = np.concatenate((b_ub1, b_ub2, b_ub3, b_ub4))

    # Contraintes d'égalité (A_eq, b_eq)
    # c @ x = P
    # cm @ xm = kP

    b_eq = np.array([P, k * P])
    A_eq1 = np.concatenate((c, np.zeros((m))))
    A_eq2 = np.concatenate((np.zeros((t)), cm, np.zeros((m))))
    A_eq = np.array([A_eq1, A_eq2])

    coeffs = -np.concatenate((V, np.zeros((m))))


    ## Calling linprog
    res = linprog(coeffs, A_ub, b_ub, A_eq, b_eq)

    if (res.success != True):
        # TODO : gestion du probleme
        print("There was a trouble with the usage of linprog : the problem could not be optimized")
        print(res.message)

    print(res)
    v = res.x
    z = -res.fun
    x = v[0:n]

    if checkpoints:
        print("Checking : is x the correct size ?", len(x) == n)
        print("Sanity check : as z is the last variable and the objective for linprog, is z equal to v[-1] ?",
              z == v[-1])
        print("Sanity check : is the production c @ x equal to the argument P ?", abs(c @ x - P) < 1e-9)
        print("Sanity check : is the off-shore production cm @ xm equal to k*P ?", abs(cm @ x[t:n] - k * P) < 1e-9)
        boundcheck = True
        for i in range(n):
            if (x[i] < 0) or (x[i] > 1):
                boundcheck = False
        print("Sanity check : are all x's taking values between 0 and 1 ?", boundcheck)
        mincheck = True
        for i in range(h):
            if (z - A[:, i] @ x > 1e-9):
                mincheck = False
        print("Sanity check : is z the minimum of production for all hours ?", mincheck)
    return x, z
