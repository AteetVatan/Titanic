"""Main Module For Ship application."""

from utils import map_utils
from utils import chart_utils as chart
from utils import json_utils
from enums.enumerations import UserInputKeys as uk
from enums.enumerations import JsonKeys as jk

CONST_SHIP_JSON_FILE = "ships_data.json"

CONST_PROMPT_DICT = {
    'welcome_msg': f"Welcome to the Ships CLI! Enter "
                   f"'{uk.HELP.value}' to view available commands.\n",
    'input_error': 'Unknown command {key}\n',
    'available_commands': 'Available commands:\n'}

CMD_METHODS_DICT = None
SHIP_JSON_DATA = None


def main_wrapper():
    """Main Wrapper Function."""
    user_process()


# region User Interaction Methods
def user_process() -> None:
    """Function to render and start the user interaction"""
    validate_user_input_help()
    user_method = get_user_input_method(uk.HELP.value)
    user_input = user_method()
    try:
        while True:
            user_method = get_user_input_method(user_input)
            if not user_method:
                user_input = input(CONST_PROMPT_DICT['input_error'].format(key=user_input))
                continue

            if user_input == uk.HELP.value:
                user_input = user_method()
                continue
            if user_input in [uk.SHOW_COUNTRIES.value,
                              uk.SHIPS_BY_TYPES.value,
                              uk.SHIPS_IN_OCEAN.value,
                              uk.SHOW_MAP.value,
                              uk.SPEED_HISTOGRAM.value]:
                user_method()
                break
            if user_input.split()[0] in [uk.TOP_COUNTRIES.value, uk.SEARCH_SHIP_NAME.value]:
                args = user_input.split()[1]
                user_method(args)
                break

    except IndexError:
        print("user_process: Invalid data Index.")
    except (RuntimeError, SystemError) as err:
        print(f"user_process: error : {err}")


def get_user_input_method(user_input: str):
    """
    Method returns the user selected function pointer.
    :param user_input: str: String entered by user
    :return:
    """
    try:
        user_input = user_input.strip()
        if len(user_input.split()) > 1 and (
                user_input.split()[0] == uk.TOP_COUNTRIES.value
                or user_input.split()[0] == uk.SEARCH_SHIP_NAME.value):
            return get_user_function(user_input.split()[0])
        if user_input in [uk.HELP.value,
                          uk.SHOW_COUNTRIES.value,
                          uk.SHIPS_BY_TYPES.value,
                          uk.SHIPS_IN_OCEAN.value,
                          uk.SHOW_MAP.value,
                          uk.SPEED_HISTOGRAM.value]:
            return get_user_function(user_input)

    except IndexError:
        print("get_user_input_method: Invalid data Index.")
    except (RuntimeError, SystemError) as err:
        print(f"get_user_input_method: Unexpected error : {err}")
    return None


def get_user_function(function_key: str):
    """
    Method returns the function pointer by given funtion key.
    :param function_key:
    :return function pointer:
    """
    return CMD_METHODS_DICT[function_key][1]


def validate_user_input_help():
    """
    Method to validate that the user has entered 'help' to proceed or
    repeat the prompt.
    :return None:
    """
    cmd_input = input(CONST_PROMPT_DICT['welcome_msg']).strip()
    while True:
        if cmd_input != uk.HELP.value:
            cmd_input = input(CONST_PROMPT_DICT['input_error'].format(key=cmd_input))
        else:
            break


# endregion

# region Base Functionality
def get_funtions_dict() -> {}:
    """
    Function to return function name and function pointer dictionary
    :return dictionary:
    """
    return {uk.HELP.value: (uk.HELP.value, show_help),
            uk.SHOW_COUNTRIES.value: (uk.SHOW_COUNTRIES.value, show_countries),
            uk.TOP_COUNTRIES.value:
                (f'{uk.TOP_COUNTRIES.value} {uk.TOP_COUNTRIES_ARG2.value}',
                 show_top_countries),
            uk.SHIPS_BY_TYPES.value: (uk.SHIPS_BY_TYPES.value, show_ships_by_types),
            uk.SEARCH_SHIP_NAME.value:
                (f'{uk.SEARCH_SHIP_NAME.value} {uk.SEARCH_SHIP_NAME_ARG2.value}',
                 search_ships_names),
            uk.SPEED_HISTOGRAM.value: (uk.SPEED_HISTOGRAM.value, show_speed_histogram),
            uk.SHIPS_IN_OCEAN.value: (uk.SHIPS_IN_OCEAN.value, ships_in_ocean),
            uk.SHOW_MAP.value: (uk.SHOW_MAP.value, show_map)}


def show_help() -> str:
    """
    Fuction to show user menu asking for input
    :return string:
    """
    try:
        cmd_str = CONST_PROMPT_DICT['available_commands']
        for cmd_tuple in CMD_METHODS_DICT.values():
            cmd_str += (cmd_tuple[0] + "\n")
        cmd_str += "\n"
    except IndexError:
        print("Invalid data Index.")
    return input(cmd_str).strip()


def show_countries():
    """
    Function to show all countries
    :return:
    """
    try:
        all_countries_list = get_all_ships_countries_from_json(unique_list=True)
        all_countries_list.sort()
        for country in all_countries_list:
            print(country)

    except ValueError:
        print("show_countries: Invalid value.")
    except RuntimeError as err:
        print(f"show_countries: Unexpected error : {err}")


