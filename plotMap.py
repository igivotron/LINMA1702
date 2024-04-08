import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plotMap(data, x, size = 100, perSize = True):

    df = pd.DataFrame({
            "Country": data.country(),
            "Latitude": data.latitude(),
            "Longitude": data.longitude(),
            "color" : data.color(),
        }
    )

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    ax = world.clip([-12, 35, 35, 75]).plot(color="white", edgecolor="black")
    ax.set_axis_off()
    if not perSize:
        x = np.where(x==0, 0, 1)
    gdf.plot(ax=ax, color=data.color(), markersize=x*size)

    plt.show()