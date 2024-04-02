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
    z,x = optimize(data.onshore_capacities().astype(np.float64), 
             data.offshore_capacities().astype(np.float64), 
             data.onshore_rendements().astype(np.float64), 
             data.offshore_rendements().astype(np.float64), 
             ## hardcodé le cast des strings en floats, sans doute mieux de faire ça dans extract_data
             P=10000, k=0.4, 
             checkpoints=True)