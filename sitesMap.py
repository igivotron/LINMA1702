import geopandas as gpd
import matplotlib.pyplot as plt

sites = open("Data-partie-1/Sites.csv", "r")
all_sites = []

for line in sites.readlines():
    tabs = line.split(",")
    try:
        index = tabs[0]
        latitude = float(tabs[1])
        longitude = float(tabs[2])
        color = tabs[4].strip()
        all_sites.append({'index': index, 'latitude': latitude, 'longitude': longitude, 'color': color})
    except:
        print(line)

gdf = gpd.GeoDataFrame(all_sites, geometry=gpd.points_from_xy([site['longitude'] for site in all_sites], [site['latitude'] for site in all_sites]))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

x_min, y_min, x_max, y_max = (-10, 35, 30, 70)
europe_zoomed = world.cx[x_min:x_max, y_min:y_max]

fig, ax = plt.subplots(figsize=(20, 16))
ax.set_axis_off()
europe_zoomed.plot(ax=ax, color='lightgrey')
gdf.plot(ax=ax, color=gdf['color'], label=gdf['index'], markersize=5)
plt.show()
