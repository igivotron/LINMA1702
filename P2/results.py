import matplotlib.pyplot as plt
import numpy as np

def print_values_get_prixmoy(prix_total, e_eolienne_produite, apports_naturels, demande_totale, e_gaz_produite=0) :

    prix_moyen = prix_total/(e_eolienne_produite + apports_naturels + e_gaz_produite)
    perte = e_eolienne_produite + apports_naturels + e_gaz_produite - demande_totale

    print("Energie éolienne produite, {:.2f} MWh".format(e_eolienne_produite))
    print("Apports naturels         , {:.2f} MWh".format(apports_naturels))
    print("Energie (gaz) produite   , {:.2f} MWh".format(e_gaz_produite))
    print("Total                    , {:.2f} MWh".format(e_eolienne_produite + apports_naturels + e_gaz_produite))
    print("Demande totale satisfaite, {:.2f} MWh".format(demande_totale))
    print("\n")
    print("Prix total, {:.2f} euros".format(prix_total))
    print("Prix moyen, {:.2f} euros/MWh".format(prix_moyen))
    return prix_moyen


def occupation_bassin(t, s, wA, wP, wT) :

    plt.figure()

    L = np.tril(np.ones((t,t)))
    nticks = 100
    step=min(nticks,t)

    time = np.arange(0,t,1)

    Wmin = -0.5*s*np.ones((t))
    Wmax = 0.5*s*np.ones((t))

    plt.plot(time, Wmin, 'r', label="Limites de stockage")
    plt.plot(time, Wmax, 'r')
    plt.plot(time, L@wA, 'b', label="Apports naturels cumulés")
    plt.plot(time, L@wP, 'g', label="Entrées cumulées")
    plt.plot(time, -L@wT, 'y', label="Sorties cumulées")
    plt.plot(time, L@(wA + wP - wT), 'black', label="Occupation du bassin")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie stockée [MWh]")
    plt.title("Occupation du bassin autour de son remplissage initial")
    plt.legend()
    plt.show()


def sources_eng(t, e, wP, wT_dim, d, epg=None) :

    try :
        if (epg==None) :
            epg = np.zeros((t,1))
    except :
        pass

    L = np.tril(np.ones((t,t)))

    plt.figure()

    time = np.arange(0,t,1)
    plt.plot(time, e, 'r', label="Energie éolienne produite")
    plt.plot(time, -wP, 'g', label="Energie pompée (stockée)")
    plt.plot(time, wT_dim, 'y', label="Energie hydroélectrique turbinée")
    plt.plot(time, epg, 'black', label="Energie au gaz produite")
    plt.plot(time, e - wP + wT_dim + epg, 'b', label="Energie employée")
    plt.plot(time, d, '--b', label="Demande")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie produite [MWh]")
    plt.legend()
    plt.plot()
    
    plt.figure()

    time = np.arange(0,t,1)
    plt.plot(time, L@e, 'r', label="Energie éolienne produite")
    plt.plot(time, -L@wP, 'g', label="Energie pompée (stockée)")
    plt.plot(time, L@wT_dim, 'y', label="Energie hydroélectrique turbinée")
    plt.plot(time, L@epg, 'black', label="Energie au gaz produite")
    plt.plot(time, L@(e - wP + wT_dim + epg), 'b', label="Energie employée")
    plt.plot(time, L@d, '--b', label="Demande")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie produite cumulée [MWh]")
    plt.legend()
    plt.plot()

