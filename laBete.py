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
    # D : matrice des deltaP
    D = np.dot(P, B)
    # E : matrice pour faire la différence entre colonnes successives
    E = np.eye(D.shape[1], D.shape[0]+1, k=-1) - np.eye(D.shape[1], D.shape[0]+1)
    # F : matrice Ak+1 - Ak
    F = np.dot(D, E)
    # G : matrice Ak - Ak+1
    G = np.dot(D, -E)

    # print("Matrice effective")
    # print(A)
    # print("Production par période P")
    # print(P)
    # print("Différences de production entre périodes successives")
    # print(D)
    # print("Ak+1 - Ak")
    # print(F.T)
    # print("Ak - Ak+1")
    # print(G.T)
    return F.T, G.T

R = np.array([[1, 2, 3, 5, 4, 2], [4, 5, 6, 7, 4, 3], [7, 8, 9, 9, 8, 5], [4, 5, 8, 8, 5, 4]])
c = np.array([10, 8, 12, 12])
x = np.array([1, 1, 1, 1])

F, G= mod3ContSup(R, c, 1)


