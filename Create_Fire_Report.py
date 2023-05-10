import os
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from cartopy.feature import ShapelyFeature
import datetime

# import folium  #saved for future use
# import fpdf  #saved for future use

"""  Static GIS Data  """
aoi = gpd.read_file(os.path.abspath('Data/UTM36/AOI.shp'))
coastline = gpd.read_file(os.path.abspath('Data/UTM36/Island.shp'))
towns = gpd.read_file(os.path.abspath('Data/UTM36/Cyprus_Towns.shp'))
geofence = gpd.read_file(os.path.abspath('Data/UTM36/geofence.shp'))

"""  Fire Data  """
# SUOMI VIIRS - Last 7 days Europe
snpp_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_7d.csv'

"""  Test Data   """
#  If testing is required remove the '#' from the line below (26) and add '#' before the snpp_df on line 29. Then Run.
#snpp_df = pd.read_csv('Test_Data/SUOMI_VIIRS_C2_Europe_7d (1).csv')

#  Create the snpp_df dataframe from the url
snpp_df = pd.read_csv(snpp_url)

#  Create a new dataframe with values less than or more than lat/lon for cyprus
snpp_df = snpp_df[(snpp_df['longitude'] >= 32.0) & (snpp_df['longitude'] <= 35.0)]
snpp_df = snpp_df[(snpp_df['latitude'] >= 34.5) & (snpp_df['latitude'] <= 36.0)]

print(snpp_df.head())  # Print the head of the dataset to show it has been downloaded correctly

#   Create a new geodataframe for active fires
all_Fires = gpd.GeoDataFrame(snpp_df[['acq_date', 'bright_ti4']],
                             geometry=gpd.points_from_xy(snpp_df['longitude'], snpp_df['latitude']),
                             crs='epsg:4326')
print(all_Fires.head())  # print the head of the new activeFires geopandas dataframe to show it worked correctly

#  Reproject the Fire data from WGS 84 to UTM 36 North
all_Fires_UTM = all_Fires.to_crs('epsg:32636')

#  Save activeFires_UTM as a shapefile
all_Fires_UTM.to_file(driver='ESRI Shapefile', filename='Data/UTM36/AllFiresUTM.shp')

# All Fires UTM Shapefile
fires = gpd.read_file(os.path.abspath('Data/UTM36/AllFiresUTM.shp'))


"""  Remove Fire Detection from Industrial Locations  """
#  Repeated fire detections at refinery cause issues with map and graph because user will think these are 'real' fires.
#  geofence is a shapefile which will be used to remove fires which intersect with this feature.
#  Find fires within 'geofence'
industrial_detections = gpd.sjoin(fires, geofence, predicate='within')
#  Remove fires within geofence
active_Fires = fires[~fires.index.isin(industrial_detections.index)]
#  Save as shapefile and rename value for map
active_Fires.to_file('Data/UTM36/ActiveFires.shp')
map_fires = gpd.read_file(os.path.abspath('Data/UTM36/ActiveFires.shp'))

"""  FIRE GRAPH  """
#  Create a graph to show number of fires per day
#  Graph is placed here so that it is plotted after removing fires inside geofence
df1 = pd.DataFrame(active_Fires)
dates = df1['acq_date'].value_counts().sort_index()  # Sort by date
plt.plot(dates, color='red', marker='.', label='Fires')
plt.title('Cyprus: Fire detected within the last 7 days', family='Arial', fontsize='14')
plt.xlabel('Date')
plt.ylabel('Number of Detections')
plt.tick_params(axis='x', rotation=55)
plt.savefig('FireGraph.png', bbox_inches='tight', dpi=100)

"""  Create Map  """
#  Function to create 50km alternating scale bar with label at each end
#  adapted this question: https://stackoverflow.com/q/32333870
#  answered by SO user Siyh: https://stackoverflow.com/a/35705477


