from matplotlib import pyplot as plt
import numpy as np

def graph (h, Rm, E, Rm_name=None, E_name=None) :
    """
    Graphe, affiche (et éventuellement enregistre) les évolutions de Rm, le rendement moyen, et E, l'énergie produite, en fonction du temps.
    (intended usage : Rm et E sont obtenus dans optimize, computed à partir de data)
    (-> remarque : Rm et E dépendent donc bien de nos variables x après optimisation)
    Si name est donné, l'image est enregistrée sous le nom <name> au format png.

    Args :
    - h, scalaire, le nombre de périodes (d'une heure) considérées
    - Rm, numpy array de taille h, évolution du rendement moyen au cours du temps
    - E, numpy array de taille h, évolution de l'énergie produite au cours du temps
    - Rm_name, le nom sous lequel enregistrer le graphe du rendement moyen en fct du temps
    - E_name, le nom sous lequel enregistrer le graphe de l'énergie produite en fct du temps

    Returns :
    None
    """
    if (h != Rm.size() or h != E.size()) :
        print("Problème de format. La production des graphes a échoué.")

    plt.figure("Rendement moyen de l'ensemble des sites, sur un an")
    plt.plot(h, Rm)
    plt.xlabel("temps [h]")
    plt.ylabel("rendement moyen [-]")
    plt.show()
    if (Rm_name != None) :
        plt.savefig(Rm_name + '.png', bbox_inches='tight')

    plt.figure("Energie produite par l'ensemble des sites, sur un an")
    plt.plot(h, E)
    plt.xlabel("temps [h]")
    plt.ylabel("energie produite [MWh]")
    plt.show()
    if (E_name != None) :
        plt.savefig(E_name + '.png', bbox_inches='tight')