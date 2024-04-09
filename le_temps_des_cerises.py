import numpy as np
from time import time
import matplotlib.pyplot as plt
from optimize import optimize
from extract_data import ExtractData

sites_file = "Data-partie-1/Sites.csv"
onshore_file = "Data-partie-1/Rendements_onshore.csv"
offshore_file = "Data-partie-1/Rendements_offshore.csv"

def resolution_speed(sites_file, onshore_file, offshore_file, timey, episode):
    """
    :param sites_file: sites file data
    :param onshore_file: onshore rendements data
    :param offshore_file: offshore rendements data
    :param timey: how many times to execute the subsimulation
    :param episode: number of pool to test
    """
    P,k = 10000, 0.4

    m = int(642/episode)
    registre_temporel = np.zeros(episode+1)
    registre_n = np.zeros(episode+1)
    for i in range(1, episode+1):
        data = ExtractData(sites_file, onshore_file, offshore_file, n=i*m)
        time_list = np.zeros(timey)
        for j in range(timey):
            onshore_capa = data.onshore_capacities()
            offshore_capa = data.offshore_capacities()
            onshore_rend = data.onshore_rendements()
            offshore_rend = data.offshore_rendements()
            start_time = time()
            optimize(onshore_capa, offshore_capa, onshore_rend, offshore_rend, P, k)
            end_time = time()
            time_list[j] = end_time - start_time
        registre_temporel[i] = np.average(time_list)
        registre_n[i] = i*m
    return registre_n, registre_temporel

n, speed = resolution_speed(sites_file, onshore_file, offshore_file, 10, 50)
print(len(n))
plt.plot(n, speed)
plt.grid(which='both')
plt.show()