def scale_bar(ax, location=(0.5, 0.05)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]
    ax.plot([sbx, sbx - 50000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 40000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 30000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx - 40000, sbx - 30000], [sby, sby], color='w', linewidth=6, transform=ax.projection)
    ax.plot([sbx - 20000, sbx - 10000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby - 6000, '50 km', transform=ax.projection, fontsize=8)
    ax.text(sbx - 55000, sby - 6000, '0 km', transform=ax.projection, fontsize=8)


#  Function to dd the current date / time as a text box to the bottom right corner of the map
def current_time():
    now = datetime.datetime.now()
    date_str = now.strftime("Fire data downloaded on\n %Y-%m-%d at %H:%M:%S")
    ax.text(0.75, 0.05, date_str, transform=ax.transAxes, ha='left', va='bottom', wrap=True,
            bbox=dict(boxstyle="round", ec='black', fc='white'))

# Create figure
myFig = plt.figure(figsize=(10, 10), facecolor='0.7')

#  Coordinate Reference system = epsg 32636 / UTM Zone 36N
myCRS = ccrs.epsg(32636)

#  Create axis object (line arc map data frame) to plot data.
ax = plt.axes(projection=myCRS,
              facecolor='#effdff')

#  Add title
plt.title('Active Fires in Cyprus: Last 7 Days')

#  Add AOI shapefile which is used for extent of the map
#  Line width set to '0' so that it does not show on map face
outline_feature = ShapelyFeature(aoi['geometry'], myCRS, edgecolor='red', facecolor='#effdff', linewidth=0)

#  Boundary of map face from extent below
xmin, ymin, xmax, ymax = aoi.total_bounds
ax.add_feature(outline_feature)  # add the features we've created to the map.

#  Set extent of the map (AOI +/- 5000 metres)
ax.set_extent([xmin - 5000, xmax + 5000, ymin - 5000, ymax + 5000], crs=myCRS)  # because total_bounds

# Add Cyprus Coastline Feature
feat = ShapelyFeature(coastline['geometry'],  # first argument is the geometry
                      myCRS,  # second argument is the CRS
                      edgecolor='k',  # outline the feature in black
                      facecolor='#DCDCDC',  # set the face color to the corresponding color from the list
                      linewidth=0.5,  # set the outline width to be 1 pt
                      alpha=1)  # set the alpha (transparency) to be 0.25 (out of 1)
ax.add_feature(feat)  # once we have created the feature, we have to add it to the map using ax.add_feature()

#  Add Geofence to show areas where fires should not appear
plot_geofence = ShapelyFeature(geofence['geometry'], myCRS, edgecolor='orange', facecolor='#effdff', linewidth=1)
ax.add_feature(plot_geofence)

#  Plot Towns
ax.plot(towns.geometry.x, towns.geometry.y, '.', color='black', ms=4, transform=myCRS)

#  Add the text labels for the towns
for ind, row in towns.iterrows():  # towns.iterrows() returns the index and row
    x, y = row.geometry.x, row.geometry.y  # get the x,y location for each town
    ax.text(x + 1000, y + 1000, row['Name'].title(), fontsize=8,
            transform=myCRS)

# Add Fire Data to Map
ax.plot(map_fires.geometry.x, map_fires.geometry.y, 's', color='red', ms=4, transform=myCRS)

#  Label Fires by date
for ind, row in map_fires.iterrows():
    x, y = row.geometry.x, row.geometry.y
    ax.text(x + 1000, y + 1000, row['acq_date'].title(), fontsize=8, transform=myCRS)

#  Add Graticule and labels
gridlines = ax.gridlines(draw_labels=True,  # draw  labels for the grid lines
                         xlocs=[32, 32.5, 33, 33.5, 34, 34.5],  # add longitude lines at 0.5 deg intervals
                         ylocs=[34, 34.5, 35, 35.5, 36])  # add latitude lines at 0.5 deg intervals

#  Add Fire Symbology to legend
fire_legend = mlines.Line2D([0], [0], color='red', marker='s',
                            markersize=4, label='Fire', linewidth=0)
#  Add Town Symbology to legend
towns_legend = mlines.Line2D([], [], color='black', marker='.',
                             markersize=4, label='Towns', linewidth=0)

#  Add Geofence to Legned to show areas where fire detections will not show on map
geofence_legend = mpatches.Patch(facecolor='none', edgecolor = 'orange')

#  Add legend text
ax.legend([fire_legend, towns_legend, geofence_legend], ['Fires', 'Towns', 'Geofence'])

#  Add the scale bar
scale_bar(ax)

#  Add the date / time that the map was created
current_time()

#  Save the map as a png
myFig.savefig('LatestFireMap.png', bbox_inches='tight', dpi=300)


"""Create PDF Report"""

""" This is saved in case FPDF can be fixed and will be used to generate final fire report.
from fpdf import FPDF

class FPDF(FPDF):
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Return page number to black
        self.set_text_color(r = 0, g = 0, b = 0)
        # Print centered page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

title = 'DAILY FIRE REPORT'
width = 210
height = 297
map = 'LatestFireMap.png'

pdf = FPDF()
pdf.add_page()
# Set the font for the title
pdf.set_font('Arial', 'B', 16)

# Add the FireMap.png as an image to the centre of the page.
pdf.image(gantt, x = 10, y = 30, w = 190, h = 150, type = '', link = '')

# Move the title cell to the centre of the page
pdf.cell(70)
# Centre the title text in a cell with a frame
pdf.cell(60, 10, title, 1, 1, 'C')

# Add an information paragraph below the Fire Map
pdf.set_font('Arial', '', 10)
pdf.set_xy(10,183)
pdf.multi_cell(w = 200, h = 8, txt ="This map shows active fires on the island of cyprus within the last 7 days.", 
                border = 0, align = 'L', fill = False)

pdf.set_xy(10,250)
pdf.multi_cell(w = 200, h = 8, txt ="This report has been auto-generated using SNPP VIIRS data, which has been 
                downloaded from the NASA FIRMS Website. For more information please click on the link below: ", 
                border = 0, align = 'L', fill = False)

pdf.set_font('Arial', 'U', 10)
pdf.set_text_color(r = 0, g = 0, b = 254)
pdf.cell(w = 30, h = 10, txt = 'https://firms.modaps.eosdis.nasa.gov/', border = 0,
          align = 'B', fill = False, link = 'https://firms.modaps.eosdis.nasa.gov/')





pdf.output('Daily_Fire_Report.pdf', 'F')

"""

print("Script Complete.........")  # script complete

# Folium Map Testing
""" This will be used to create Folium interactive map at a later stage.
folium.map.activeFires.explore('acq_date',
                 m=m, # add the markers to the same map we just created
                 marker_type='marker', # use a marker for the points, instead of a circle
                 popup=True, # show the information as a popup when we click on the marker
                 legend=False, # don't show a separate legend for the point layer
                )
m.save('NASA_Fire_Map.html') # export the folium fire map as a html
"""
