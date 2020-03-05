import numpy as np
import geopandas as gpd
import shapely

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

def points_in_radius_wrapper(x, y, pointx, pointy, radius, data={}):
    df = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(x, y))

    # df.crs = "EPSG:4326"
    # print("CRS before:", df.crs)
    # df = df.to_crs("EPSG:3395")
    # print("CRS after:", df.crs)
    init_crs = "EPSG:4326"
    df.crs = init_crs
    crs = "EPSG:3395"
    df = df.to_crs(crs)
    print(df.head())

    point = shapely.geometry.Point(pointx, pointy)
    gs = gpd.GeoSeries([point])
    gs.crs = init_crs
    gs = gs.to_crs(crs)

    neighbours = points_in_radius(df, gs[0], radius)
    neighbours = df.iloc[neighbours]
    neighbours = neighbours.to_crs(init_crs)
    return neighbours

