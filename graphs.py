from matplotlib import pyplot as plt
import numpy as np

def graph_rendements (Rm, nticks=None, scale = 'heures', Rm_name=None) :
    """
    Graphe, affiche (et éventuellement enregistre) l'évolution de Rm, le rendement moyen, en fonction du temps.
    (intended usage : Rm est obtenu dans optimize, computed à partir de data)
    (-> remarque : Rm dépend donc bien de nos variables x après optimisation)
    Si name est donné, l'image est enregistrée sous le nom <name> au format png.

    Args :
    - Rm, numpy array de taille h, évolution du rendement moyen au cours du temps
    - nticks, scalaire (optionnel : par défaut None), nombre d'abscisses à considérer pour les deux graphes
    (si nticks = None, le nombre de graduations est h)
    - scale, chaîne de caractères (optionnel : par défaut 'heures'), indique la légende de l'axe des abscisses pour les deux graphes
    scale prend ses valeurs dans ['heures', 'jours', 'semaines', 'mois']
    - Rm_name (optionnel), le nom sous lequel enregistrer le graphe du rendement moyen en fct du temps

    Returns :
    None
    """
    h = np.size(Rm)

    if (nticks != None) :
    ## Espacement des valeurs (sampling)
        step = h // min(nticks,h)
        plot_hours = np.arange(0,h)[::step]
        plot_Rm = Rm[::step]
    else :
        plot_hours, plot_Rm = np.arange(0,h), Rm

    ## Calibrage de l'axe des abscisses selon l'argument scale
    plot_time = plot_hours
    if (scale == 'jours') :
        plot_time = plot_time/24
    elif (scale == 'semaines') :
        plot_time = plot_time/168
    elif (scale == 'mois') :
        plot_time = plot_time/730
    else :
        print("Argument 'scale' is invalid. Graph is scaled with hours.")

    plt.figure("Rendement moyen de l'ensemble des sites, sur un an")
    plt.plot(plot_time, plot_Rm*100)
    plt.xlabel("temps [{}]".format(scale))
    plt.ylabel("rendement moyen [%]")

    if (Rm_name != None) :
        plt.savefig(Rm_name + '.png', bbox_inches='tight')
    plt.show()


def graph_energy (E, nticks=None, scale='heures', E_name=None) :
    """
    Graphe, affiche (et éventuellement enregistre) l'évolution de E, l'énergie produite, en fonction du temps.
    (intended usage : E est obtenu dans optimize, computed à partir de data)
    (-> remarque : E dépent donc bien de nos variables x après optimisation)
    Si name est donné, l'image est enregistrée sous le nom <name> au format png.

    Args :
    - E, numpy array de taille h, évolution de l'énergie produite au cours du temps
    - nticks, scalaire (optionnel : par défaut None), nombre d'abscisses à considérer pour les deux graphes
    (si nticks = None, le nombre de graduations est h)
    - scale, chaîne de caractères (optionnel : par défaut 'heures'), indique la légende de l'axe des abscisses pour les deux graphes
    scale prend ses valeurs dans ['heures', 'jours', 'semaines', 'mois']
    - E_name (optionnel), le nom sous lequel enregistrer le graphe de l'énergie produite en fct du temps

    Returns :
    None
    """
    h = np.size(E)

    if (nticks != None) :
    ## Espacement des valeurs (sampling)
        step = h // min(nticks,h)
        plot_hours = np.arange(0,h)[::step]
        plot_E = E[::step]
    else :
        plot_hours, plot_E = np.arange(0,h), E

    ## Calibrage de l'axe des abscisses selon l'argument scale
    plot_time = plot_hours
    if (scale == 'jours') :
        plot_time = plot_time/24
    elif (scale == 'semaines') :
        plot_time = plot_time/168
    elif (scale == 'mois') :
        plot_time = plot_time/730
    else :
        print("Argument 'scale' is invalid. Graph is scaled with hours.")

    plt.figure("Energie produite par l'ensemble des sites, sur un an")
    plt.plot(plot_time, plot_E)
    plt.xlabel("temps [{}]".format(scale))
    plt.ylabel("energie produite [MWh]")
    if (E_name != None) :
        plt.savefig(E_name + '.png', bbox_inches='tight')
    plt.show()