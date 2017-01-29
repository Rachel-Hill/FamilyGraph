#! Python3
import os
import webbrowser

GEDFile = open('C:\\Users\\rachel.hill\\Documents\\NEWHESS2Nov2016\\NEWHESS2Nov2016.GED')

content = GEDFile.readlines()
currentID = ''
#lastTag = ''
person = []
places = []

for i in range(1000):
    #range(len(content)):
    line = content[i].strip()
    if line[0] == '0' and line[-4:] == 'INDI':
        person.append(line[2:-5])
    if line[:6] == '2 PLAC':
        places.append(line[7:])

GEDFile.close()
print(places)


webbrowser.open('https://www.google.com/maps/place/' + places[11])
