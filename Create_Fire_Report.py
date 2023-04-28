print("Starting Script........") # script starting

""" Libraries """
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import folium
#import fpdf

""" Fire Data """
# SUOMI VIIRS - Last 7 days Europe
snpp_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_7d.csv'

snpp_df = pd.read_csv(snpp_url) # create the snpp_df dataframe from the url

print(snpp_df.head()) # print the head of the dataset to show it has download correctly

# Create a new geodataframe for active fires
activeFires = gpd.GeoDataFrame(snpp_df[['acq_date', 'bright_ti4']], # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(snpp_df['longitude'], snpp_df['latitude']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon
print(activeFires.head()) # print the head of the new activeFires geopandas dataframe to show it worked correctly

""" GIS DATA """
aoi = gpd.read_file(os.path.abspath('Data/UTM36/AOI.shp'))
coastline = gpd.read_file(os.path.abspath('Data/UTM36/Island.shp'))

""" Create Map"""
# Work in progress. Copy Pasta exercise 2, to create fire map for cyprus instead of NI.
# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


# create a scale bar of length 20 km in the upper right corner of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477
def scale_bar(ax, location=(0.92, 0.95)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
    ax.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby-4500, '20 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-12500, sby-4500, '10 km', transform=ax.projection, fontsize=8)
    ax.text(sbx-24500, sby-4500, '0 km', transform=ax.projection, fontsize=8)


# load the datasets


# create a figure of size 10x10 (representing the page size in inches)
myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.epsg(32636)  # create a Universal Transverse Mercator reference system to transform our data.
# epsg32636 is UTM Zone 36 North for Cyprus

ax = plt.axes(projection=myCRS)  # finally, create an axes object in the figure, using a UTM projection,
# where we can actually plot our data.

# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(aoi['geometry'], myCRS, edgecolor='red', facecolor='w')


xmin, ymin, xmax, ymax = aoi.total_bounds
ax.add_feature(outline_feature)  # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=myCRS)  # because total_bounds
# gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

# pick colors, add features to the map
#county_colors = ['firebrick', 'seagreen', 'royalblue', 'coral', 'violet', 'cornsilk']

# get a list of unique names for the county boundaries
#county_names = list(counties.CountyName.unique())
#county_names.sort()  # sort the counties alphabetically by name

# next, add the municipal outlines to the map using the colors that we've picked.
# here, we're iterating over the unique values in the 'CountyName' field.
# we're also setting the edge color to be black, with a line width of 0.5 pt.
# Feel free to experiment with different colors and line widths.

feat = ShapelyFeature(coastline['geometry'],  # first argument is the geometry
                          myCRS,  # second argument is the CRS
                          edgecolor='k',  # outline the feature in black
                          facecolor='black',  # set the face color to the corresponding color from the list
                          linewidth=1,  # set the outline width to be 1 pt
                          alpha=0.25)  # set the alpha (transparency) to be 0.25 (out of 1)
ax.add_feature(feat)  # once we have created the feature, we have to add it to the map using ax.add_feature()

"""for ii, name in enumerate(county_names):
    feat = ShapelyFeature(counties.loc[counties['CountyName'] == name, 'geometry'],  # first argument is the geometry
                          myCRS,  # second argument is the CRS
                          edgecolor='k',  # outline the feature in black
                          facecolor=county_colors[ii],  # set the face color to the corresponding color from the list
                          linewidth=1,  # set the outline width to be 1 pt
                          alpha=0.25)  # set the alpha (transparency) to be 0.25 (out of 1)
    ax.add_feature(feat)  # once we have created the feature, we have to add it to the map using ax.add_feature()
"""
# here, we're setting the edge color to be the same as the face color. Feel free to change this around,
# and experiment with different line widths.
"""water_feat = ShapelyFeature(water['geometry'],  # first argument is the geometry
                            myCRS,  # second argument is the CRS
                            edgecolor='mediumblue',  # set the edgecolor to be mediumblue
                            facecolor='mediumblue',  # set the facecolor to be mediumblue
                            linewidth=1)  # set the outline width to be 1 pt
#ax.add_feature(water_feat)  # add the collection of features to the map

#river_feat = ShapelyFeature(rivers['geometry'],  # first argument is the geometry
                            myCRS,  # second argument is the CRS
                            edgecolor='royalblue',  # set the edgecolor to be royalblue
                            linewidth=0.2)  # set the linewidth to be 0.2 pt
#ax.add_feature(river_feat)  # add the collection of features to the map

# ShapelyFeature creates a polygon, so for point data we can just use ax.plot()
#town_handle = ax.plot(towns.geometry.x, towns.geometry.y, 's', color='0.5', ms=6, transform=myCRS)

# generate a list of handles for the county datasets
#county_handles = generate_handles(counties.CountyName.unique(), county_colors, alpha=0.25)

# note: if you change the color you use to display lakes, you'll want to change it here, too
#water_handle = generate_handles(['Lakes'], ['mediumblue'])

# note: if you change the color you use to display rivers, you'll want to change it here, too
#river_handle = [mlines.Line2D([], [], color='royalblue')]  # have to make this a list

# update county_names to take it out of uppercase text
#nice_names = [name.title() for name in county_names]

# ax.legend() takes a list of handles and a list of labels corresponding to the objects you want to add to the legend
#handles = county_handles + water_handle + river_handle + town_handle
#labels = nice_names + ['Lakes', 'Rivers', 'Towns']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                fontsize=10, loc='upper left', frameon=True, framealpha=1)
"""
gridlines = ax.gridlines(draw_labels=True,  # draw  labels for the grid lines
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],  # add longitude lines at 0.5 deg intervals
                         ylocs=[54, 54.5, 55, 55.5])  # add latitude lines at 0.5 deg intervals
gridlines.left_labels = False  # turn off the left-side labels
gridlines.bottom_labels = False  # turn off the bottom labels

# add the text labels for the towns
"""
#for ind, row in towns.iterrows():  # towns.iterrows() returns the index and row
    x, y = row.geometry.x, row.geometry.y  # get the x,y location for each town
    ax.text(x, y, row['TOWN_NAME'].title(), fontsize=8, transform=myCRS)  # use plt.text to place a label at x,y
"""
# add the scale bar to the axis
scale_bar(ax)

# save the figure as map.png, cropped to the axis (bbox_inches='tight'), and a dpi of 300
myFig.savefig('LatestFireMap.png', bbox_inches='tight', dpi=300)



#Folium Map Testing
""" This will be used to create Folium interactive map at a later stage.
folium.map.activeFires.explore('acq_date',
                 m=m, # add the markers to the same map we just created
                 marker_type='marker', # use a marker for the points, instead of a circle
                 popup=True, # show the information as a popup when we click on the marker
                 legend=False, # don't show a separate legend for the point layer
                )
m.save('NASA_Fire_Map.html') # export the folium fire map as a html which can be opened from windows explorer in the same folder as this python script
"""

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
map = 'map.png'

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
pdf.multi_cell(w = 200, h = 8, txt ="This map shows active fires on the island of cyprus within the last 7 days.", border = 0,
                align = 'L', fill = False)

pdf.set_xy(10,250)
pdf.multi_cell(w = 200, h = 8, txt ="This report has been auto-generated using SNPP VIIRS data, which has been downloaded from the NASA FIRMS Website. For more information please click on the link below: ", border = 0,
                align = 'L', fill = False)

pdf.set_font('Arial', 'U', 10)
pdf.set_text_color(r = 0, g = 0, b = 254)
pdf.cell(w = 30, h = 10, txt = 'https://firms.modaps.eosdis.nasa.gov/', border = 0,
          align = 'B', fill = False, link = 'https://firms.modaps.eosdis.nasa.gov/')





pdf.output('Daily_Fire_Report.pdf', 'F')

"""



print("Script Complete.........") # script complete