"""Some docstring here."""
import sys
import math
import pandas as pd


def getCoord(zip):
    coord = []
    zip2coord = pd.read_csv('PLZ.tab', sep='\t', lineterminator='\n', converters={'plz': lambda x: str(x)})  # converters to keep leading zeros in plz
    for plz in zip2coord.itertuples():
        if plz[2] == zip:
            coord.append(plz[3])
            coord.append(plz[4])
    return coord


def geoDist(loc1, loc2):
    r = 6372.8  # earth radius
    lon1, lat1 = math.radians(loc1[0]), math.radians(loc1[1])
    lon2, lat2 = math.radians(loc2[0]), math.radians(loc2[1])
    deltaLon = lon2 - lon1
    deltaLat = lat2 - lat1
    h = math.sin(deltaLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(deltaLon / 2)**2
    dist = 2 * r * math.asin(math.sqrt(h))
    return dist


def geoDistZip(zip1, zip2):
    loc1 = getCoord(zip1)
    loc2 = getCoord(zip2)
    dist = geoDist(loc1, loc2)
    return dist


def geoDistZipDF(zips):
    distDF = pd.DataFrame(columns=zips, index=zips)
    dests = zips
    for zip in zips:
        distances = {}
        for dest in dests:
            distances[dest] = geoDistZip(zip, dest)
        distDF.loc[zip] = pd.Series(distances)

#   just 4 eyecandy ;-)
#   un-comment next block to plot a heatmap

#    import matplotlib.pyplot as plt
#    import seaborn as sb
#    distDF = distDF[distDF.columns].astype(float)
#    sb.heatmap(distDF, annot=True, cmap='summer')
#    plt.show()

    return distDF


if __name__ == "__main__":

    helptext = '\nusage:\npython geoDist.py [option] [argument]\n\noption:\n-dm: calculates distance matrix if [argument] is a comma-separated list\n(!without whitespaces) of valid german zip codes\n\nargument:\na) two space-separated german zip-codes to calculate distance between them\nb) a comma-seperated list (!without whitespaces!) of valid german zip codes\nto calculate a distance matrix (only works if option "-dm" is set)\n\n'

    if len(sys.argv) < 3:
        print(helptext)
        sys.exit()
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-dm':
            zips = sys.argv[2]
            zips = zips.split(',')
            distance = geoDistZipDF(zips)
        else:
            zip1 = sys.argv[1]
            zip2 = sys.argv[2]
            distance = geoDistZip(zip1, zip2)
    else:
        print(helptext)
        sys.exit()

    print(distance)
