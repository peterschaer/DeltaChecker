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

# Beispiel ohne Datenmodelländerung
result = arcpy.CheckGeoproduct_deltachecker("DIPANU","//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.DIPANU_DIPANUF;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.DIPANU_DIPANUP","#","P:/Z_Systems/GeoDB/Zusatzdaten/NORM@WORKP.sde/NORM.DIPANU_DIPANUP;P:/Z_Systems/GeoDB/Zusatzdaten/NORM@WORKP.sde/NORM.DIPANU_DIPANUF",scriptDir)

print "HTML-Datei: " + result.getOutput(0)
# Der Rückgabewert von result.getOutput ist immer ein Unicode-String (http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//002z0000000n000000)
# Der Wert muss daher mit Python-Funktionen umgewandelt werden (unicode => integer => boolean)                                                                    
print "Geoproduct.hasDelta: " + str(bool(int(result.getOutput(1))))

resDictJSON = result.getOutput(2)
resDict = json.loads(resDictJSON)
pprint.pprint(resDict)

print "Ende"