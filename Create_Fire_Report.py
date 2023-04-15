# Libraries
import requests
import pandas as pd

# Fire Data
# SUOMI VIIRS - Last 7 days
snpp_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_7d.csv'

snpp_df = pd.read_csv(snpp_url)