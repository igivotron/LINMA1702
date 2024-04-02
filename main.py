import extract_data as ext
if __name__ == '__main__':
    sites_file = "Data-partie-1/Sites.csv"
    onshore_file = "Data-partie-1/Rendements_onshore.csv"
    offshore_file = "Data-partie-1/Rendements_offshore.csv"
    n = 10
    data = ext.ExtractData(sites_file, onshore_file, offshore_file, n)
    data.capacities()

