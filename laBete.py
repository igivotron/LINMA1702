import numpy as np

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
    # E : matrice pour faire la différence entre colonnes successives
    E = np.eye(P.shape[1], P.shape[1]-1, k=-1) - np.eye(P.shape[1], P.shape[1]-1)
    # F : matrice Ak+1 - Ak
    F = np.dot(P, E)
    # G : matrice Ak - Ak+1
    G = np.dot(P, -E)
    # U: matrice addition toutes les heures
    U = np.ones((P.shape[1], 1))
    # V : matrice production éolienne totale
    V = np.dot(P, U)

    print("Matrice effective")
    print(A)
    print("Production par période P")
    print(P)
    print("Ak+1 - Ak")
    print(F)
    print("Ak - Ak+1")
    print(G)
    print("matrice addition toutes les heures")
    print(V)
    return V, F.T, G.T

R = np.array([[1, 2, 3, 5, 4, 2], [4, 5, 6, 7, 4, 3], [7, 8, 9, 9, 8, 5], [4, 5, 8, 8, 5, 4]])
c = np.array([10, 8, 12, 12])
x = np.array([1, 1, 1, 1])

V, F, G= mod3ContSup(R, c, 1)


X = np.dot(F, x)

