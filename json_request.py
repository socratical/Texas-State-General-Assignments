import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import seaborn as sns
import numpy as np
import ijson
from pandas.io.json import json_normalize
import geojson
import mplleaflet as mpll


# filename = "pets.json"
# with open(filename, 'r') as f:
#    objects = ijson.items
# austin dangerous dog api
urlD = 'https://data.austintexas.gov/resource/ykw4-j3aj.json'
# austin stray dog data
urlS = 'https://data.austintexas.gov/resource/hye6-gvq2.json'

# found_df / austin found pets pandas data frame constructor
pets_df = pd.read_json(urlS, orient='records')
location_df = json_normalize(pets_df['location'])
concat_df = pd.concat([pets_df, location_df], axis=1)
found_df = concat_df.drop(concat_df.columns[0:7], axis=1)
found_df = found_df.drop(found_df.columns[[2, 4, 6, 10]], axis=1)
address_df = pd.DataFrame(columns=['address', 'city', 'zip_code'])
for i, row in location_df.iterrows():
    rowStr = row['human_address']
    splitRow = rowStr.split('\"')
    address = splitRow[3]
    city = splitRow[7]
    zipCode = splitRow[15]
    address_df = address_df.append({'address': address, 'city': city, 'zip_code': zipCode}, ignore_index=True)
found_df = pd.concat([found_df, address_df], axis=1)
#       formatting address correctly
for i, row in found_df.iterrows():
    rowStr = row['city']
    splitRow = rowStr.split(' ')
#       ADD MORE LOCALITIES HERE IF NEEDED IN DATASET
    if splitRow[0] not in ('AUSTIN', 'PFLUGERVILLE', 'LAKEWAY', ''):
        for j in splitRow:
            if j in ('AUSTIN', 'PFLUGERVILLE', 'LAKEWAY'):
                found_df.at[i, 'city'] = j
            else:
                found_df.at[i, 'city'] = ''
        found_df.at[i, 'address'] = ''


# danger_df austin dangerous dogs pandas data frame constructor
danger_df = pd.read_json(urlD)
danger_df = danger_df.drop(danger_df.columns[[0, 1, 4, 5]], axis=1)
location_df = json_normalize(danger_df['location'])
address_df = pd.DataFrame(columns=['address'])
for i, row in location_df.iterrows():
    rowStr = row['human_address']
    splitRow = rowStr.split('\"')
    address = splitRow[3]
    address_df = address_df.append({'address': address}, ignore_index=True)
danger_df = danger_df.drop(danger_df.columns[[2]], axis=1)
location_df = location_df.drop(location_df.columns[[0]], axis=1)
danger_df = pd.concat([danger_df, address_df, location_df], axis=1)

# converting data types
found_df["latitude"] = pd.to_numeric(found_df["latitude"])
found_df["longitude"] = pd.to_numeric(found_df["longitude"])
found_df["zip_code"] = pd.to_numeric(found_df["zip_code"])
danger_df["latitude"] = pd.to_numeric(found_df["latitude"])
danger_df["longitude"] = pd.to_numeric(found_df["longitude"])
danger_df["zip_code"] = pd.to_numeric(found_df["zip_code"])

# aggregate/averages by cat vs dog
sort_zip = found_df.sort_values(by=["zip_code", "type"], ascending=[True, False])
print(sort_zip.head())
# plotting austin zip codes
# f, ax = plt.subplots(1, figsize=(9, 9))
# zc = gpd.read_file('/home/nathanh/Documents/PetDataScienceProject/Zipcodes.geojson')
# zc.plot(linewidth=0.1, ax=ax)
# found_df['geometry'] = found_df[['longitude', 'latitude']].apply(Point, axis=1)
# found_gdf = gpd.GeoDataFrame(found_df)
# found_gdf.crs = {'init': 'epsg:4269'}
# found_gdf.plot(color='red', ax=ax)
# ax.set_axis_off()
# plt.axis('equal')
# plt.show()

# displays unique values
# print(found_df.head())
# print(danger_df.dtypes)
# print(found_df.city.unique())
# print(location_df.at[0, 'human_address'])
# print(address_df.dtypes)
# print(address_df.head())
# print(found_df.dtypes)
# print(found_df.head())
# print(pets_df['location', 'human_address'].head())

# trying to convert raw json, is incomplete
# r = requests.get('https://data.austintexas.gov/api/views/hye6-gvq2/rows.json?accessType=DOWNLOAD')
# petjson = r.text
# df = pd.read_json(petjson, orient='records')
# print(df)
# with petjson as j:
#    objects = ijson.items(j, 'location.human_address')
#    columns = list(objects)"""