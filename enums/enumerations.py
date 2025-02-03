"""Module For Enumerations."""
from enum import Enum


class UserInputKeys(Enum):
    """
    Class Enumeration for User inputs
    """
    HELP = "help"
    SHOW_COUNTRIES = "show_countries"
    TOP_COUNTRIES = "top_countries"
    TOP_COUNTRIES_ARG2 = "<num_countries>"
    SHIPS_BY_TYPES = "ships_by_types"
    SEARCH_SHIP_NAME = "search_ship"
    SEARCH_SHIP_NAME_ARG2 = "<name>"
    SPEED_HISTOGRAM = "speed_histogram"
    SHIPS_IN_OCEAN = "ships_in_ocean"
    SHOW_MAP = "show_map"


class JsonKeys(Enum):
    """
    Class Enumeration for Json Keys
    """
    DATA_KEY = "data"
    SHIPNAME = "SHIPNAME"
    COUNTRY = "COUNTRY"
    TYPE = "TYPE_SUMMARY"
    SPEED = "SPEED"
    LAT = "LAT"
    LON = "LON"
