import numpy as np
import geopandas as gpd
import shapely
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from get_locs_from_db import lats, longs, uids
import sys

def points_in_radius(gpd_df, cpt, radius):
    """
    :param gpd_df: Geopandas dataframe in which to search for points
    :param cpt:    Point about which to search for neighbouring points
    :param radius: Radius about which to search for neighbours
    :return:       List of point indices around the central point, sorted by
                   distance in ascending order
    """
    # Spatial index
    sindex = gpd_df.sindex
    # Bounding box of rtree search (West, South, East, North)
    bbox = (cpt.x-radius, cpt.y-radius, cpt.x+radius, cpt.y+radius)
    # Potential neighbours
    good = []
    for intersection_point in sindex.intersection(bbox):
        dist = cpt.distance(gpd_df['geometry'][intersection_point])
        if dist < radius:
            good.append((dist, intersection_point))
    # Sort list in ascending order by `dist`, then `n`
    good.sort()
    # print(good)
    # Return only the neighbour indices, sorted by distance in ascending order
    return [x[1] for x in good]

if __name__ == "__main__":
    long_min = 12.8716
    long_max = 12.9716
    lat_min = 77.5946
    lat_max = 77.9946

    # x = np.random.uniform(low=lat_min, high=lat_max, size=100)
    # y = np.random.uniform(low=long_min, high=long_max, size=100)
    # print(np.array2string(x, separator=', '))
    # print(np.array2string(y, separator=', '))
    x = longs
    y = lats

    init_crs = "EPSG:4326"
    crs = "EPSG:3395"

    fig, ax = plt.subplots(figsize = (8,8))

    # kar_map = gpd.read_file("karnataka_location/karnataka_location.shp")
    # kar_map.crs = init_crs
    # kar_map = kar_map.to_crs(crs)
    # kar_map.plot(ax=ax)
    # plt.show()

    # kar_map.plot(ax=ax, alpha=0.4, color="grey")

    df = gpd.GeoDataFrame(
        data={"uid": uids}, geometry=gpd.points_from_xy(x, y))

    # df.plot(ax=ax, markersize=20, color="red")
    # gpd.GeoDataFrame(data={}, geometry=gpd.points_from_xy([77.6], [12.9])).plot(ax=ax, markersize=20, color="blue")
    # plt.show()

    print(df.head())
    df.crs = init_crs
    print("CRS before:", df.crs)
    df = df.to_crs(crs)
    print("CRS after:", df.crs)
    print(df.head())

    # unnecesarry values since coords are in geometry
    # del df["x"]
    # del df["y"]
    # try:
        # import geocoder
        # g = geocoder.ip('me')
        # pointy, pointx = g.latlng
    # except ImportError as e:
    pointx = 77.5876724
    pointy = 13.1285214
    point = shapely.geometry.Point(pointx, pointy)
    gs = gpd.GeoSeries([point])
    print(gs)
    gs.crs = init_crs
    print(gs)
    gs = gs.to_crs(crs)
    print(gs)
    print(gs[0])

    try:
        radius = float(sys.argv[1])
    except (IndexError, ValueError) as e:
        print("Assuming radius as 10 meters")
        radius = 10
    neighbours = points_in_radius(df, gs[0], radius)
    # print(neighbours)
    # print("Points near 12.5, 76.5 in range 0.5")
    neighbours = df.iloc[neighbours]

    circle = Circle((gs.geometry.x, gs.geometry.y), radius=radius, color="cyan", fill=False)

    ax.add_artist(circle)
    df.plot(ax=ax, markersize=20, color="red")
    gs.plot(ax=ax, markersize=20, color="blue")

    neighbours.plot(ax=ax, markersize=20, color="green")
    plt.show()

