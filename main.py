import extract_data as ext
from optimize import optimize

import numpy as np ## pourra etre retiré lorsque np ne sera plus employe

if __name__ == '__main__':
    sites_file = "Data-partie-1/Sites.csv"
    onshore_file = "Data-partie-1/Rendements_onshore.csv"
    offshore_file = "Data-partie-1/Rendements_offshore.csv"
    n = 10
    data = ext.ExtractData(sites_file, onshore_file, offshore_file)
    data.capacities()
    z,x = optimize(data.onshore_capacities(),
             data.offshore_capacities(),
             data.onshore_rendements(),
             data.offshore_rendements(),
             P=10000, k=0.4, 
             checkpoints=True)