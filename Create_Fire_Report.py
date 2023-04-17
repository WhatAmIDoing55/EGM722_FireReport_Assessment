print("Starting Script........") # script starting

""" Libraries """
import pandas as pd
import geopandas as gpd
import folium

""" Fire Data """
# SUOMI VIIRS - Last 7 days Europe
snpp_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_7d.csv'

snpp_df = pd.read_csv(snpp_url) # create the snpp_df dataframe from the url

print(snpp_df.head()) # print the head of the dataset to show it has download correctly

# create a new geodataframe
activeFires = gpd.GeoDataFrame(snpp_df[['acq_date', 'bright_ti4']], # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(snpp_df['longitude'], snpp_df['latitude']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon

print(activeFires.head()) # print the head of the new activeFires geopandas dataframe to show it worked correctly



#Folium Map Testing
"""
folium.map.activeFires.explore('acq_date',
                 m=m, # add the markers to the same map we just created
                 marker_type='marker', # use a marker for the points, instead of a circle
                 popup=True, # show the information as a popup when we click on the marker
                 legend=False, # don't show a separate legend for the point layer
                )
m.save('NASA_Fire_Map.html') # export the folium fire map as a html which can be opened from windows explorer in the same folder as this python script
"""

print("Script Complete.........") # script complete