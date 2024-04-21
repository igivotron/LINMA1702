import numpy as np

class ExtractData:
    def __init__(self, sites_file, onshore_file, offshore_file, n=642):
        """
        Extrait les données des fichiers
        :param sites_file: Nom du fichier contenant les sites
        :param onshore_file: Nom du fichier contenant les données onshore
        :param offshore_file: Nom du fichier contenant les données offshore
        :param n: Nombre de sites à visiter
        """
        self.sites_file = sites_file
        self.onshore_file = onshore_file
        self.offshore_file = offshore_file
        self.n = n
        self.n_onshore = int(0.75 * n)
        self.n_offshore = n - self.n_onshore
        if self.n_offshore > 155:
            self.n_offshore = 154
        self.data = self.extract_sites()

    def extract_sites(self):
        ### On ouvre le fichier et on l'enregistre dans une variable (c'est lourd)
        with open(self.sites_file, 'r') as f:
            lines = f.read()

        ### On coupe le contenu du fichier en lignes puis en colonnes
        if self.n != 642:
            lines1 = lines.split("\n")[1:1+self.n_onshore]
            lines2 = lines.split("\n")[489:489+self.n_offshore]
            lines3 = lines1 + lines2
        else:
            lines3 = lines.split("\n")[1:-1]

        for i in range(len(lines3)):
            lines3[i] = lines3[i].split(",")
        return lines3

    def capacities(self):
        list_capacities = []
        for i in self.data:
            list_capacities.append(i[7])
        return np.array(list_capacities).astype(np.float64)

    def onshore_capacities(self):
        list_capacities = np.array([])
        for i in self.data:
            if i[5] == "Non":
                list_capacities = np.append(list_capacities, i[7])
        return list_capacities.astype(np.float64)

    def offshore_capacities(self):
        list_capacities = np.array([])
        for i in self.data:
            if i[5] == "Oui":
                list_capacities = np.append(list_capacities, i[7])
        return list_capacities.astype(np.float64)
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

        return np.array(list_onshore).astype(np.float64)

    def offshore_rendements(self):
        ### On ouvre le fichier des données offshore et crée une liste de string à partir des données
        with open(self.offshore_file, 'r') as f:
            lines = f.read()

        lines = lines.split("\n")
        list_offshore = []

        for i in self.data:
            if i[5] == "Oui":
                index = int(i[0])
                a = lines[index].split(",")
                list_offshore.append(a)

        return np.array(list_offshore).astype(np.float64)

    def latitude(self):
        lat = []
        for i in self.data:
            lat.append(i[1])
        return lat

    def longitude(self):
        long = []
        for i in self.data:
            long.append(i[2])
        return long

    def country(self):
        country = []
        for i in self.data:
            country.append(i[3])
        return country

    def color(self):
        color = []
        for i in self.data:
            color.append(i[4])
        return color

