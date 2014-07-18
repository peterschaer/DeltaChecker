# -*- coding: utf-8 -*-
import arcpy
import os
import json
import pprint

#~ Funktion als Variable, es wird lesbarer
dirname = os.path.dirname
scriptDir = dirname(os.path.abspath(__file__))

toolbox = os.path.join(dirname(scriptDir), "DeltaChecker.tbx")
print toolbox
arcpy.ImportToolbox(toolbox)

#Beispiel mit diversen Feldänderungen
# result = arcpy.CheckLayer_deltachecker("P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.FP12_FP12","P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.FP12_FP12_A",scriptDir,"'Typ [type]';'Anzahl Dezimalstellen [scale]';'Anzahl Zeichen [length]';'Anzahl Ziffern [precision]'","'Feature-Typ [featureType]';'Geometrie [shapeType]';'hat M [hasM]'","'Bezeichnung [name]'","#","#")

#Beispiel ohne jede Änderung
result = arcpy.CheckLayer_deltachecker("P:\Z_Systems\GeoDB\Zusatzdaten\Freigabeserver Vektor Historie (GEO).sde\GEODB.AVR_BOF_2014_04","P:\Z_Systems\GeoDB\Zusatzdaten\Freigabeserver Vektor Historie (GEO).sde\GEODB.AVR_BOF_2014_05",scriptDir,"'Typ [type]';'Anzahl Dezimalstellen [scale]';'Anzahl Zeichen [length]';'Anzahl Ziffern [precision]'","'Feature-Typ [featureType]';'Geometrie [shapeType]';'hat M [hasM]'","'Bezeichnung [name]'","#","#")

#Beispiel mit Unterschieden im Wertevergleich
# result = arcpy.CheckLayer_deltachecker("P:\Z_Systems\GeoDB\Zusatzdaten\Freigabeserver Vektor Historie (GEO).sde\GEODB.VEC200_BUILTUPP_2014_01","P:\Z_Systems\GeoDB\Zusatzdaten\Freigabeserver Vektor Historie (GEO).sde\GEODB.VEC200_BUILTUPP_2013_01",scriptDir,"'Typ [type]';'Anzahl Dezimalstellen [scale]';'Anzahl Zeichen [length]';'Anzahl Ziffern [precision]'","'Feature-Typ [featureType]';'Geometrie [shapeType]';'hat M [hasM]'","'Bezeichnung [name]'","#","OBJNAME")

print "HTML-Datei: " + result.getOutput(0)
# Der Rückgabewert von result.getOutput ist immer ein Unicode-String (http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//002z0000000n000000)
# Der Wert muss daher mit Python-Funktionen umgewandelt werden (unicode => integer => boolean)                                                                    
tblHasDelta = result.getOutput(1)
print "Tabelle.hasDelta: " + tblHasDelta

if tblHasDelta.lower() == 'True'.lower():
    print "Delta gefunden"


resDictJSON = result.getOutput(2)
resDict = json.loads(resDictJSON)
pprint.pprint(resDict)
# print "===================================================================="
# pprint.pprint(resDict['fields'])

print "Ende"