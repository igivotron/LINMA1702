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


def modele2 (t, m, n, h, ct, cm, c, Rt, Rm, R, A, P, k, S, checkpoints) :
    """
    modele2 est un enfant d'optimize

    Args :
    valeurs propres au problème telles que décrites / construites dans optimize
    
    Returns :
    - x, numpy array de taille n, les proportions de chaque site d'éoliennes qui seront installées,
    - s, numpy array de taille h, les quantités achetées pour chaque heure,
    - z, scalaire, la fonction objectif, minimum des productions d'énergie sur toutes les periodes d'une heure
    
    """
    ## Constructing all the matrices of use for linprog
    ## v are the variables linprog will give us in return, v = (x|s|z)
    ## size of v : n + h + 1
    ## fun is the optimized objective linprog will give us in return
    ## A_ub @ v <= b_ub
    ## A_eq @ v == b_eq
    ## min (coeff @ v) = -max (-coeff @ v)

    ## max (min (x@aj)) = max z ; z <= x@aj
    ## where aj is a column of A, of size n
    ## there are h values for x@aj and we want to maximize the smaller one (z)
    
    # Contraintes d'inégalité (A_ub, b_ub) :
    # 0 <= x <= 1 pour tout x
    # z <= (aj)^Tx + sj pour tout aj colonne de A ; sj element de s
    # 0 <= s pour tout s
    # sum(sj) <= S

    # Traduit en 
    #  xi <= 1
    # -xi <= 0
    #  -(aj)^T@x - sj + z <= 0
    # -sj <= 0 
    # sum(sj) <= S

    # b_ub est de taille 2*n + 2*h + 1
    # A_ub est de dimensions (2n+2h+1,n+h+1)

    In = np.identity(n)
    A_ub1 = np.concatenate((In,-In))
    if checkpoints :
        print("Checking construction of A_ub : for now, is A_ub1 shape correct ?", np.shape(A_ub1)==(2*n, n))
    A_ub1 = np.concatenate((A_ub1, np.zeros((2*n,h+1))), axis = 1)
    if checkpoints :
        print("Checking construction of A_ub : is A_ub1 shape correct ?", np.shape(A_ub1)==(2*n, n+h+1))
    A_ub2 = np.concatenate((-np.transpose(A), -np.identity(h), np.ones((h))[:, np.newaxis]), axis = 1)
    if checkpoints :
        print("Checking construction of A_ub : is A_ub2 shape correct ?", np.shape(A_ub2)==(h, n+h+1))
    A_ub3 = np.concatenate((np.zeros((h,n)),-np.identity(h),np.zeros((h,1))), axis=1)
    if checkpoints :
        print("Checking construction of A_ub : is A_ub3 shape correct ?", np.shape(A_ub3)==(h,n+h+1))
    A_ub4 = np.concatenate((np.zeros((1,n)),np.ones((1,h)),np.zeros((1,1))), axis = 1)
    if checkpoints :
        print("Checking construction of A_ub : is A_ub4 shape correct ?", np.shape(A_ub4)==(1,n+h+1))
    A_ub = np.concatenate((A_ub1, A_ub2, A_ub3, A_ub4))
    if checkpoints :
        print("Checking construction of A_ub : is A_ub shape correct ?", np.shape(A_ub)==(2*n+2*h+1, n+h+1))
    b_ub = np.concatenate((np.ones((n)),np.zeros((n+2*h)),S*np.ones((1))))
    if checkpoints :
        print("Checking construction of b_ub : is b_ub shape correct ?", np.shape(b_ub)==(2*n+2*h+1,))

    
    # Contraintes d'égalité (A_eq, b_eq)
    # c @ x = P
    # cm @ xm = kP
    
    b_eq = np.array([P, k*P])
    A_eq1 = np.concatenate((c,np.zeros((h+1))))
    A_eq2 = np.concatenate((np.zeros((t)), cm))
    A_eq2 = np.concatenate((A_eq2, np.zeros((h+1))))
    A_eq = np.array([A_eq1, A_eq2])
    if checkpoints :
        print("Checking construction of A_eq : is A_eq shape correct ?", np.shape(A_eq)==(2,n+h+1))
    
    coeffs = np.concatenate((np.zeros((n+h)), np.array([-1])))
    if checkpoints :
        print("Checking construction of coeffs : is coeffs shape correct ?", np.shape(coeffs)==(n+h+1,))

    ## Calling linprog
    res = linprog(coeffs, A_ub, b_ub, A_eq, b_eq)

    if (res.success != True) :
        # TODO : gestion du probleme
        print("There was a trouble with the usage of linprog : the problem could not be optimized")
        print(res.message)
    
    v = res.x
    z = -res.fun
    x = v[0:n]
    s = v[n:n+h]

    if checkpoints :
        print("Checking : is x the correct size ?", len(x)==n)
        print("Checking : is s the correct size ?", len(s)==h)
        print("Sanity check : as z is the last variable and the objective for linprog, is z equal to v[-1] ?", z == v[-1])
        print("Sanity check : is the production c @ x equal to the argument P ?", abs(c@x-P)<1e-9)
        print("Sanity check : is the off-shore production cm @ xm equal to k*P ?", abs(cm@x[t:n]-k*P)<1e-9)
        print("Sanity check : is the sum of the buyings inferior to S ?", S-np.sum(s)<=1e-9)
        boundcheck = True
        for i in range (n) :
            if (x[i]<0) or (x[i]>1) :
                boundcheck = False
        print("Sanity check : are all x's taking values between 0 and 1 ?", boundcheck)
        sboundcheck = True
        for j in range (h) :
            if (s[j] < 0) :
                sboundcheck = False
        print("Sanity check : are all s's positive ?", sboundcheck)
        mincheck = True
        for i in range (h) :
            if ( z - A[:,i]@x - s[i] > 1e-9 ) :
                mincheck = False
        print("Sanity check : is z the minimum of production + buying for all hours ?", mincheck)

    return x,s,z