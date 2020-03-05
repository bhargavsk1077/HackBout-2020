import numpy as np
import geopandas as gpd

oregon_xmin = -124.5664
oregon_xmax = -116.4633
oregon_ymin = 41.9920
oregon_ymax = 46.2938


def radius(gpd_df, cpt, radius):
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
    for n in sindex.intersection(bbox):
        dist = cpt.distance(gpd_df['geometry'][n])
        if dist < radius:
            good.append((dist, n))
    # Sort list in ascending order by `dist`, then `n`
    good.sort()
    # Return only the neighbour indices, sorted by distance in ascending order
    return [x[1] for x in good]


# Generate random points throughout Oregon
x = np.random.uniform(low=oregon_xmin, high=oregon_xmax, size=10000)
y = np.random.uniform(low=oregon_ymin, high=oregon_ymax, size=10000)

# Turn the lat-long points into a geodataframe
gpd_df = gpd.GeoDataFrame(
    data={'x': x, 'y': y}, geometry=gpd.points_from_xy(x, y))

print(gpd_df.sindex)

# Set up point geometries so that we can index the data frame
# gpd_df['geometry'] = gpd_df.apply(lambda row: shapely.geometry.Point((row['x'], row['y'])), axis=1)

# The 'x' and 'y' columns are now stored as part of the geometry, so we remove
# their columns in order to save space
del gpd_df['x']
del gpd_df['y']

for i, row in gpd_df.iterrows():
    neighbours = radius(gpd_df, row['geometry'], 0.5)
    print(neighbours)
    # Use len(neighbours) here to construct a new row for the data frame
