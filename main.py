import extract_data as ext
from optimize import optimize
from plotMap import plotMap
from graphs import graph

import numpy as np ## pourra etre retiré lorsque np ne sera plus employe


if __name__ == '__main__':
    sites_file = "Data-partie-1/Sites.csv"
    onshore_file = "Data-partie-1/Rendements_onshore.csv"
    offshore_file = "Data-partie-1/Rendements_offshore.csv"

    data = ext.ExtractData(sites_file, onshore_file, offshore_file)

    onshore_capa = data.onshore_capacities()
    offshore_capa = data.offshore_capacities()
    onshore_rend = data.onshore_rendements()
    offshore_rend = data.offshore_rendements()

    P, k = 10000, 0.4

    print("Valeurs utilisées : P = {} ; k = {}".format(P,k))
    
    print("Resolution du probleme lineaire...")
    z, x, sol = optimize(onshore_capa, offshore_capa, onshore_rend, offshore_rend, P, k)

    print("Affichage des sites concernés sur une carte de l'Europe...")
    plotMap(data, x)

    ##
    print("Vecteur de solutions x : {}".format(x))
    print(np.nonzero(x))
    ## A retirer d'apres moi (peut-on faire les checks de maniere interne et ne pas encombrer le main ? :))

    print("Minimum de l'énergie produite en une heure, ou fonction objectif : {} MWh".format(z))

    print("Affichage des graphes du rendement moyen et de l'énergie produite en fonction du temps...")
    graph(sol.Rm, sol.E, 
          nticks = 10000,
          scale = 'mois',
          E_name = "graphe-eng",
          Rm_name = "graphe-rendement")

    print("Rendement moyen sur l'année : {} %".format(sol.Rmtot*100))
    print("Energie produite en un an : {} MWh".format(sol.Etot))


