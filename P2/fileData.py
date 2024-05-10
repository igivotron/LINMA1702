import pandas as pd
import numpy as np
class FileData:
    def __init__(self, ):
        self.consoFile = "../Data/Consommations.csv"
        self.hydroFile = "../Data/Apports-hydro.csv"
        self.rend_offshoreFile = "../Data/Rendements_offshore.csv"
        self.rend_onshoreFile = "../Data/Rendements_onshore.csv"
        self.sitesFile = "../Data/Sites.csv"
        self.consoData = pd.read_csv(self.consoFile)
        self.hydroData = pd.read_csv(self.hydroFile)
        self.sitesData = pd.read_csv(self.sitesFile)

    def getConsoData(self):
        return self.consoData.values

    def getHydroData(self):
        return self.hydroData.values

    def getOnshore(self):
        return self.sitesData.loc[self.sitesData["capacite offshore"] == "Non"]

    def getOffshore(self):
        return self.sitesData.loc[self.sitesData["capacite offshore"] == "Oui"]

    def getOnshoreCapacites(self):
        return self.getOnshore()["capacites"].values

    def getOffshoreCapacites(self):
        return self.getOffshore()["capacites"].values

    def getOnshoreIndex(self):
        return self.getOnshore()["index site"].values

    def getOffshoreIndex(self):
        return self.getOffshore()["index site"].values

    def getRendOnshore(self):
        with open(self.rend_onshoreFile) as f:
            data = f.read().split("\n")
        rendOnshore = []
        for i in self.getOnshoreIndex():
            rendOnshore.append(data[i])
        return np.array(rendOnshore, dtype=np.float64)

    def getRendOffshore(self):
        with open(self.rend_offshoreFile) as f:
            data = f.read().split("\n")
        rendOffshore = []
        for i in self.getOffshoreIndex():
            rendOffshore.append(data[i])
        return np.array(rendOffshore, dtype=np.float64)

    def getLatitude(self):
        return self.sitesData["latitude"].values

    def getLongitude(self):
        return self.sitesData["longitude"].values

    def getColor(self):
        return self.sitesData["couleur"].values



