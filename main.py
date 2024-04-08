import extract_data as ext
from optimize import optimize
from time import time

import numpy as np ## pourra etre retiré lorsque np ne sera plus employe


def resolution(data):
    z, x = optimize(data.onshore_capacities(),
                    data.offshore_capacities(),
                    data.onshore_rendements(),
                    data.offshore_rendements(),
                    P=10000, k=0.4)
    return z, x

if __name__ == '__main__':
    sites_file = "Data-partie-1/Sites.csv"
    onshore_file = "Data-partie-1/Rendements_onshore.csv"
    offshore_file = "Data-partie-1/Rendements_offshore.csv"

    data = ext.ExtractData(sites_file, onshore_file, offshore_file, n=10)
    z, x = resolution(data)
    print(x)

