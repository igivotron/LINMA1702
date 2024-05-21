import matplotlib.pyplot as plt
import numpy as np

def print_values_get_prixmoy(prix_total, e_eolienne_produite, apports_naturels, demande_totale, e_gaz_produite=0) :

    prix_moyen = prix_total/demande_totale
    perte = e_eolienne_produite + apports_naturels + e_gaz_produite - demande_totale

    print("Energie éolienne produite    : {:.2f} MWh".format(e_eolienne_produite))
    print("Apports naturels             : {:.2f} MWh".format(apports_naturels))
    print("Energie (gaz) produite       : {:.2f} MWh".format(e_gaz_produite))
    print("Total                        : {:.2f} MWh".format(e_eolienne_produite + apports_naturels + e_gaz_produite))
    print("Demande totale satisfaite    : {:.2f} MWh".format(demande_totale))
    print("\n")
    print("Prix total                   : {:.2f} euros".format(prix_total))
    print("Prix moyen                   : {:.2f} euros/MWh".format(prix_moyen))
    return prix_moyen


def lissage(array, depth) :
    n = np.size(array)
    m = n//depth
    new_array = np.zeros(m)
    for i in range (m) :
        for j in range (depth) :
            new_array[i] += (array[depth*i + j]/depth)
    return new_array


def occupation_bassin(t, s, wA, wP, wT) :

    L = np.tril(np.ones((t,t)))

    # Utilisation de la fonction de lissage et profondeur de lissage
    bool_lissage = True
    if t <= 300 :
        bool_lissage = False
    depth = 50

    # Hardcodé : réduction de l'échelle de l'énergie
    fact = 1e6
    strfact = '1e6'

    Wmin = -0.5*s*np.ones((t))
    Wmax = 0.5*s*np.ones((t))

    plt.figure()
    plt.title("Occupation du bassin et apports naturels")

    ax1 = plt.subplot()
    ax1.plot(np.arange(t), Wmin/fact, label="Limites de stockage", color='black', linestyle='dashdot', linewidth=0.5)
    ax1.plot(np.arange(t), Wmax/fact, color='black', linestyle='dashdot', linewidth=0.5)
    ax1.plot(np.arange(t), L@(wA + wP - wT)/fact, 'black')
    ax1.set_xlabel("Nombre de périodes [-]")
    ax1.set_ylabel("Occupation du bassin [{} MWh]".format(strfact), color='black')

    ax2 = ax1.twinx()
    ax2.plot(np.arange(t), wA/fact, 'b')
    ax2.set_ylabel("Apports naturels [{} MWh]".format(strfact), color='b')

    plt.show()

    plt.figure()
    plt.title("Quantités d'énergie hydroélectrique pompées et turbinées")

    ax1 = plt.subplot()
    if bool_lissage :
        ax1.plot(np.arange(t), wP/fact, '-.g', linewidth=0.1)
        ax1.plot(np.arange(0,t-depth,depth), lissage(wP,depth)/fact, 'g')
    else :
        ax1.plot(np.arange(t), wP/fact, 'g')
    ax1.set_ylabel("Quantité pompée [{} MWh]".format(strfact), color='g')

    ax2 = ax1.twinx()
    if bool_lissage :
        ax2.plot(np.arange(t), wT/fact, '-.y', linewidth=0.1)
        ax2.plot(np.arange(0,t-depth,depth), lissage(wT,depth)/fact, 'y')
    else :
        ax2.plot(np.arange(t), wT/fact, 'y')
    ax2.set_ylabel("Quantité turbinée [{} MWh]".format(strfact), color='y')
    ax2.set_xlabel("Nombre de périodes [-]")

    plt.show()


def sources_eng(t, e, wP, wT_dim, d, epg=None) :

    try :
        if (epg==None) :
            epg = np.zeros((t,1))
    except :
        pass

    L = np.tril(np.ones((t,t)))

    # Lissage
    bool_lissage = True
    if t <= 300 :
        bool_lissage = False
    depth = 50

    # Echelle energie
    fact = 1e6
    strfact = '1e6'

    plt.figure()

    if bool_lissage :
        plt.plot(np.arange(t), e/fact, '-.r', linewidth=0.1)
        plt.plot(np.arange(0,t-depth,depth), lissage(e,depth)/fact, 'r', label="Energie éolienne produite")

        plt.plot(np.arange(t), epg/fact, 'black', linewidth=0.1, linestyle='dashdot')
        plt.plot(np.arange(0,t-depth,depth), lissage(epg,depth)/fact, 'black', label="Energie au gaz produite")
        
        plt.plot(np.arange(t), (e - wP + wT_dim + epg)/fact, '-.b', linewidth=0.1)
        plt.plot(np.arange(0,t-depth,depth), lissage((e - wP + wT_dim + epg),depth)/fact, 'b', label="Energie employée")

    else :
        plt.plot(np.arange(t), e/fact, 'r', label="Energie éolienne produite")
        plt.plot(np.arange(t), epg/fact, 'black', label="Energie au gaz produite")
        plt.plot(np.arange(t), (e - wP + wT_dim + epg)/fact, 'b', label="Energie employée")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie [{} MWh]".format(strfact))
    plt.legend()
    plt.show()

    plt.figure()
    
    plt.plot(np.arange(t), L@e/fact, 'r', label="Energie éolienne cumulée")
    plt.plot(np.arange(t), L@epg/fact, 'black', label="Energie au gaz cumulée")
    plt.plot(np.arange(t), L@(e - wP + wT_dim + epg)/fact, 'b', label="Energie employée cumulée")
    plt.plot(np.arange(t), L@d/fact, '--b', label="Demande cumulée")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie [{} MWh]".format(strfact))
    plt.legend()

    plt.plot()

