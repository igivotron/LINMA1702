from matplotlib import pyplot as plt
import numpy as np

def graph_rendements (Rm, nticks=None, scale = 'heures', name=None) :
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
    - name (optionnel), le nom sous lequel enregistrer le graphe du rendement moyen en fct du temps

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
    if (scale=='heures'):
        pass
    elif (scale == 'jours') :
        plot_time = plot_time/24
    elif (scale == 'semaines') :
        plot_time = plot_time/168
    elif (scale == 'mois') :
        plot_time = plot_time/730
    else :
        print("Argument 'scale' is invalid. Graph is scaled with hours.")

    title = "Rendement moyen de l'ensemble des sites, sur un an"
    plt.figure(title)
    plt.plot(plot_time, plot_Rm*100)
    plt.xlabel("temps [{}]".format(scale))
    plt.ylabel("rendement moyen [%]")
    plt.title(title)

    if (name != None) :
        plt.savefig(name + '.png', bbox_inches='tight')
    plt.show()


def graph_Q1energy (E, nticks=None, scale='heures', name=None) :
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
    - name (optionnel), le nom sous lequel enregistrer le graphe de l'énergie produite en fct du temps

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

    title = "Energie produite par l'ensemble des sites, sur un an"
    plt.figure(title)
    plt.plot(plot_time, plot_E)
    plt.xlabel("temps [{}]".format(scale))
    plt.ylabel("energie produite [MWh]")
    plt.title(title)

    if (name != None) :
        plt.savefig(name + '.png', bbox_inches='tight')
    plt.show()

def graph_Q2energy(E, s, nticks=None, scale='heures', name=None) :
    """
    Graphe, affiche (et éventuellement enregistre) l'évolution de E, l'énergie produite, s, l'énergie achetée, et la somme des deux en fonction du temps.
    (intended usage : E,s sont obtenus dans optimize, computed à partir de data)
    (-> remarque : E dépend donc bien de nos variables x après optimisation ; s est une partie des variables d'optimisation)
    Si name est donné, l'image est enregistrée sous le nom <name> au format png.

    Args :
    - E, numpy array de taille h, évolution de l'énergie produite au cours du temps
    -s, numpy array de taille h, évolution de l'énergie achetée au cours du temps
    - nticks, scalaire (optionnel : par défaut None), nombre d'abscisses à considérer pour les deux graphes
    (si nticks = None, le nombre de graduations est h)
    - scale, chaîne de caractères (optionnel : par défaut 'heures'), indique la légende de l'axe des abscisses pour les deux graphes
    scale prend ses valeurs dans ['heures', 'jours', 'semaines', 'mois']
    - name (optionnel), le nom sous lequel enregistrer le graphe de l'énergie produite en fct du temps

    Returns :
    None
    """
    h = np.size(E)

    if (np.size(s) != h) :
        print("Taille des arguments invalides. Taille de E = {}, taille de s = {}. Le graphe n'a pas pu etre créé.".format(h,np.size(s)))

    if (nticks != None) :
    ## Espacement des valeurs (sampling)
        step = h // min(nticks,h)
        plot_hours = np.arange(0,h)[::step]
        plot_E = E[::step]
        plot_s = s[::step]
    else :
        plot_hours, plot_E, plot_s = np.arange(0,h), E, s

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

    title = "Energie produite et achetée sur un an"
    plt.figure(title)

    plt.plot(plot_time,plot_E,'blue',label='Energie produite')
    plt.plot(plot_time,plot_s,'green',label='Energie achetee')
    plt.plot(plot_time,plot_E+plot_s,'red',label='Energie totale')  

    plt.xlabel("temps [{}]".format(scale))
    plt.ylabel("energie [MWh]")
    plt.legend()
    plt.title(title)

    if (name != None) :
        plt.savefig(name + '.png', bbox_inches='tight')
    plt.show()   


def graph_comparison (Edisp1, Edisp2, x1, x2, nticks=None, scale='heures', name=None, modeles=(1,2)) :
        
    h = np.size(Edisp1)

    if (nticks != None) :
    ## Espacement des valeurs (sampling)
        step = h // min(nticks,h)
        plot_hours = np.arange(0,h)[::step]
        plot_Edisp1 = Edisp1[::step]
        plot_Edisp2 = Edisp2[::step]
    else :
        plot_hours, plot_Edisp1, plot_Edisp2 = np.arange(0,h), Edisp1, Edisp2

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

    plt.figure("Comparaison des deux modèles au niveau des sites éoliens installés et des énergies produites")

    plt.subplot(2,1,1)
    plt.title("Energie disponible au cours de l'année pour les deux modèles")
    plt.plot(plot_time, plot_Edisp1, label="modele {}".format(modeles[0]))
    plt.plot(plot_time, plot_Edisp2, label="modele {}".format(modeles[1]))
    plt.xlabel("temps [{}]".format(scale))
    plt.ylabel("energie disponible [MWh]")
    plt.legend()

    plt.subplot(2,1,2)
    plt.title("Différence en portions des sites installés pour les deux modèles (x{} - x {})".format(modeles[0],modeles[1]))
    plt.stem(np.arange(0,np.size(x1)), (x1-x2)*100, linefmt='C0:', markerfmt='C0.', basefmt='C0', label="diff")
    plt.xlabel("indice des sites [-]")
    plt.ylabel("portion installee [%]")
    plt.legend()

    plt.subplots_adjust(hspace=0.5)

    if (name != None) :
        plt.savefig(name + '.png', bbox_inches='tight')
    plt.show()
