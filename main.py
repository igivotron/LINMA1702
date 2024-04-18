import extract_data as ext
from optimize import optimize
from plotMap import plotMap
from graphs import graph_rendements, graph_Q1energy, graph_Q2energy

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

    P, k = 500000, 0.17


    ### Modele 1

    print("\nMODELE 1 : RESOLUTION\n")

    print("Valeurs utilisées : P = {} ; k = {}\n".format(P,k))
    
    print("Resolution du probleme lineaire...\n")
    (x), z, sol = optimize(onshore_capa, offshore_capa, onshore_rend, offshore_rend, P, k, modele=1)

    print("Affichage des sites concernés sur une carte de l'Europe...\n")
    plotMap(data, x, name="bigIronFanQ1")

    print("Minimum de l'énergie produite en une heure, ou fonction objectif : {} MWh\n".format(z))

    print("Affichage des graphes du rendement moyen et de l'énergie produite en fonction du temps...\n")
    nticks = 500
    scale = 'jours'
    graph_rendements(sol.Rm, nticks = nticks, scale = scale, name = "graphe-rendement-Q1")
    graph_Q1energy(sol.E, nticks = nticks, scale = scale, name = "graphe-eng-Q1")


    print("Rendement moyen sur l'année : {} %".format(sol.Rmtot*100))
    print("Energie produite en un an : {} MWh".format(sol.Etot))


    ### Modele 2

    print("\nMODELE 2 : RESOLUTION\n")

    S = 2e8

    print("Valeurs utilisées : P = {} ; k = {} ; S = {}\n".format(P,k,S))
    
    print("Resolution du probleme lineaire...\n")
    (x,s), z, sol = optimize(onshore_capa, offshore_capa, onshore_rend, offshore_rend, P, k, modele=2, S=S)

    print("Affichage des sites concernés sur une carte de l'Europe...\n")
    plotMap(data, x, name="bigIronFanQ2")

    print("Minimum de l'énergie produite en une heure, ou fonction objectif : {} MWh\n".format(z))

    print("Affichage des graphes du rendement moyen et de l'énergie produite en fonction du temps...\n")
    nticks = 500
    scale = 'jours'
    graph_rendements(sol.Rm, nticks = nticks, scale = scale, name = "graphe-rendement-Q2")
    graph_Q2energy(sol.E, s, nticks = nticks, scale = scale, name = "graphe-eng-Q2")

    print("Rendement moyen sur l'année : {} %".format(sol.Rmtot*100))
    print("Energie produite en un an : {} MWh".format(sol.Etot))
    print("Energie achetee sur un an : {} MWh".format(np.sum(s)))

    
    ### Modele 3
    #(x), z, sol = optimize(onshore_capa, offshore_capa, onshore_rend, offshore_rend, P, k, delta=0.02, T=3,  modele=3)