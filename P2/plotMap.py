import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plotMap(data, x, size = 0.1):
    """
    Plots the map
    :param data:data
    :param x:x
    :param size: points default size (default 10)
    :param perSize: change the size of the points (default True)
    :param name: name of the image to save
    """

    df = pd.DataFrame({
            "Latitude": data.getLatitude(),
            "Longitude": data.getLongitude(),
            "color" : data.getColor(),
        }
    )

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    ax = world.clip([-12, 35, 35, 75]).plot(color="ivory", edgecolor="black")
    ax.set_axis_off()
    gdf.plot(ax=ax, color=data.getColor(), markersize=x*size, aspect="equal")

    plt.show()
