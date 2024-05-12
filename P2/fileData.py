import pandas as pd
import numpy as np
class FileData:
    def __init__(self, ):
        self.__consoFile = "../Data/Consommations.csv"
        self.__hydroFile = "../Data/Apports-hydro.csv"
        self.__rend_offshoreFile = "../Data/Rendements_offshore.csv"
        self.__rend_onshoreFile = "../Data/Rendements_onshore.csv"
        self.__sitesFile = "../Data/Sites.csv"
        self.__consoData = pd.read_csv(self.__consoFile)
        self.__hydroData = pd.read_csv(self.__hydroFile)
        self.__sitesData = pd.read_csv(self.__sitesFile)

    def getConsoData(self):
        return self.__consoData.values

    def getHydroData(self):
        return self.__hydroData.values

    def getOnshore(self):
        return self.__sitesData.loc[self.__sitesData["capacite offshore"] == "Non"]

    def getOffshore(self):
        return self.__sitesData.loc[self.__sitesData["capacite offshore"] == "Oui"]

    def getOnshoreCapacites(self):
        return self.getOnshore()["capacites"].values

    def getOffshoreCapacites(self):
        return self.getOffshore()["capacites"].values

    def getCapacities(self):
        return np.concatenate((self.getOnshoreCapacites(), self.getOffshoreCapacites()))

    def getOnshoreIndex(self):
        return self.getOnshore()["index site"].values

    def getOffshoreIndex(self):
        return self.getOffshore()["index site"].values

    def getRendOnshore(self):
        with open(self.__rend_onshoreFile) as f:
            data = f.read().split("\n")
        for i in range(len(data)):
            data[i] = data[i].split(",")
        rendOnshore = []
        for i in self.getOnshoreIndex():
            rendOnshore.append(data[i])
        return np.array(rendOnshore, dtype=np.float64)

    def getRendOffshore(self):
        with open(self.__rend_offshoreFile) as f:
            data = f.read().split("\n")
        for i in range(len(data)):
            data[i] = data[i].split(",")
        rendOffshore = []
        for i in self.getOffshoreIndex():
            rendOffshore.append(data[i])
        return np.array(rendOffshore, dtype=np.float64)

    def getRend(self):
        return np.concatenate((self.getRendOnshore(), self.getRendOffshore()))

    def getLatitude(self):
        return self.__sitesData["latitude"].values

    def getLongitude(self):
        return self.__sitesData["longitude"].values

    def getColor(self):
        return self.__sitesData["couleur"].values

data = FileData()
print(data.getOffshoreCapacites().shape)
print(data.getOnshoreCapacites().shape)