def show_top_countries(num: str):
    """
    Function to show top countries with most ships by the given number(num) of countries
    :param num:
    :return:
    """
    try:
        num = int(num)
        ships_country_data = get_all_ships_countries_from_json()
        countries_count_tuple_list = create_item_count_tuple_list(ships_country_data)

        num = len(countries_count_tuple_list) if num > len(countries_count_tuple_list) else num

        for tup in countries_count_tuple_list[:num]:
            print(f"{tup[0]}: {tup[1]}")

    except IndexError:
        print("show_top_countries: Invalid data Index.")
    except ValueError:
        print("show_top_countries: Invalid value.")
    except (RuntimeError, SystemError) as err:
        print(f"show_top_countries: error : {err}")


def show_ships_by_types():
    """
    Function prints number of Ships by ship types.
    """
    try:
        ships_types_data = get_all_types_for_ships_list()
        types_count_tuple_list = create_item_count_tuple_list(ships_types_data)

        for tup in types_count_tuple_list:
            print(f"{tup[0]}: {tup[1]}")
    except IndexError:
        print("show_ships_by_types: Invalid data Index.")
    except RuntimeError as err:
        print(f"show_ships_by_types: error : {err}")


def search_ships_names(user_input: str):
    """
    Funtion prints ships name by user input
    """
    try:
        ships_name_data = get_all_names_for_ships_list()
        ships_names_found = [x for x in ships_name_data if user_input.lower() in x.lower()]
        if len(ships_names_found) < 1:
            print(f"No ships by name {user_input} found")
        else:
            for item in ships_names_found:
                print(f"{item}")
    except RuntimeError as err:
        print(f"search_ships_names: error : {err}")


def show_speed_histogram():
    """
    Function to show histogram
    """
    try:
        speed_list = get_ships_speed_list()
        chart.create_histogram(speed_list)
    except RuntimeError as err:
        print(f"show_speed_histogram: error : {err}")


def ships_in_ocean():
    """
    Funtion prints ships by oceans
    """
    ships_name_lat_lng_dict = get_ships_lat_lng_dict()
    ocean_dict = {}
    for ship, loc in ships_name_lat_lng_dict.items():
        ocean = ship_in_which_ocean(loc[0], loc[1])
        if ocean != "":
            ocean_ship_list = ocean_dict.get(ocean)
            if ocean_ship_list is not None:
                ocean_ship_list += [ship]
            else:
                ocean_ship_list = [ship]
            ocean_dict.update({ocean: ocean_ship_list})

    for ocean, ships in ocean_dict.items():
        print(f"Ocean Name : {ocean}")
        print(ships, sep=", ")


def show_map():
    """
    Funtion to create map for ships
    """
    ships_name_lat_lng_dict = get_ships_lat_lng_dict()
    # ship_names = ships_name_lat_lng_dict.keys()
    lats, lngs = zip(*ships_name_lat_lng_dict.values())
    file_name = map_utils.draw_map(lats, lngs)
    print(f"Map saved as {file_name}")


# endregion

# region Json


def get_all_ships_countries_from_json(unique_list=False) -> []:
    """
    Function to load countries(if unique_list then no dulplicates) of all ships in a list
    :param unique_list:
    :return list:
    """
    all_countries = [x[jk.COUNTRY.value] for x in SHIP_JSON_DATA[jk.DATA_KEY.value]]
    if unique_list:
        return list(set(all_countries))
    return all_countries


def get_all_types_for_ships_list() -> []:
    """
    Function to load countries of all ships in a list
    :param ship_json:
    :return list:
    """
    return [x[jk.TYPE.value] for x in SHIP_JSON_DATA[jk.DATA_KEY.value]]


def get_all_names_for_ships_list() -> []:
    """
    Function to load countries of all ships in a list
    :param ship_json:
    :return list:
    """
    return [x[jk.SHIPNAME.value] for x in SHIP_JSON_DATA[jk.DATA_KEY.value]]


def get_ships_speed_list() -> {}:
    """
    Funtion return dictionary of ships with there speed
    """
    return [float(x[jk.SPEED.value]) for x in SHIP_JSON_DATA[jk.DATA_KEY.value]]


def get_ships_lat_lng_dict() -> {}:
    """
    Funtion return dictionary of ships with there Latitude and Longitude
    """
    return {x[jk.SHIPNAME.value]: (float(x[jk.LAT.value]), float(x[jk.LON.value])) for x in
            SHIP_JSON_DATA[jk.DATA_KEY.value]}


# endregion

# region Map
def ship_in_which_ocean(latitude: float, longitude: float):
    """
    Funtion to identify that the ship is in which ocean
    """
    ocean_name = ""
    for ocean_name, bound in map_utils.CONST_MAP_OCEANS_BOUNDS_DICT.items():
        if map_utils.in_bounds(longitude, latitude, bound[1], bound[0]):
            return ocean_name
    return ocean_name


# endregion

# region Utils
def create_item_count_tuple_list(raw_list: list) -> list[tuple[str, int]]:
    """
    Funtion return dictionary of ships with there speed
    """
    raw_list_tuple = tuple(raw_list)
    item_dict = {x: raw_list_tuple.count(x) for x in raw_list}
    items_tuple_sorted_list = sorted(item_dict.items(),
                                     key=lambda item: item[1], reverse=True)
    return items_tuple_sorted_list


# endregion

if __name__ == "__main__":
    CMD_METHODS_DICT = get_funtions_dict()
    SHIP_JSON_DATA = json_utils.load_ship_json(CONST_SHIP_JSON_FILE)
    main_wrapper()
