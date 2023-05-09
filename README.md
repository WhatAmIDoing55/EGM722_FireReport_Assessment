# EGM722_FireReport_Assessment
Python script to create a Fire Report, for a local area, using NASA FIRMS Data.

Current plan:
- Use Reuqests to download nasa fire data ( probably csv )
- Geo Geopandas to turn to point shapefile
- Create 'Geofence' to remove detections which occour inside industrail areas / power stations
- Use Maplotlib to create map and graphs to analyse data
- Export map and graph as png

Future Development:
- Import map and graph into pdf report which is ready for the customer 
- Use Folium to create interactive map
