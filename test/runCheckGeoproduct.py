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
# result = arcpy.CheckGeoproduct_deltachecker("DIPANU","//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.DIPANU_DIPANUF;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.DIPANU_DIPANUP","#","P:/Z_Systems/GeoDB/Zusatzdaten/NORM@WORKP.sde/NORM.DIPANU_DIPANUP;P:/Z_Systems/GeoDB/Zusatzdaten/NORM@WORKP.sde/NORM.DIPANU_DIPANUF",scriptDir)

#Beispiel mit Änderungen (STREU)
# result = arcpy.CheckGeoproduct_deltachecker("STREU","//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.STREU_STREU","#","P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.STREU_STREU",scriptDir)

#Beispiel mit Änderungen inkl. gelöschte Ebene (KLEK)
result = arcpy.CheckGeoproduct_deltachecker("KLEK","//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_AFLGEW;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_ALDSCH;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_KLMASSNT;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_VBACHS;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_WDHIND;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_WDMSSN;//geodb.infra.be.ch/freigabe/Anwendungen/DeltaChecker/v10.0.0/geodb.sde/GEODB.KLEK_WDWCHS","#","P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.KLEK_AFLGEW;P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.KLEK_ALDSCH;P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.KLEK_VBACHS;P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.KLEK_WDHIND;P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.KLEK_WDMSSN;P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.KLEK_WDWCHS",scriptDir)

print "HTML-Datei: " + result.getOutput(0)
# Der Rückgabewert von result.getOutput ist immer ein Unicode-String (http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//002z0000000n000000)
# Der Wert muss daher mit Python-Funktionen umgewandelt werden (unicode => integer => boolean)                                                                    
print "Geoproduct.hasDelta: " + result.getOutput(1)

resDictJSON = result.getOutput(2)
resDict = json.loads(resDictJSON)
pprint.pprint(resDict)
for tbl in resDict:
    print "NAME der FC: " + tbl['name']
    print "hasDelta: " + str(tbl['hasDelta'])
    print "Status: " + tbl['status']
    for fld in tbl['fields']:
        print "    Feldname: " + fld['name']
        print "    hasDelta: " + str(fld['hasDelta'])
        print "    Status: " +fld['status']
    

print "Ende"