import matplotlib.pyplot as plt
import numpy as np

def print_values(prix_total, e_eolienne_produite, apports_naturels, demande_totale, e_gaz_produite=0) :

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


def occupation_bassin(t, s, wA, wP, sorties) :

    plt.figure()

    L = np.tril(np.ones((t,t)))

    time = np.arange(0,t,1)

    min = -0.5*s*np.ones((t))
    max = 0.5*s*np.ones((t))

    plt.plot(time, min, 'r', label="Limites de stockage")
    plt.plot(time, max, 'r')
    plt.plot(time, L@wA, 'b', label="Apports naturels cumulés")
    plt.plot(time, L@wP, 'g', label="Entrées cumulées")
    plt.plot(time, -L@sorties, 'y', label="Sorties cumulées")
    plt.plot(time, L@(wA + wP - sorties), 'black', label="Occupation du bassin")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie stockée [MWh]")
    plt.title("Occupation du bassin autour de son remplissage initial")
    plt.legend()
    plt.show()


def sources_eng(t, e, wP, wT, d, epg=None) :

    try :
        if (epg==None) :
            epg = np.zeros((t,1))
    except :
        pass

    plt.figure()

    time = np.arange(0,t,1)
    plt.plot(time, e, 'r', label="Energie éolienne produite")
    plt.plot(time, -wP, 'g', label="Energie pompée (stockée)")
    plt.plot(time, wT, 'y', label="Energie hydroélectrique turbinée")
    plt.plot(time, epg, 'black', label="Energie au gaz produite")
    plt.plot(time, e - wP + wT + epg, 'b', label="Energie employée")
    plt.plot(time, d, '--b', label="Demande")

    plt.xlabel("Nombre de periodes [-]")
    plt.ylabel("Energie produite [MWh]")
    plt.legend()
    plt.plot()