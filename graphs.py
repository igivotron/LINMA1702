from matplotlib import pyplot as plt
import numpy as np

def graph (Rm, E, Rm_name=None, E_name=None, nticks=None) :
    """
    Graphe, affiche (et éventuellement enregistre) les évolutions de Rm, le rendement moyen, et E, l'énergie produite, en fonction du temps.
    (intended usage : Rm et E sont obtenus dans optimize, computed à partir de data)
    (-> remarque : Rm et E dépendent donc bien de nos variables x après optimisation)
    Si name est donné, l'image est enregistrée sous le nom <name> au format png.

    Args :
    - Rm, numpy array de taille h, évolution du rendement moyen au cours du temps
    - E, numpy array de taille h, évolution de l'énergie produite au cours du temps
    - ticks, scalaire (optionnel), nombre de graduations à considérer pour l'axe des abscisses des deux graphes
    (si ticks = None, le nombre de graduations est h)
    - Rm_name (optionnel), le nom sous lequel enregistrer le graphe du rendement moyen en fct du temps
    - E_name (optionnel), le nom sous lequel enregistrer le graphe de l'énergie produite en fct du temps

    Returns :
    None
    """
    h = np.size(Rm)

    if (nticks != None) :
    ## Espacement des valeurs (sampling)
        step = h // nticks
        plot_hours = np.arange(0,h)[::step]
        plot_Rm = Rm[::step]
        plot_E = E[::step]
    else :
        plot_hours, plot_Rm, plot_E = np.arange(0,h), Rm, E

    if (h != E.size) :
        print("Problème de format. La production des graphes a échoué.")

    plt.figure("Rendement moyen de l'ensemble des sites, sur un an, en pourcents")
    plt.plot(plot_hours, plot_Rm*100)
    plt.xlabel("temps [h]")
    plt.ylabel("rendement moyen [%]")
    plt.show()
    if (Rm_name != None) :
        plt.savefig(Rm_name + '.png', bbox_inches='tight')

    plt.figure("Energie produite par l'ensemble des sites, sur un an")
    plt.plot(plot_hours, plot_E)
    plt.xlabel("temps [h]")
    plt.ylabel("energie produite [MWh]")
    plt.show()
    if (E_name != None) :
        plt.savefig(E_name + '.png', bbox_inches='tight')