import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from IPython.display import display

from arcgis.gis import GIS
from arcgis.features.analyze_patterns import calculate_density, find_hot_spots
from arcgis.features.use_proximity import create_drive_time_areas
from arcgis.features.summarize_data import summarize_within

gis = GIS()