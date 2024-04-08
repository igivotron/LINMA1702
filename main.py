import extract_data as ext
from optimize import optimize
from time import time

import numpy as np ## pourra etre retiré lorsque np ne sera plus employe


def resolution(on_cap, off_cap, on_rend, off_rend):
    z, x = optimize(on_cap, off_cap, on_rend, off_rend, P=10000, k=0.4)
    return z, x

if __name__ == '__main__':
    sites_file = "Data-partie-1/Sites.csv"
    onshore_file = "Data-partie-1/Rendements_onshore.csv"
    offshore_file = "Data-partie-1/Rendements_offshore.csv"

    data = ext.ExtractData(sites_file, onshore_file, offshore_file, n=10)

    onshore_capa = data.onshore_capacities()
    offshore_capa = data.offshore_capacities()
    onshore_rend = data.onshore_rendements()
    offshore_rend = data.offshore_rendements()

    z, x = resolution(onshore_capa, offshore_capa, onshore_rend, offshore_rend)
    print(x)

