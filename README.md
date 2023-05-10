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

Setup, Installation & Testing

These instructions for setup and installation will assume a Windows operating system with anaconda3 already installed. We will also assume that you are using GitHub desktop or have Git installed on the PC. The create_fire_report.py script uses python version 3.9 and relies on a number of internal and external python libraries. To ensure that there are no issues with dependencies an environment file is supplied within the GitHub repository.
The instructions are broken down into several steps, follow each one to ensure that the script runs properly. At the end of the installation, test data has been supplied to ensure that the script is running with no errors. Follow the Testing instructions and once testing is complete, remember to return the script to its original state to begin using it.
-	Step 1: Visit the GitHub repository found at the following URL and read the README documentation: WhatAmIDoing55/EGM722_FireReport_Assessment: Python script to create a Fire Report, for a local area, using NASA FIRMS Data. (github.com) Clone the repository and open the folder structure on your PC.

-	Step 2: Use the assignment_environment.yml file to install all the required libraries and dependencies used by the script. The script has been developed and ran from PyCharm and relies on Pandas, GeoPandas, Matplotlib and Cartopy. Folium is installed and will be used for further development to create an interactive web map.

-	Step 3: Open PyCharm from the newly imported anaconda environment and launch PyCharm. Once open make sure that PyCharm is using the python interpreter and environment specified by the assignment_environment.yml file.

-	Step 4: From PyCharm, open the create_fire_report.py script. Testing should be carried out to ensure that the script function correctly. To do this follow the instruction given in the section which is titled """  Test Data   """ (Lines 24 – 29). At this stage you will comment out the dataframe on line 26 and uncomment the dataframe on line 29. Running the code now should produce a map and graph using the “SUOMI_VIIRS_C2_Europe_7d (1).csv” stored in the Test Data folder. If the result in the terminal is the same as Figure 5 and the map and graph produced look like those in Fig1 and Fig 2 the script is performing as expected. The final part of Testing is to return lines 26 and 29 to the state they were in at the start of the test (line 26 uncommented, line 29 commented).

Now that the environment file is installed and the script has been tested, it can be run to download fire data and create the map and graph.

