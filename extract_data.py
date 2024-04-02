import numpy as np
class ExtractData:
    def __init__(self, sites_file, onshore_file, offshore_file, n=642):
        """
        Extrait les données des fichiers
        :param sites_file: Nom du fichier contenant les sites
        :param onshore_file: Nom du fichier contenant les données onshore
        :param offshore_file: Nom du fichier contenant les données offshore
        :param n: Nombre de site à visiter
        """
        self.sites_file = sites_file
        self.onshore_file = onshore_file
        self.offshore_file = offshore_file
        self.n = n
        self.data = self.extract_sites()

    def extract_sites(self):
        ### On ouvre le fichier et on l'enregistre dans une variable (c'est lourd)
        with open(self.sites_file, 'r') as f:
            lines = f.read()

        ### On coupe le contenu du fichier en ligne puis en colonne
        lines = lines.split("\n")[1:self.n + 1]
        for i in range(len(lines)):
            lines[i] = lines[i].split(",")
        return lines

    def capacities(self):
        list_capacities = []
        for i in self.data:
            list_capacities.append(i[7])
        return list_capacities

    def onshore_capacities(self):
        list_capacities = np.array([])
        for i in self.data:
            if i[5] == "Non":
                list_capacities = np.append(list_capacities, i[7])
        return list_capacities

    def offshore_capacities(self):
        list_capacities = np.array([])
        for i in self.data:
            if i[5] == "Oui":
                list_capacities = np.append(list_capacities, i[7])
        return list_capacities
    def onshore_rendements(self):
        ### Ouvre le fichier des données onshore et crée une liste à partir des données
        with open(self.onshore_file, 'r') as f:
            lines = f.read()

        lines = lines.split("\n")
        list_onshore = []

        for i in self.data:
            if i[5] == "Non":
                index = int(i[0])
                a = lines[index].split(",")
                list_onshore.append(a)

        return np.array(list_onshore)

    def offshore_rendements(self):
        ### On ouvre le fichier des données offshores et crée une liste de string à partir des données
        with open(self.offshore_file, 'r') as f:
            lines = f.read()

        lines = lines.split("\n")
        list_offshore = []

        for i in self.data:
            if i[5] == "Oui":
                index = int(i[0])
                a = lines[index].split(",")
                list_offshore.append(a)

        return np.array(list_offshore)
