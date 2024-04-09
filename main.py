import extract_data as ext
from optimize import optimize
from plotMap import plotMap

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

    z, x, sol = optimize(onshore_capa, offshore_capa, onshore_rend, offshore_rend)
    plotMap(data, x)
    print(x)
    print(np.nonzero(x))


