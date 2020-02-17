import csv
import sys

import numpy as np
import PySimpleGUI as sg


FILENAME = 'Developer Test.csv'


def load_airport_list(filename):
    """
    Load a list of airports from a csv file.

    Args:
        filename (string): The name of the csv file containing
                           the airport data.

    First row of the CSV file should be the column headers, with
    the row data in the following format:

        Airport Name, Airport Code, Latitude, Longitude

    Returns:
        Dictionary of airport data.

        [
            ('NAME', '<string containing the name of airport>'),
            ('ICAO', '<string containing the airport code>'),
            ('Latitude', '<latitude of the airport, -ve = S>'),
            ('Longitude', '<longitude of the airport, -ve = W>')
        ],
        ...

    Raises:
        FileNotFoundError: If the csv file is not found.
    """
    reader = csv.DictReader(open(filename, 'r'))
    dict_list = []
    for line in reader:
        # Appending the `line` directly adds the latitude and longitude as
        # strings, create entry manually and do the conversions to floats
        row = {
            'NAME': line['NAME'],
            'ICAO': line['ICAO'],
            'Latitude': float(line['Latitude']),
            'Longitude': float(line['Longitude']),
        }
        dict_list.append(row)
    return dict_list


def get_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points using the
    haversine formula, which is the shortest distance
    over the surface of a sphere - in this case the
    earth.

    See:
    https://en.wikipedia.org/wiki/Haversine_formula
    http://www.movable-type.co.uk/scripts/latlong.html

    Haversine formula:
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c

    The latitudes, longitudes and deltas must be converted
    to radians to work with trigonometric functions.

    Although the built-in math library could be used here,
    Numpy is used for convenience.

    An alternative to using a `deg2rad` function would be to
    simply multiply the value by pi/180.
        Δφ = (lat2 - lat1) * pi / 180
        Δλ = (lon2 - lon1) * pi / 180
        φ1 = lat1 * pi / 180
        φ2 = lat2 * pi / 180
    """
    radius = 6371 # radius of the earth in km
    dlat = np.deg2rad(lat2 - lat1)
    dlon = np.deg2rad(lon2 - lon1)
    a  = (
        np.square(np.sin(dlat / 2)) +
        np.cos(np.deg2rad(lat1)) *
        np.cos(np.deg2rad(lat2)) *
        np.square(np.sin(dlon / 2))
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = radius * c
    return d


def get_closest(airport_list, lat, lon):
    closest_airport = None
    closest_dist = np.finfo('d').max

    for airport in airport_list:
        d = get_distance(airport['Latitude'], airport['Longitude'], lat, lon)
        if d < closest_dist:
            closest_dist = d
            closest_airport = airport

    return closest_airport, closest_dist


if __name__ == '__main__':
    # The list of airports with their respective longitudes
    # and latitudes
    airport_list = []

    # Load the airport data from the csv file and exit with
    # an error mesage if there was any issues
    try:
        airport_list = load_airport_list(FILENAME)
    except:
        print("Failed to load list of airports. "
              "Please check `{}` exists and try again.".format(FILENAME))
        sys.exit(1)

    # Display a form with inputs for latitude and longitude, plus a submit
    # and exit button
    form = sg.FlexForm("Flight Data Services Test")
    layout = [
        [sg.Text("Please enter a location (latitude and longitude):")],
        [sg.Text("Latitude", size=(15, 1)), sg.InputText('')],
        [sg.Text("Longitude", size=(15, 1)), sg.InputText('')],
        [sg.ReadFormButton("Submit"), sg.Exit()], # Use `ReadFormButton` so the
    ]                                             # form remains open
    form.Layout(layout)

    # Loop until the user exits
    while True:
        (button, values) = form.Read()
        if button is "Submit":
            # Submit has been pressed, so fetch the entered latitude and
            # longitude, then call `get_closest` to calculate the nearest
            # airport and distance to it
            try:
                lat = float(values[0]) # Convert the inputs to floats
                lon = float(values[1])
            except:
                sg.Popup(
                    "Error",
                    "There was an error reading your input. Please try again."
                )
                continue
            closest_airport, closest_dist = get_closest(airport_list, lat, lon)
            if closest_airport is not None:
                sg.Popup(
                    "Result",
                    "The closest airport to {} LAT, {} LON is:".format(
                        lat,
                        lon
                    ),
                    "\t{} ({})".format(
                        closest_airport['NAME'],
                        closest_airport['ICAO']
                    ),
                    "at a distance of:",
                    "\t{:f}.".format(closest_dist),
                )
            else:
                # Should never happen - the only foreseeable case might be with
                # an empty airport list, but that should have already been
                # caught
                sg.Popup(
                    "Result",
                    "No suitable airport was found. Please try again."
                )
        elif button is None or button is "Exit": # quit if exit button or X
            break
    exit()
