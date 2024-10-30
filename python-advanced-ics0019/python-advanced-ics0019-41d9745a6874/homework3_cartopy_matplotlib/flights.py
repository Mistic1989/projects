"""Generate map with direct flights from Tallinn comparing years 2020 and 2023."""

import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib import pyplot as plt
from matplotlib import patches as matpatches
import pandas as pd

# read flight data to variables
flights_2020 = pd.read_csv("otselennud20.csv", sep=";")
flights_2023 = pd.read_csv("otselennud23.csv", sep=";")
all_airports = pd.read_csv("airports.dat", sep=",")

# merge files, based on column 'IATA'
merged_results_20 = pd.merge(flights_2020, all_airports, on=["IATA"])
merged_results_23 = pd.merge(flights_2023, all_airports, on=["IATA"])

# creating the base map and add features
proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)
ax.set_extent([-20, 45, 20, 70])
ax.stock_img()
ax.add_feature(cf.NaturalEarthFeature('physical', 'land', '50m',
                                      edgecolor='black',
                                      facecolor=cf.COLORS['land']))
ax.add_feature(cf.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='black', facecolor='lightblue'))
ax.add_feature(cf.NaturalEarthFeature(category='physical', name='rivers_lake_centerlines',
    scale='50m', facecolor='none', edgecolor='lightblue'))
ax.add_feature(cf.BORDERS, linewidth=0.5)

# set the map size
plt.gcf().set_size_inches(20, 15)

# adding flights from year 2020 to the map
for i in merged_results_20.values:
    plt.plot([24.8327999115, i[8]], [59.41329956049999, i[7]],
             color='red', linewidth=1, marker='o',
             transform=ccrs.Geodetic(),
             )
    plt.text(i[8] - 0.5, i[7] - 1, i[1],
             horizontalalignment='left', color='black', size=13,
             transform=ccrs.Geodetic())

# adding flights from year 2023 to the map
for i in merged_results_23.values:
    plt.plot([24.8327999115, i[8]], [59.41329956049999, i[7]],
             color='blue', linewidth=1, marker='o',
             transform=ccrs.Geodetic(),
             )
    plt.text(i[8] - 0.5, i[7] - 1, i[1],
             horizontalalignment='left', color='black', size=13,
             transform=ccrs.Geodetic())

# add title and legend to the map
red = matpatches.Patch(color='red', label='2020 aasta lennud')
blue = matpatches.Patch(color='blue', label='2023 aasta lennud')
ax.legend(handles=[red, blue])
plt.title('Tallinna Lennujaama otselennud aastatel 2020 ja 2023. Alo Ansberg')

# drawing the map and saving it to jpg file

plt.savefig("flights2020_2023.jpg")
plt.show()
