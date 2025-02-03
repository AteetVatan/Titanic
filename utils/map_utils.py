"""Module For Map Operations."""
import gmplot

# pip install gmplot
# Create the map plotter:
API_KEY = 'AIzaSyCXI9zcv5OzJDviTUnblWm3kYQRCGWRRHc'  # (your API key here)
gmap = gmplot.GoogleMapPlotter(30.000000, 0.000000, 3, apikey=API_KEY)

CONST_MAP_OCEANS_BOUNDS_DICT = {
    'NORTH_PACIFIC_OCEAN': ((10.04004, 104.2759), (69.4983, -92.4232)),
    'SOUTH_PACIFIC_OCEAN': ((-49.5105, 125.3169), (29.3634, -71.3822)),
    'INDIAN_OCEAN': ((-13.3742, 36.8148), (29.1084, 118.4652)),
    'MEDITERRANEAN_SEA': ((27.6883, -5.4327), (45.2168, 35.3924)),
    'NORTH_ATLANTIC_OCEAN': ((13.3308, -88.5992), (49.6711, -6.9488)),
    'SOUTH_ATLANTIC_OCEAN': ((-40.7455, -64.234), (-0.7447, 17.4153)),
    'NORTH_SEA': ((48.0150, -10.7684), (60.6915, 30.0567))}


def in_bounds(longitude: float, latitude: float, bounds_ne: tuple, bounds_sw: tuple):
    """
    Function to check longitude & latitude are in given map bounds
    """
    east_bound = longitude < float(bounds_ne[1])
    west_bound = longitude > float(bounds_sw[1])

    if float(bounds_ne[1]) < float(bounds_sw[1]):
        in_long = east_bound or west_bound
    else:
        in_long = east_bound and west_bound

    in_lat = latitude > float(bounds_sw[0]) and longitude < float(bounds_ne[0])
    return in_lat and in_long


def draw_map(lats, lngs) -> str:
    """
    Function to draw map and returns the created map file name
    """
    file_name = 'map.html'
    gmap.scatter(lats, lngs, symbol="o", color='#3B0B39', size=30000, marker=False)
    gmap.draw(file_name)
    return file_name
