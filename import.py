import pandas as pd
import googlemaps
from geopy.distance import geodesic
import requests

curr_location = "1280 Main Street West"

# Todo: import api key from hidden file
gmaps = googlemaps.Client(key='XXXXXX')  # Authentication Information


# Takes in a google maps geocode, outputs the latitude and longitude
def lat_long(geocode):
    for info in geocode:
        latitude = info['geometry']['location']['lat']
        longitude = info['geometry']['location']['lng']
        return latitude, longitude


# Takes in a csv, the index of the title, index of the lattitude, and the index of the longitude and the current
# location. Outputs the a list with all of the information including the distance
def coordinates(csv, title_ind, lat_ind, lng_ind, location):
    csv_list = csv.values.tolist()
    curr_coord = lat_long(gmaps.geocode(location))
    object_list = []
    title = []
    address = []
    lat = []
    lng = []
    distance = []
    for entry in csv_list:
        title.append(entry[title_ind])
        lat.append(entry[lat_ind])
        lng.append(entry[lng_ind])

    for i in range(len(csv_list)):
        coord = (lat[i], lng[i])
        km = geodesic(coord, curr_coord).kilometers
        distance.append(km)
        reverse_geocode_result = gmaps.reverse_geocode(coord)
        address.append(reverse_geocode_result[0]["formatted_address"])

    for j in range(len(title)):
        object_list.append(
            {'Title': title[j], 'Address': address[j], 'Latitude': lat[j], 'Longitude': lng[j], 'Distance': distance[j]}
        )

    return object_list


# Extracting the CSVs for indoor information
arena_import = pd.read_csv('Arenas.csv', index_col=0)
arenas = coordinates(arena_import, 2, 7, 6, curr_location)

library_import = pd.read_csv('Libraries.csv', index_col=0)
libraries = coordinates(library_import, 2, 9, 8, curr_location)

museums_import = pd.read_csv('Museums_and_Galleries.csv', index_col=0)
museums = coordinates(museums_import, 2, 4, 3, curr_location)

community_import = pd.read_csv('Recreation_and_Community_Centres.csv', index_col=0)
communities = coordinates(community_import, 2, 4, 3, curr_location)

# Extracting the CSVs for outdoor information
beaches_import = pd.read_csv('Beaches.csv', index_col=0)
beaches = coordinates(beaches_import, 2, 5, 4, curr_location)

campground_import = pd.read_csv('Campgrounds.csv', index_col=0)
camps = coordinates(campground_import, 1, 5, 4, curr_location)

waterfalls_import = pd.read_csv('City_Waterfalls.csv', index_col=0)
falls = coordinates(waterfalls_import, 3, 14, 13, curr_location)

pads_import = pd.read_csv('Spray_Pads.csv', index_col=0)
pads = coordinates(pads_import, 2, 9, 8, curr_location)

# Sorting the Lists by distance and categorising the information
indoor = [arenas, libraries, museums, communities]
outdoor = [beaches, camps, falls, pads]

for i in range(len(indoor)):
    indoor[i].sort(key=lambda item: item.get('Distance'))

for i in range(len(outdoor)):
    outdoor[i].sort(key=lambda item: item.get('Distance'))

# Weather Information API
resp = requests.get(
    "https://api.darksky.net/forecast/8b486e7acbd606454f4a0f8f95b56886/43.263444914224245,-79.91824930126315"
)

data = resp.json()

# Gets information on the temperature, current precipitation and predicted precipitation
temp = data['currently']['apparentTemperature']
precip = data['currently']['precipIntensity']
predict_precip = data['currently']['precipProbability']


# ouputs a list of activities, one from each category, with all of the information from "coordinates()"
def output(temperature, precipitation, predicted_precipitation, indoor_list, outdoor_list):
    if predicted_precipitation < 0.5 and precipitation == 0 and temperature > 68:
        place_list = []
        for i in range(len(outdoor_list)):
            place_list.append(outdoor_list[i][0])

    else:
        place_list = []
        for i in range(len(indoor_list)):
            place_list.append(indoor_list[i][0])

    place_list.sort(key=lambda item: item.get('Distance'))

    return place_list

